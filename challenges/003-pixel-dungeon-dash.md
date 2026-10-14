---
date: 2026-10-14
---
# #003 — One-Room Pixel Dungeon Dash
**Difficulty:** Intermediate · **Time:** 2–4 hours · **Theme:** Mini game jam / pixel art consistency

## Description
A single-screen roguelite: dodge slimes, grab the key, reach the door before a 60-second timer runs out. Each run randomizes the layout. Focus on a strict, consistent pixel-art style.

## Starter Prompt
```
Create a browser game "Dungeon Dash" with HTML5 Canvas and vanilla JS (or Phaser 3 via CDN), single index.html plus one game.js.

Gameplay:
- 16x12 tile room, 16px tiles, rendered at 3x scale with no smoothing.
- Player moves with WASD/arrows on a tile grid with smooth tweening.
- Randomly place walls (keep a guaranteed path via BFS check), 1 key, 1 locked door, and 3–6 slimes that move one tile every 0.5s toward the player with simple pathing.
- Touching a slime = lose a heart (3 hearts, 1s invulnerability flash). Grab key, reach door = win; timer hits 0 = lose.
- Show hearts, timer, and best time (localStorage). Press R to restart with a new layout.

Art rules (enforce strictly):
- Generate all sprites in code from small string-art arrays, using ONE 8-color palette defined once at the top.
- Every sprite 16x16, 1px dark outline, light source top-left.
- 2-frame idle animation for player and slimes.

Also add simple Web Audio beeps for pickup, hit, win and lose. Explain the code structure when done.
```

## Success Criteria
- Every generated layout is solvable.
- Collisions, hearts, timer, win/lose and restart all work.
- All visuals share one palette and the same outline/lighting rules.
- Runs at a steady 60fps in a modern browser.

## Optional Extensions
- Multiple rooms with increasing slime count.
- Daily seed so everyone plays the same layout today.
- An AI "ghost" that plays the level with A* and races you.
