# PROGRESS — ai-automation-90

## Day 1
- Built: repo scaffold, env, hello_llm.py
- Broke/learned: Basic API for LLM

## Day 2 — Prompt engineering fundamentals ✅

**Built:** 3 reusable prompt templates in `prompts/` (`summarize.md`, `extract.md`, `classify.md`),
each with ALL_CAPS placeholders filled at call time via `day02_prompts.py`.
Provider: Groq (`llama-3.3-70b-versatile`), OpenAI-compatible client.

### Test results (2 inputs each)

**summarize.md** — 2/2 ✅ (concise, neutral, numbers/dates preserved)
- Revenue text →
  * Q2 revenue was $1.2M, up 30% from Q1
  * 4 engineers were hired
  * The mobile app shipped on May 14
- Outage text →
  * The server outage on June 3 lasted 2 hours
  * It affected 500 users
  * It was caused by a bad deploy

**extract.md** — 2/2 ✅ (valid JSON, correct fields, no hallucination)
- Contact text (FIELD_LIST = name, email, phone, location) →
  {"name": "Maria Santos", "email": "maria@example.com", "phone": "+971 50 123 4567", "location": "Dubai"}
- Contact text (re-run, same fields) →
  {"name": "Maria Santos", "email": "maria@example.com", "phone": "+971 50 123 4567", "location": "Dubai"}

**classify.md** — 2/2 ✅ (single category + short reason)
- "My card was charged but I never got the product." → billing | unauthorized charge issue
- "Can you add a dark mode toggle?" → feature_request | Requesting new functionality addition

### What I learned
- Switched the "swap the contents" step to "swap the user message `content`" now that we're on the
  OpenAI-compatible client (`messages=[...]`).
- Placeholder tests must match the input's field list — a `null` result can mean the guardrail is
  working, not that the prompt failed.
- Multi-character placeholders (FIELD_LIST, CATEGORY_LIST, MAX_BULLETS) avoid the `str.replace("N", ...)`
  collision footgun.

**Definition of done:** ✅ 3 templates, each correct on 2 test inputs.
**Commit:** `git commit -am "Day 2: prompt templates + tutorial ch1-3"`