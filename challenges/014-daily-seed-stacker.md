---
date: 2026-10-24
---
# #014 — Daily Seed Stacker: A One-Button Tower Game with a Shareable Daily Score
**Difficulty:** Beginner · **Time:** 1–2 hours · **Theme:** Mini game jam

## Description
Jam rules for today: one button, one screen, one evening. Build a one-button stacking game where a block slides back and forth and you tap to drop it on the tower; whatever overhangs gets sliced off, so every miss makes the next drop harder. The twist that makes it sticky: every player in the world gets the same block speeds and colors each day from a date-based seed, and when the tower falls you get a Wordle-style emoji result to paste into chat. Small scope, real game feel (screen shake, slice particles, perfect-drop streaks) and a built-in reason to come back tomorrow.

## Starter Prompt
```
Build "Daily Seed Stacker", a one-button browser stacking game. Single index.html with game.js and style.css, vanilla JS + Canvas 2D, no frameworks, no build step, no server, no external assets (draw everything, make sound with the Web Audio API).

Core loop
- A block slides left and right above the tower. Space, click or tap drops it. The part that overhangs the block below is sliced off and falls away with a little spin; the part that overlaps stays and becomes the new top. Miss completely and the run ends.
- A "perfect" drop (overlap within 3 px) snaps exactly into place, keeps full width, and builds a streak; every 3rd perfect in a row grows the block back by 10%.
- Speed ramps up gently with height. The camera scrolls up smoothly as the tower grows. Mobile-friendly: whole canvas is the button, works in portrait.

Daily seed (the twist)
- Seed a small deterministic PRNG (e.g. mulberry32) from today's UTC date string "YYYY-MM-DD". The seed controls each block's slide speed, start side and color palette, so everyone plays the identical tower today.
- Daily mode counts: one official attempt per day stored in localStorage (best score, streak of days played). After it, unlimited "practice" runs with a random seed, clearly labeled.
- Add a ?date=YYYY-MM-DD URL parameter to replay any past day (unofficial), useful for testing determinism.

Share result
- On game over show: height, perfect drops, best perfect streak, and a share text like:
  Daily Seed Stacker 2026-10-24
  Height 23 · Perfect 7
  🟩🟩🟨🟩🟥...
  where each emoji is one drop (🟩 perfect, 🟨 good, 🟥 big slice), max 30 emoji, wrapped at 10 per line.
- Copy button using navigator.clipboard with a textarea fallback. Show a "next tower in hh:mm:ss" countdown to UTC midnight.

Game feel (keep it small but juicy)
- Short screen shake scaled by slice size, a few slice particles, a rising pitch "plink" for each perfect in a streak, a thud on miss. Mute toggle remembered in localStorage.
- Title screen with "Tap to start", game-over screen with share card, and a soft pastel palette that shifts with height.

Quality bar: 60 fps on a mid-range phone, no console errors, game.js under ~500 lines, and a tests.html with at least 8 assertions covering the PRNG (same date gives same sequence), the slice math (overlap, perfect snap, full miss) and the share-text formatter.

When done, explain how the daily seed guarantees two players get the same tower, show a sample share text from a real run, and list which game-feel effect made the biggest difference.
```

## Success Criteria
- One input (space, click or tap) plays the whole game on desktop and mobile, and overhangs are sliced off correctly with perfect drops snapping into place.
- The same date always produces the same block speeds, start sides and colors (verified in tests.html and with ?date=), and daily mode allows one official attempt per day.
- Game over shows a copyable emoji share text with date, height and perfect count, plus a countdown to the next tower.
- Screen shake, slice particles and streak sounds work, with a mute toggle that persists.
- No console errors, no external assets, runs by just opening index.html.

## Optional Extensions
- Ghost tower: replay your best run from today as a faint outline behind the current tower.
- Weekly themed seeds (ice blocks that slide farther, wobbly jelly blocks) chosen by the date.
- A 60-second "jam timer" mode that scores how high you get before time runs out.
- Let an AI agent tune the difficulty curve: run 1,000 simulated drops with a noisy bot and adjust speed ramp until the median height lands around 20.
