---
date: 2026-10-14
---
# #001 — Cozy Plant Shop Idle Game
**Difficulty:** Beginner · **Time:** 1–2 hours · **Theme:** Cozy games

## Description
A tiny browser idle game: you run a plant shop, water pots, plants grow through 4 pixel-art stages, and you sell them for coins to buy new seeds and pots. Calm palette, soft sounds optional.

## Starter Prompt
```
Build a single-page cozy idle game called "Little Leaf Shop" using plain HTML, CSS and JavaScript (no build step, one index.html is fine).

Core loop:
- A 3x3 grid of pots. Each pot is empty, or holds a plant with a growth stage 0–3.
- Clicking an empty pot plants a seed (costs 5 coins). Start with 20 coins.
- Clicking a planted pot waters it. A watered plant advances one stage every 8 seconds; it needs watering again after each stage.
- At stage 3 the plant is "ready"; clicking it sells it for 15 coins.
- Show coins, plants sold, and a "Buy pot" button that unlocks extra pots (up to 16) at rising cost.

Style:
- Draw plants as CSS/canvas pixel art (16x16 scaled up, image-rendering: pixelated), with a warm pastel palette (#f4e7d3, #9cc5a1, #49a078, #216869, #1f2421).
- Gentle hover/bounce animations. Readable on mobile.
- Persist state in localStorage so progress survives reloads.

Keep the code in clearly separated sections (state, render, input, persistence) with short comments. When done, tell me how to run it and list any assumptions.
```

## Success Criteria
- Plant, water, grow, sell loop works end to end.
- Coins and pot purchases update correctly; no negative coins.
- Progress persists after a page reload.
- Looks consistent and cozy on desktop and phone.

## Optional Extensions
- Multiple seed types with different grow times and prices.
- Day/night tint cycle and a lo-fi ambient sound toggle.
- Offline progress: plants keep growing while the tab is closed.
