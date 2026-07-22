# Automation 2 — Lead Capture

## Before
- I manually copy lead details from form submissions, email replies, or chat messages into a tracker or CRM.

## After (automated)
- What the automation does: webhook -> Groq qualify -> log every lead -> alert only on hot leads, dedup on email
- Tested: duplicate email correctly updates instead of creating a 2nd row; empty submissions rejected with 400

## Time saved
- Manual time to read + qualify + log 1 lead: ___ min
- Automated time: ~5 sec
- Estimated leads/week at current volume: ___  ->  Weekly time saved: ___ min/week

## Hypothesis
- I will automate the handoff from inbound inquiries into a structured lead list so no new opportunity gets missed.
