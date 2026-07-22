import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"],
)

def run_prompt(template_path: str, replacements: dict) -> str:
    """Load a prompt template, fill ALL_CAPS placeholders, send to the model."""
    # Using 'with' ensures the file handle is properly closed
    with open(template_path, encoding="utf-8") as f:
        prompt = f.read()
        
    for placeholder, value in replacements.items():
        prompt = prompt.replace(placeholder, str(value))
        
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content

if __name__ == "__main__":
    # --- summarize.md ---
    for text in [
        "Our Q2 revenue hit $1.2M, up 30% from Q1. We hired 4 engineers and shipped the mobile app on May 14.",
        "The server outage on June 3 lasted 2 hours, affected 500 users, and was caused by a bad deploy.",
    ]:
        print(run_prompt("prompts/summarize.md", {"INPUT_TEXT": text, "MAX_BULLETS": "3"}))
        print("---")

    # --- extract.md ---
    for text in [
        "Invoice #A-102 from Acme Corp, dated 2026-06-01, total $4,500, due 2026-06-30.",
        "Contact: Maria Santos, maria@example.com, +971 50 123 4567, based in Dubai.",
    ]:
        print(run_prompt("prompts/extract.md", {
    "INPUT_TEXT": "Contact: Maria Santos, maria@example.com, +971 50 123 4567, based in Dubai.",
    "FIELD_LIST": "name, email, phone, location",
        }))
        print("---")

    # --- classify.md ---
    for text in [
        "My card was charged but I never got the product.",
        "Can you add a dark mode toggle?",
    ]:
        print(run_prompt("prompts/classify.md", {
            "INPUT_TEXT": text,
            "CATEGORY_LIST": "billing, technical, account, feature_request, other",
        }))
        print("---")