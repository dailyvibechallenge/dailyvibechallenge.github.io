---
date: 2026-10-26
---
# #016 — Terminal Tape: Record a Shell Session and Turn It into a Step-by-Step Web Tutorial
**Difficulty:** Intermediate · **Time:** 2–3 hours · **Theme:** Dev tools

## Description
Every "how I set this up" doc goes stale the moment you finish typing it. Today you build a tiny dev tool that records a real terminal session (every command, its output and exit code) and turns it into a clean, single-file web tutorial: numbered steps, copy buttons on each command, collapsible output, failed commands flagged in red, and optional AI-written one-line explanations for each step. Run it once while you set up a project and you get a shareable walkthrough that is true by construction, because it is exactly what you ran.

## Starter Prompt
```
Build "Terminal Tape", a CLI that records a shell session and exports it as a step-by-step HTML tutorial. Use Node.js 18+ with no dependencies (child_process, readline, fs, fetch). Files: tape.js, template.html, README.md, and an examples/ folder.

Recording
- `node tape.js record my-setup` starts a simple REPL with the prompt "tape> ". Each line you type is run with the user's shell (bash -lc on macOS/Linux, cmd /c on Windows) in a persistent working directory: handle `cd` yourself so later commands run in the new folder, and keep exported env vars set with `export NAME=value`.
- Stream stdout/stderr live to the terminal while also capturing them. Save each step to tapes/my-setup.json as { n, cwd, command, stdout, stderr, exitCode, durationMs, startedAt }.
- Built-in commands: `#note some text` adds a narration step with no command, `!undo` drops the last step, `!stop` ends recording. Ctrl+C kills the running command, not the recorder.
- Redact secrets before saving: mask values of env vars whose names contain KEY, TOKEN, SECRET or PASSWORD, plus anything that looks like a bearer token or a long hex/base64 string. Print how many values were redacted.
- Truncate any output longer than 200 lines to the first 80 and last 40, with a "… N lines hidden …" marker.

Exporting
- `node tape.js export my-setup` writes tapes/my-setup.html, one self-contained file (inline CSS/JS) built from template.html: a title, a short summary (step count, total time, failures), then numbered steps. Each command step shows the cwd, the command in a code block with a Copy button, output in a collapsible <details> (open by default if under 15 lines), and a red "failed (exit N)" badge for non-zero exits. Notes render as plain paragraphs.
- Add a sticky table of contents and a "Copy all commands" button that copies only the successful commands as a runnable script.
- Optional AI explanations: `--explain` sends each command plus the first 30 lines of its output to an OpenAI-compatible endpoint (baseUrl, model and the env var name for the key come from tape.config.json; never write keys to disk) and adds a one-sentence "what this did" line under each step. Without a key, skip it gracefully.

Also
- `node tape.js list` shows saved tapes with step counts and dates.
- Include examples/hello-node.json and its exported HTML so the README can show output without recording anything.
- README: install, a 30-second quick start, how redaction works, and its limits (interactive programs like vim or top are not supported).
```

## Success Criteria
- Recording `mkdir demo && cd demo`, `npm init -y`, and a command that fails produces a JSON tape with correct cwd, output, and exit codes for every step.
- `cd` and `export` persist across steps, and Ctrl+C stops a long command without ending the recording.
- The exported HTML opens offline as one file, with working Copy buttons, collapsible output, and the failed step clearly flagged.
- A fake `export API_KEY=sk-123...` in a session never appears in the JSON or HTML.
- "Copy all commands" yields a script that reruns the successful steps in a fresh folder.

## Optional Extensions
- Add a `replay` mode that re-runs a tape in a temp folder and marks steps whose output or exit code changed, so you can tell when a tutorial has gone stale.
- Export to Markdown as well, ready to paste into a README or a blog post.
- Add a typing-animation "play" button that replays the session like a terminal recording.
- Let an AI agent read the tape and suggest which steps could be merged or dropped to make the tutorial shorter.
