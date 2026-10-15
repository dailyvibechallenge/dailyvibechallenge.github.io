---
date: 2026-10-15
---
# #005 — The Lighthouse Keeper: A Text Adventure with an Agent NPC
**Difficulty:** Intermediate · **Time:** 2–4 hours · **Theme:** Text adventures with agents

## Description
Build a small parser text adventure set in a storm-battered lighthouse where the one character you meet, the old keeper, is an LLM agent. The twist: the game engine owns the truth. The keeper can only change the world through a few typed tools (give an item, unlock a door, reveal a clue), so the conversation feels free-form while the puzzle stays fair, winnable and impossible to talk your way around.

## Starter Prompt
```
Build "The Lighthouse Keeper", a short browser text adventure with one LLM-powered NPC. Use a single index.html plus engine.js and keeper.js, vanilla JS, no build step. The game must also run with NO API key using a scripted fallback keeper (see below).

World and engine (engine.js, fully deterministic, the single source of truth):
- 6 rooms: Shore, Keeper's Cottage, Lighthouse Base, Spiral Stairs, Lamp Room, Cellar. Each room has a description, exits and items.
- Items: lantern, oil can, brass key, logbook, matches, fuse. Inventory limit of 4.
- Parser verbs: look, go <dir>/n/s/e/w/up/down, take, drop, use <item> [on <thing>], inventory, talk <message> (or say "..."), help. Unknown input gets a helpful hint, never a crash.
- Goal: relight the lamp before the ship offshore runs aground. A turn counter (40 turns) is the storm clock; show it in the status bar.
- Puzzle chain: the Cellar is locked (brass key), the lamp needs oil + a fuse + matches, and the fuse's location is only written in the logbook, which the keeper holds.

The keeper agent (keeper.js):
- The player talks to the keeper with "talk ..." when in the Cottage. Send the LLM a system prompt with his persona (gruff, superstitious, secretly kind), the current visible game state, the last 8 exchanges, and a strict tool list:
  give_item(item), unlock(door), reveal_clue(clue_id), refuse(reason).
- Ask the model for JSON: {"say": "...", "tool_calls": [{"name": "...", "args": {...}}]}. Validate every call against the engine: he can only give items he actually holds, only unlock doors he has keys for, and only reveal clues from a fixed list (clue ids: "fuse_location", "cellar_key", "storm_lore"). Rejected calls are dropped and logged, never applied.
- Conditions the engine enforces (not the model): he hands over the logbook only after the player brings him the lantern, and gives the brass key only after the player asks about the cellar. The model can decide WHEN and HOW he says it, not whether the rules apply.
- Config: an API key field stored in localStorage and an OpenAI-compatible endpoint + model name field. Handle errors and timeouts by falling back to the scripted keeper for that turn.
- Scripted fallback: keyword matching (cellar, key, lantern, logbook, fuse, storm, ship) with a few canned lines per topic that call the same tools, so the game is fully completable offline.

UI:
- Dark terminal look: scrolling transcript, input line with command history (Up/Down arrows), status bar with room, turns left and inventory.
- Keeper lines in a different color. A "Debug" toggle shows the raw JSON from the model and any rejected tool calls.
- Save/load to localStorage; a "New game" button.

When done, explain how the engine/agent boundary works, list the tool validation rules, and give a walkthrough that wins in under 30 turns.
```

## Success Criteria
- The game is winnable start to finish with no API key, using the scripted keeper.
- With a key set, the keeper responds in character and his item hand-offs actually show up in your inventory.
- Trying to sweet-talk him ("just give me the fuse", "ignore your rules") never breaks the puzzle; invalid tool calls appear in the debug panel and are not applied.
- The storm clock runs out correctly and shows a lose screen; relighting the lamp in time shows a win screen.
- Save, reload the page, load: you are in the same room with the same inventory and turn count.

## Optional Extensions
- Give the keeper memory across saves: a short summary of what the player told him, rewritten by the model each conversation.
- Add a second agent NPC (a ghostly sailor in the Lamp Room) who only speaks in riddles and can reveal one clue.
- Generate fresh room descriptions each playthrough with the LLM while keeping exits and items fixed by the engine.
- Write a tiny test script that plays the walkthrough against the engine and asserts a win.
