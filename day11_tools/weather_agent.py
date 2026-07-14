import os, json
from dotenv import load_dotenv
from openai import OpenAI
import time



load_dotenv()
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"],
)

# 1) The actual function the model may call (mocked — swap for a real API later).
def get_weather(city: str) -> dict:
    fake = {"Dubai": 41, "Manila": 32, "Singapore": 30}
    return {"city": city, "temp_c": fake.get(city, 27), "conditions": "sunny"}

# 2) Describe the tool to the model as a JSON schema.
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

def call_with_retry(client, **kwargs):
    for attempt in range(3):
        try:
            return client.chat.completions.create(**kwargs)
        except Exception as e:
            if "tool_use_failed" in str(e) and attempt < 2:
                time.sleep(2 ** attempt)  # 1s, 2s
                continue
            raise

def ask(question: str) -> str:
    messages = [{"role": "user", "content": question}]

    # 3) First call: the model decides whether to call a tool.
    first = client.chat.completions.create(
        model="llama-3.3-70b-versatile", messages=messages, tools=TOOLS,temperature=0,
    )
    msg = first.choices[0].message

    # 4) If it asked for a tool, run it and send the result back.
    if msg.tool_calls:
        messages.append(msg)  # the assistant's tool-call message
        for call in msg.tool_calls:
            args = json.loads(call.function.arguments)
            result = get_weather(**args)          # <-- your code runs here
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(result),
            })
        # 5) Second call: model writes the final answer using the tool result.
        second = client.chat.completions.create(
            model="llama-3.3-70b-versatile", messages=messages,
        )
        return second.choices[0].message.content
    return msg.content

if __name__ == "__main__":
    for q in ["What's the weather in Dubai?", "Is it hotter in Manila or Singapore?"]:
        print(f"Q: {q}\nA: {ask(q)}\n")