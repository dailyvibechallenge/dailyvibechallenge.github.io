---
date: 2026-10-14
---
# #002 — Tool-Using Research Desk Agent
**Difficulty:** Intermediate · **Time:** 2–3 hours · **Theme:** AI agents / tool use

## Description
A minimal CLI agent that answers questions by deciding which of three local tools to call (calculator, file search, a notes store), looping until it has an answer. The point is a clean, inspectable agent loop you fully understand.

## Starter Prompt
```
Build a small command-line AI agent in Python (or TypeScript if you prefer) called "desk-agent".

Requirements:
- Use any chat LLM API with tool/function calling (read the API key from an env var; make the provider swappable behind one function).
- Implement exactly three tools with JSON schemas:
  1. calculator(expression: str) — safely evaluates arithmetic (no eval of arbitrary code).
  2. search_files(query: str) — case-insensitive search across .md/.txt files in ./docs, returning file names and matching lines (max 10).
  3. notes(action: "add"|"list", text?: str) — persists notes to notes.json.
- Agent loop: send the user message plus tool schemas, execute any tool calls, feed results back, repeat until the model returns a final answer or 6 steps pass.
- Print each step clearly: "→ tool: name(args)" and "← result (truncated to 200 chars)".
- Include a ./docs folder with 3 short sample files so it works out of the box.
- Add a --dry-run flag that shows which tool would be called without executing it.

Write a README with setup, an example session, and how to add a new tool. Keep it under ~250 lines of code total.
```

## Success Criteria
- Asking "What's 17% of 2,340, and save that as a note" triggers calculator then notes.
- Asking about content in ./docs triggers search_files and cites the file.
- Loop stops cleanly at the step limit; errors from tools are reported back to the model, not crashed on.

## Optional Extensions
- Add a tiny web UI that streams the step trace.
- Let the agent write its own new tool (sandboxed) and register it.
- Add a token/cost counter per session.
