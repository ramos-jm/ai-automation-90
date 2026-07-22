import os, json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"],
)

TICKET_SCHEMA = {
    "type": "object",
    "properties": {
        "category": {
            "type": "string",
            "enum": ["billing", "technical", "account", "feature_request", "other"],
        },
        "priority": {
            "type": "string",
            "enum": ["low", "medium", "high", "urgent"],
        },
        "summary": {"type": "string", "description": "One-sentence summary."},
    },
    "required": ["category", "priority", "summary"],
    "additionalProperties": False,
}

def classify(ticket_text: str) -> dict:
    # response_format with a json_schema forces schema-valid JSON.
    # (Same idea on Gemini via response_schema, on OpenAI via json_schema.)
    # Some providers/models (e.g. Groq llama variants) don't support
    # the `json_schema` response_format. Request strict JSON output
    # via a system instruction instead and parse the model's content.
    system_msg = (
        "You will receive a support ticket. Respond with a single valid JSON object only,\n"
        "strictly matching the following fields: category (one of: billing, technical, account, feature_request, other),\n"
        "priority (one of: low, medium, high, urgent), and summary (one-sentence summary).\n"
        "Do not include any additional text, formatting, or explanation."
    )

    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": f"Classify this support ticket:\n\n{ticket_text}"},
        ],
    )
    
    return json.loads(resp.choices[0].message.content)

SAMPLES = [
    "I was charged twice for my subscription this month, please refund.",
    "The export button throws a 500 error every time I click it.",
    "Can you add dark mode to the dashboard?",
    "I forgot my password and the reset email never arrives.",
    "Your service is down and my whole team is blocked right now!!",
]

if __name__ == "__main__":
    passed = 0
    for t in SAMPLES:
        out = classify(t)
        assert set(out) >= {"category", "priority", "summary"}
        print(json.dumps(out, indent=2))
        passed += 1
    print(f"\n{passed}/{len(SAMPLES)} tickets returned valid schema")