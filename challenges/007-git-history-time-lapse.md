---
date: 2026-10-17
---
# #007 — Repo Time-Lapse: Turn Any Git History into a Playable Visual Timeline
**Difficulty:** Intermediate · **Time:** 2–3 hours · **Theme:** Dev tools

## Description
Build a tiny command-line dev tool that reads the git history of any local repository and writes one self-contained HTML file you can open in a browser and press play. Files appear as glowing dots grouped by folder, pulse when they change, fade when they are deleted, and a scrubber lets you jump through time while commit messages scroll by. It is a fun way to see how a project really grew, and a perfect weekend screenshot for your README.

## Starter Prompt
```
Build "Repo Time-Lapse", a command-line tool that turns a git repository's history into a single self-contained, playable HTML visualization. Use Python 3 standard library only (subprocess, json, argparse, html) for the CLI, and vanilla JS + Canvas inside the generated HTML. No external libraries, no CDN, no network calls.

CLI:
- Usage: python3 timelapse.py [REPO_PATH] [-o out.html] [--since 2024-01-01] [--max-commits 2000] [--branch main]
- Default REPO_PATH is the current directory; exit with a friendly error if it is not a git repo.
- Read history with: git log --reverse --no-merges --date=iso-strict --pretty=format:'%H|%an|%ad|%s' --name-status
  Parse each commit into {hash, author, date, message, changes:[{status A/M/D/R, path, old_path?}]}. Handle renames (R100 old new) and paths with spaces.
- Anonymize option: --hide-authors replaces author names with "Dev 1", "Dev 2" in order of first appearance.
- Embed the parsed data as JSON inside one HTML file (escape "</" safely) and print the output path plus a one-line summary (commits, files, authors, date range).

Visualization (inside the HTML):
- Full-window canvas, dark background. Each file is a dot; files cluster around their top-level folder, and folders are arranged in a circle with their name labels.
- Use a simple force layout or deterministic spiral placement within each folder cluster so dots don't overlap much.
- Dot color by file extension (stable hash -> hue), with a legend of the top 8 extensions.
- Playback: on each commit, added files fade in, modified files pulse (brief glow + grow), deleted files shrink and fade out, renames slide to the new position.
- Bottom bar: Play/Pause, speed (1x, 4x, 16x), and a scrubber across the whole date range. Scrubbing rebuilds the state at that commit quickly (precompute snapshots every 100 commits).
- Overlay in a corner: current date, commit number / total, author, and the commit message, with the last 5 messages fading upward.
- Small live stats panel: total files alive, commits so far, most-changed file so far.
- Keyboard: Space play/pause, Left/Right step one commit, Home/End jump to start/end.

Robustness:
- Works on a fresh repo with 1 commit and on a large repo (cap at --max-commits, keep 60 fps by drawing only changed regions or batching).
- Binary or huge paths are fine; never read file contents, only history.

Ship it with a README that shows how to run it on its own repo, plus a sample output generated from this project's history.

When done, explain the data flow (git log -> parser -> JSON -> canvas), the layout choice, and 3 ideas for using an LLM later (for example, auto-generating chapter titles for phases of the project).
```

## Success Criteria
- Running the tool on any local repo produces one HTML file that opens offline with no console errors.
- Playback visibly shows files appearing, changing and disappearing, and the overlay date and message stay in sync with the commits.
- The scrubber jumps to any point in history in under a second on a repo with ~1,000 commits.
- Renames move a dot instead of creating a duplicate, and --hide-authors removes every real name from the output.
- Running it on its own repo after a few commits gives a time-lapse you would happily screenshot.

## Optional Extensions
- Add an "Export GIF/WebM" button using MediaRecorder on the canvas.
- Color by author instead of extension, with a toggle.
- Add a "chapters" mode: send batches of commit messages to an LLM (OpenAI-compatible endpoint + key you provide) and show generated chapter titles on the timeline.
- Draw faint lines between files that are frequently changed in the same commit to reveal hidden coupling.
