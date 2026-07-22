# Automation 3 — File/Report Processing

## Before
- I manually open downloaded reports, scan them for important changes, and summarize the findings before sharing them with others.

## After (automated)
- What the automation does: file dropped in Drive -> extract text -> Groq structures Overview/Findings/Action Items -> logged + emailed
- Tested: 3 files processed one after another (dropped ~70s apart so each poll caught one), each produced a distinct correct report

## Time saved
- Manual time to read + structure 1 file into a report: ~15 min
- Automated time: ~20-30 sec
- Files processed per week at current volume: ~10  ->  Weekly time saved: ~145 min/week (~2.4 hrs)

## Hypothesis
- I will automate the process of turning raw reports into a quick summary so I can review updates in less time.
