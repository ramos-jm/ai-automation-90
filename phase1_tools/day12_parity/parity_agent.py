import os, json, sys
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROVIDERS = {
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "key_env": "GROQ_API_KEY",
        "model": "openai/gpt-oss-120b",
    },
    "gemini": {
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "key_env": "GEMINI_API_KEY",
        "model": "gemini-2.5-flash",
    },
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "key_env": "OPENROUTER_API_KEY",
        "model": "openrouter/free",
    },
}

def get_weather(city: str) -> dict:
    fake = {"Dubai": 41, "Manila": 32, "Singapore": 30, "Tokyo": 28, "London": 18}
    return {"city": city, "temp_c": fake.get(city, 27), "conditions": "sunny"}

TOOLS = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the current weather for a city.",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string", "description": "City name"}},
            "required": ["city"],
        },
    },
}]

def make_client(name: str):
    cfg = PROVIDERS[name]
    return OpenAI(base_url=cfg["base_url"], api_key=os.environ[cfg["key_env"]]), cfg["model"]

def ask(name: str, question: str) -> str:
    client, model = make_client(name)
    messages = [{"role": "user", "content": question}]

    for _ in range(5):  # safety cap to avoid infinite loops
        response = client.chat.completions.create(
            model=model, messages=messages, tools=TOOLS, temperature=0,
        )
        msg = response.choices[0].message

        if not msg.tool_calls:
            return msg.content

        messages.append(msg)
        for call in msg.tool_calls:
            args = json.loads(call.function.arguments)
            result = get_weather(**args)
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(result),
            })

    return "Error: too many tool-call iterations"


if __name__ == "__main__":
    questions = [
        "What's the weather in Dubai?",
        "Is it hotter in Manila or Singapore?",
        # The hard one: forces multiple tool calls + multi-step arithmetic reasoning
        "Get the weather for Dubai, Manila, Singapore, Tokyo, and London. "
        "Rank them from hottest to coldest, identify the two cities with the "
        "smallest temperature difference between them and state that difference, "
        "and calculate the average temperature across all five cities rounded to one decimal place.",
    ]
    providers = sys.argv[1:] or ["groq", "gemini", "openrouter"]
    for p in providers:
        print(f"\n=== {p} ===")
        for q in questions:
            print(f"Q: {q}\nA: {ask(p, q)}\n")