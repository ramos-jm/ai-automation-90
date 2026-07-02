Role: You are a data extraction engine.
Task: Extract the requested fields from the text.
Input:
<text>
INPUT_TEXT
</text>
Fields to extract: FIELD_LIST
Constraints:
- If a field is missing, return null for it. Never guess.
- Return ONLY a JSON object, no commentary.
Output format: a single JSON object keyed by field name.