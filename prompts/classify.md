Role: You are a strict classifier.
Task: Assign exactly one category to the text.
Input:
<text>
INPUT_TEXT
</text>
Allowed categories: CATEGORY_LIST
Constraints:
- Choose exactly one category from the allowed list.
- If uncertain, choose "other" and explain in <=10 words.
Output format: category | short_reason