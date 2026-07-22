import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

# =====================================================
# Part A - Simple Chain
# =====================================================

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a concise assistant. Answer in one sentence."),
    ("human", "{question}")
])

chain = prompt | llm | StrOutputParser()

print(
    "A:",
    chain.invoke(
        {"question": "What is an AI agent, in one sentence?"}
    ),
)

# =====================================================
# Stage 1 - Ticket Classification Agent
# =====================================================

class TicketClassification(BaseModel):
    category: str = Field(description="billing, technical, account, other")
    priority: str = Field(description="low, medium, high, urgent")
    summary: str = Field(description="one sentence summary")


classifier = llm.with_structured_output(TicketClassification)

ticket = classifier.invoke(
    """
    Classify this support ticket:

    "I was double-charged and need a refund today."
    """
)

print("\nStage 1")
print(ticket)

# =====================================================
# Stage 2 - Resolution Time Agent
# =====================================================

class ResolutionEstimate(BaseModel):
    estimated_hours: float = Field(
        description="Estimated hours to resolve"
    )
    sla: str = Field(
        description="Suggested SLA"
    )
    reasoning: str = Field(
        description="Why this estimate was chosen"
    )


estimator = llm.with_structured_output(ResolutionEstimate)

estimate = estimator.invoke(
    f"""
    You are an experienced IT support manager.

    Ticket Category:
    {ticket.category}

    Ticket Priority:
    {ticket.priority}

    Ticket Summary:
    {ticket.summary}

    Estimate how long this should take to resolve.
    """
)

print("\nStage 2")
print(estimate)

# =====================================================
# Stage 3 - Customer Reply Agent
# =====================================================

reply_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "Write a friendly customer support response."
    ),
    (
        "human",
        """
Ticket Summary:
{summary}

Priority:
{priority}

Estimated Resolution:
{hours} hours

SLA:
{sla}

"""
    )
])

reply_chain = reply_prompt | llm | StrOutputParser()

reply = reply_chain.invoke({
    "summary": ticket.summary,
    "priority": ticket.priority,
    "hours": estimate.estimated_hours,
    "sla": estimate.sla
})

print("\nStage 3")
print(reply)