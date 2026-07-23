import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain.agents import create_agent   # <-- changed

load_dotenv()
llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)

@tool
def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression, e.g. '12 * (3 + 4)'.
    Use this whenever the user asks for a calculation."""
    allowed = set("0123456789+-*/(). ")
    if not set(expression) <= allowed:
        return "Error: only numbers and + - * / ( ) are allowed."
    try:
        return str(eval(expression))  # safe: input is filtered to arithmetic only
    except Exception as e:
        return f"Error: {e}"

@tool
def search_docs(query: str) -> str:
    """Look up a fact in the internal knowledge base.
    Use this for questions about company policies or products."""
    FAKE_KB = {
        "refund": "Refunds are processed within 5 business days.",
        "hours": "Support is available 9am-6pm GST, Sunday to Thursday.",
    }
    for key, val in FAKE_KB.items():
        if key in query.lower():
            return val
    return "No matching entry found in the knowledge base."

# One line builds the full think -> act -> think loop with both tools.
agent = create_agent(llm, tools=[calculator, search_docs])   # <-- changed

QUESTIONS = [
    "What is 137 * 24?",                                 # -> calculator
    "What is your refund policy?",                        # -> search_docs
    "What are your support hours, and what is 569 / 69?",   # -> both
    "Do you know how many days it would take if I walk from my home to the moon?" # -> error testing
]

for q in QUESTIONS:
    result = agent.invoke({"messages": [("user", q)]})
    print(f"\nQ: {q}\nA: {result['messages'][-1].content}")