---
date: 2026-10-20
---
# #010 — Pocket Coding Agent: Watch a Tiny Agent Fix Failing Tests in a Browser Sandbox
**Difficulty:** Intermediate · **Time:** 2–4 hours · **Theme:** AI agents / tool use

## Description
Build a single-page "coding agent in a jar": a tiny in-browser project with a few buggy JavaScript functions and a test suite, plus an agent that can only touch it through five tools (list files, read file, run tests, propose edit, finish). You watch every tool call stream into a trace panel, approve or reject each edit like a real human-in-the-loop review, and see the test bar turn from red to green. It works offline with a scripted mock model, and plugs into a real LLM API with tool calling when you add a key. It is the clearest way to understand how coding agents actually loop.

## Starter Prompt
```
Build "Pocket Coding Agent", a single-page web app (one index.html, vanilla JS, CSS) where an AI agent fixes failing unit tests inside an in-memory sandbox, using only tool calls. No build step and no frameworks. The only network call allowed is the optional LLM API request described below.

Sandbox project (in memory, stored as a JS object of path -> source string):
- src/slugify.js: export a slugify(text) function with 2 bugs (does not lowercase, leaves double dashes).
- src/cart.js: export cartTotal(items, discountPct) with 1 bug (applies discount before quantity).
- src/dates.js: export daysBetween(a, b) with 1 off-by-one bug.
- tests/all.test.js: 10-12 small tests using a tiny assert helper you write (equal, deepEqual), covering all three files.
- A "Reset sandbox" button restores the original buggy files. A "Shuffle bugs" button picks a different set of 3-4 bugs from a list of at least 8 prepared bug variants, so runs differ.

Test runner:
- Run tests safely in a Web Worker: send the current file contents, rewrite simple "export function" lines into plain functions, evaluate them with new Function inside the worker, run each test with a 500 ms timeout, and post back a result list {name, pass, message}.
- Show a big progress bar "7 / 11 passing" that animates when it changes.

Agent tools (the agent can do nothing else):
1. list_files() -> array of paths
2. read_file(path) -> source with line numbers
3. run_tests() -> pass/fail list with assertion messages
4. propose_edit(path, find, replace, reason) -> applies only after the user clicks Approve (or immediately if "Auto-approve" is on). Reject sends "Edit rejected by reviewer: <optional note>" back to the agent as the tool result. The edit fails with a clear error if `find` is not found exactly once.
5. finish(summary) -> ends the run.
Define all tools in one array with name, description and JSON Schema parameters, so the same definitions feed both the mock model and the real LLM.

Agent loop:
- Messages array (system, user, assistant, tool). Loop: send messages + tools to the model, execute any tool calls, append results, repeat until finish() or a 25-step limit. Show a Stop button that cancels between steps.
- Mock model mode (default, no key needed): a deterministic scripted policy that lists files, runs tests, reads the file named in the first failing test, proposes a fix from a lookup table keyed by bug variant, re-runs tests, and repeats. It should also make one deliberately wrong edit on the first run so the reviewer can reject it and watch the agent recover.
- Real LLM mode: a settings panel with provider base URL, model name and API key (kept in sessionStorage only, never localStorage). Use an OpenAI-compatible /chat/completions request with the "tools" field. Handle malformed tool arguments by returning a tool error instead of crashing.

UI (three columns on desktop, stacked on mobile):
- Left: file tree and a read-only code view with line numbers; lines just edited are highlighted for 3 seconds, and pending edits show a red/green diff with Approve / Reject buttons.
- Middle: a live trace of every step: model thought text (if any), tool name, arguments as pretty JSON, result (collapsible), and elapsed ms. Color-code by tool.
- Right: test results list, the progress bar, step counter, and a run summary card (steps, edits approved/rejected, tests fixed) when finish() is called.
- An "Export trace" button downloads the full run as JSON.

Quality bar: no console errors, keyboard accessible buttons, works offline in mock mode, and a single file under ~900 lines.

When done, explain the agent loop, why the tools are narrow, and how the human approval step works, and suggest 3 safety improvements a real coding agent would need.
```

## Success Criteria
- Opening index.html shows the sandbox files and a red test bar, and Run (mock mode) drives the agent until all tests pass without any API key.
- Every tool call appears in the trace panel with its arguments and result, in order, and the trace can be exported as JSON.
- Edits wait for your Approve or Reject, a rejected edit is reported back to the agent, and the agent recovers and still finishes.
- Tests run inside a Web Worker with a timeout, so an infinite loop in an edited file cannot freeze the page.
- With a valid key and an OpenAI-compatible endpoint, the same tool definitions work with a real model.

## Optional Extensions
- Add a "budget" meter: each tool call costs tokens or points, and the run fails gracefully when the budget runs out.
- Race two agents (mock vs. real LLM, or two models) on the same shuffled bugs and compare steps and rejected edits.
- Add a write_test(path, name, code) tool and ask the agent to cover an untested edge case before fixing it.
- Replay mode: load an exported trace and step through it like a debugger timeline.
