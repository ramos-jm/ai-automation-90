import os
from typing import TypedDict, Annotated
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# 1) Define the STATE shape. `messages` uses the add_messages reducer so new
#    messages append (not overwrite). This is the standard chat-agent state.
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 2) Define a NODE: a function (state) -> partial state update.
def chatbot(state: State):
    reply = llm.invoke(state["messages"])
    return {"messages": [reply]}  # appended to state['messages'] by the reducer

# 3) Build the GRAPH: register the node, then wire the EDGES.
builder = StateGraph(State)
builder.add_node("chatbot", chatbot)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)
graph = builder.compile()

# 4) Run it. Input is the initial state; output is the final state.
result = graph.invoke({"messages": [HumanMessage("Write 3 different reason why I should use AI agents in my business.")]})
for m in result["messages"]:
    print(f"[{m.type}] {m.content}")