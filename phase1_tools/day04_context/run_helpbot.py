import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("Missing API key. Set OPENAI_API_KEY or GROQ_API_KEY in .env.")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1" if "GROQ_API_KEY" in os.environ else None,
)

SYSTEM = open("day04_context/system_prompt.md", encoding="utf-8").read()
CONTEXT = open("day04_context/context.md").read()   # your short knowledge doc (FAQ-style facts)

def ask(question, use_context: bool):
    if use_context:
        messages = [
            {"role": "system", "content": SYSTEM + "\n\nKnowledge base:\n" + CONTEXT},
            {"role": "user",   "content": question},
        ]
    else:  # bare prompt — no system, no context
        messages = [{"role": "user", "content": question}]
    resp = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=messages)
    return resp.choices[0].message.content

QUESTIONS = [
    "How many days are there in a month?",
    "What's your refund policy for annual plans?",
]

for q in QUESTIONS:
    print("Q:", q)
    print("WITH context:", ask(q, True))
    print("BARE:        ", ask(q, False))
    print("---")