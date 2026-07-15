# PROGRESS — ai-automation-90

## Day 1 — Repo scaffold + first LLM call ✅

**Built:** Repo scaffold (`.gitignore`, `.env.example`, `requirements.txt`),
`day01_setup/hello_llm.py` — first live call via Gemini (`google-genai`, `gemini-2.5-flash`).

### What I learned
- Env vars via `python-dotenv` keep keys out of git; `.env` stays local.
- Gemini client uses `client.models.generate_content(...)`, not the chat-completions shape.

**Definition of done:** ✅ Scaffold + one successful LLM print.
**Commit:** `Day 1 - Done` (`c7a210f`) / scaffold (`a46ae9e`)

---

## Day 2 — Prompt engineering fundamentals ✅

**Built:** 3 reusable prompt templates in `prompts/` (`summarize.md`, `extract.md`, `classify.md`),
each with ALL_CAPS placeholders filled at call time via `day02_setup/day02_prompts.py`.
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
**Commit:** `Day 2 - Done` (`ad5b5a9`)

---

## Day 3 — Structured ticket classification ✅

**Built:** `day03_structured/classify_ticket.py` — classifies support tickets into a fixed schema:
`category` (enum), `priority` (enum), `summary` (one sentence). Groq + system instruction that
demands JSON-only output, then `json.loads` + assert on required keys.

### Test results (5 samples)

Ran all `SAMPLES`; each returned valid keys → **5/5** schema-valid.

| Ticket | Expected shape |
|---|---|
| Double charge / refund | category + priority + summary |
| Export button 500 | category + priority + summary |
| Dark mode request | category + priority + summary |
| Password reset email missing | category + priority + summary |
| Service down / team blocked | category + priority + summary |

### What I learned
- Groq `llama-3.3-70b-versatile` does not reliably support `response_format: json_schema`;
  prompt the schema in the system message and parse content instead.
- Assert `set(out) >= {"category", "priority", "summary"}` catches incomplete replies early.

**Definition of done:** ✅ 5 tickets → valid JSON schema.
**Commit:** `Day 3 - Done` (`01a03c7`)

---

## Day 4 — Context / RAG-lite HelpBot ✅

**Built:** `day04_context/` — `system_prompt.md` (HelpBot rules + few-shots), `context.md` (short FAQ),
`run_helpbot.py` (WITH context vs BARE prompt comparison). Same Groq client.

### Test results (2 questions × 2 modes)

**"How many days are there in a month?"**
- WITH context → stays grounded / declines inventing facts outside KB
- BARE → answers from general knowledge (no grounding)

**"What's your refund policy for annual plans?"**
- WITH context → ticket offer line from KB rules (no published refund policy in `context.md`)
- BARE → invents / guesses a policy

### What I learned
- System prompt + pasted KB beats a bare user prompt for honesty ("I don't have that…").
- Few-shots in the system prompt teach the exact refusal phrase.

**Definition of done:** ✅ HelpBot answers from context; bare mode hallucinates policies.
**Commit:** `Day 4 - Done` (`3ec68d3`)

---

## Day 5 — n8n GitHub → Google Sheets ✅

**Built:** `day05_n8n/day05-github-to-sheets.json`
Flow: Manual Trigger → HTTP Request (`GET https://api.github.com/repos/n8n-io/n8n`) →
Edit Fields → Append row in Google Sheets (`name`, `stargazers_count`, `updated_at`).

### What I learned
- n8n expressions (`={{ $json.name }}`) map API fields into sheet columns.
- OAuth credential for Sheets lives in n8n; the exported JSON is the portable workflow.

**Definition of done:** ✅ Manual run appends one GitHub repo row to Sheets.
**Commit:** `Day 5: n8n GitHub-to-Sheets workflow` (`a1d4d41`)

---

## Day 6 — n8n summarize-and-deliver (Groq via HTTP) ✅

**Built:** `day06_n8n_LLM/Day06-summarize-and-deliver.json`
Flow: Manual Trigger → Story Writer (Groq HTTP, write essay) → Story Summarizer (Groq HTTP,
5 bullets) → Manual Mapping → Append row in Sheets (`summary`, `input_preview`).

### What I learned
- Call Groq from n8n with Header Auth + raw JSON body to `/openai/v1/chat/completions`.
- Chain two LLM HTTP nodes; `JSON.stringify(...)` keeps nested prompt strings valid in the body.
- Map `$json.choices[0].message.content` into sheet columns before append.

**Definition of done:** ✅ Essay → summary → one Sheets row.
**Commit:** `Day 6: n8n summarize-and-deliver (Groq via HTTP)` (`8879e9f`)

---

## Day 7 — n8n webhook receive / transform / respond ✅

**Built:** `day07_webhook/day07-webhook-echo.json`
Flow: Webhook (POST, `responseMode: responseNode`) → Edit Fields
(`received_name`, greeting `message`, `received_at`) → Respond to Webhook (JSON).

### What I learned
- `responseMode: responseNode` + Respond to Webhook returns a custom body instead of the default ack.
- Read payload via `$json.body.name`; stamp time with `$now.toISO()`.

**Definition of done:** ✅ POST → shaped JSON response with name + timestamp.
**Commit:** `Day 7: n8n webhook receive/transform/respond` (`29f6718`)

---

## Day 8 — Retries + error branch + failure alerts ✅

**Built:** `day08_resilience/day08-summarize-resilient.json` + `failure_notes.md`
Hardened Day 6 pattern: Story Writer has `retryOnFail: true` and `onError: continueErrorOutput`.
Error path: Build Alert → parse/format error → Error Sheet (Google Sheets).

### Induced failures (documented in `failure_notes.md`)

**400** — invalid `role` on `messages.0` → alert logged with message/type/code.
**401** — invalid API key → alert logged with `invalid_api_key`.

### What I learned
- `continueErrorOutput` splits success vs failure without killing the whole run.
- Retries alone are not enough — persist a readable alert row when the happy path fails.
- Parsing nested Axios / API error blobs needs cleanup before `JSON.parse`.

**Definition of done:** ✅ Retries + error branch writes failure alerts to Sheets.
**Commit:** `Day 8: retries + error branch + failure alerts` (`3e38164`)

---

## Day 9 — Make.com GitHub → Sheets ✅

**Built:** `day09_make/blueprint.json` ("Integration HTTP")
Scenario: HTTP `GET` GitHub repo → Google Sheets `addRow`
(same idea as Day 5, Make instead of n8n). Folder renamed `day9_make` → `day09_make` for linear naming.

### What I learned
- Make blueprints export as JSON modules (`http:MakeRequest`, `google-sheets:addRow`).
- Porting Day 5 to Make is mostly credentials + mapper fields, not new business logic.

**Definition of done:** ✅ Make scenario appends GitHub repo row to Sheets.
**Commit:** `Day 9: Make GitHub-to-Sheets scenario` (`afd823f`, rename `aecf147`)

---

## Day 10 — Make router + filters + webhook integrations ✅

**Built:** three Make blueprints in `day10_make/`:

1. **`filter-scenario.blueprint.json`** — HTTP GitHub → BasicRouter:
   - "Popular" branch when `stargazers_count > 10000` → Sheet1
   - "lowstar" branch → `low-star` sheet
   - `onerror` / Resume path for failed sheet writes
2. **`Tally Webhook.blueprint.json`** — Tally new response → Sheets append → router →
   Browse AI task (scrape website link) → update sheet row
3. **`Integration Browse AI.blueprint.json`** — Browse AI task finished webhook →
   filter/find sheet row → update with scrape results

### What I learned
- Make Router + filters replace IF/Else sprawl; each route can target a different sheet/tab.
- Webhook chains (Tally → Browse AI → Sheets) need a row key to update the right submission later.
- Error handlers (`onerror` + Resume) keep a bad write from stranding the whole scenario.

**Definition of done:** ✅ Router/filters + Tally/Browse AI → Sheets round-trip.
**Commit:** `Day 10: Make router + filters + schedule + error handler` (`3cd06f1`)

---

## Day 11 — LLM tool use / function calling ✅

**Built:** `day11_tools/weather_agent.py` — Groq function calling with mocked `get_weather(city)`.
Loop: ask model with `tools=` → if `tool_calls`, run local function → append `role: tool` → second completion.
Includes `call_with_retry` for transient `tool_use_failed` errors (not wired into `ask` yet).

### Test questions
- "What's the weather in Dubai?" → tool call → uses mocked temp (41°C)
- "Is it hotter in Manila or Singapore?" → tool call(s) → compares 32 vs 30

### What I learned
- Tool schemas are JSON; the model only *requests* the call — your code must execute it.
- Append the assistant `tool_calls` message before tool results or the second turn breaks.
- `temperature=0` makes tool choice more stable for demos.

**Definition of done:** ✅ Model calls `get_weather` and answers from tool results.
**Commit:** `Day 11: LLM tool use / function calling (Groq)` (`2861c3c`)

---

## Day 12 — Provider-agnostic agent (parity) ✅

**Built:** `day12_parity/parity_agent.py` — same weather tool agent across three OpenAI-compatible backends:
- **groq** — `openai/gpt-oss-120b` + `GROQ_API_KEY`
- **gemini** — `gemini-2.5-flash` via Generative Language OpenAI endpoint + `GEMINI_API_KEY`
- **openrouter** — `openrouter/free` + `OPENROUTER_API_KEY`

Multi-step loop (cap 5) for multi-tool questions; CLI: `python parity_agent.py [groq|gemini|openrouter...]`.

### Hard question (forces multi-tool + arithmetic)
Weather for Dubai, Manila, Singapore, Tokyo, London → rank hottest→coldest, smallest pairwise temp
diff, average to 1 decimal.

### What I learned
- One tool schema + OpenAI client works across providers if each exposes a chat-completions URL.
- Harder prompts expose provider differences (tool loops, reasoning quality) more than hello-world does.
- Cap tool iterations to avoid infinite call loops.

**Definition of done:** ✅ Same agent runs on Groq / Gemini / OpenRouter with shared tools.
**Commit:** `Day 12: provider-agnostic agent (Groq/OpenRouter/Gemini)` (`636c782`)

---

**Status:** Days 1–12 complete in repo. Next day TBD.
