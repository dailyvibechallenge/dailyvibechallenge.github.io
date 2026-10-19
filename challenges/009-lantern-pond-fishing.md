---
date: 2026-10-19
---
# #009 — Lantern Pond: A Cozy Night-Fishing Game with a Field Journal
**Difficulty:** Beginner · **Time:** 2–3 hours · **Theme:** Cozy games

## Description
Build a calm little night-fishing game for the browser. You sit at the edge of a lantern-lit pond, cast your line, wait for a gentle tug, and play a forgiving one-button reel minigame to land one of a dozen whimsical fish. Every new catch is sketched into a field journal that fills up over time, and the pond changes with an in-game clock and weather. There is no fail state and no timer pressure, just a cozy loop you can finish in an afternoon and keep polishing for weeks.

## Starter Prompt
```
Build "Lantern Pond", a cozy single-page night-fishing game. Use one index.html with vanilla JS and an HTML5 Canvas (CSS for UI panels). No external libraries, CDNs, images or network calls: draw everything with canvas shapes and gradients, and generate any sound with the Web Audio API.

Scene:
- A 960x540 canvas (scaled to fit the window, crisp on high-DPI) showing a dark-blue pond at night, a wooden dock at the bottom, reeds at the edges, a moon with a soft reflection, and 3-5 floating paper lanterns that bob slowly and cast warm glow circles on the water.
- Gentle animated ripples and drifting fireflies. Keep the palette soft: deep navy, teal, warm amber and cream.
- An in-game clock (1 real minute = 1 game hour, from 8 PM to 4 AM, then loops) shown as a small moon icon. Weather rolls every in-game 2 hours: Clear, Mist (fog layer) or Drizzle (falling rain streaks and ring ripples).

Core loop:
1. Cast: hold Space (or press and hold the mouse/touch) to charge a power meter, release to cast. The bobber lands farther with more power; show a small splash.
2. Wait: after a random 3-10 seconds the bobber dips twice (a "nibble") then sinks (a "bite"). Pressing too early during a nibble only scares the fish away with a friendly message, never a penalty.
3. Reel: on a bite, show a vertical meter with a moving fish icon and a player "catch zone" bar. Hold Space/mouse to lift the zone, release to let it fall. Keep the fish inside the zone to fill a progress ring; outside drains it slowly. Fill it to land the fish. Difficulty scales gently per fish (fish speed and zone size), and the easiest fish should be catchable by a 7-year-old.
4. Catch card: show the fish drawn with simple shapes, its name, a one-line cozy flavor text, its size in cm (random within its range) and whether it is a new journal entry or a new size record.

Fish data:
- Define 12 fish in one JS array: id, name, color palette, size range, rarity (common/uncommon/rare), allowed hours, allowed weather, flavor text. Examples: "Lantern Minnow" (common, any time), "Moonlit Koi" (rare, Clear only, 11 PM-2 AM), "Fog Eel" (uncommon, Mist only), "Puddle Pike" (uncommon, Drizzle only), "Dawn Perch" (rare, 3-4 AM only).
- Pick the bite fish by weighted random from fish that match the current hour and weather.

Field journal (press J or tap the book icon):
- A grid of 12 cards. Uncaught fish show a silhouette and a hint ("Seen near the reeds when the fog rolls in"). Caught fish show their drawing, best size, times caught and first-caught game time.
- Show progress "7 / 12 discovered" and a small reward when all 12 are found (the lanterns change color and a shooting star appears).

Feel and accessibility:
- Soft sound effects made with Web Audio: plop on cast, tiny bell on bite, rising chime on catch. A mute toggle (M) saved to localStorage.
- A relaxing ambient loop (quiet filtered noise for water plus occasional cricket chirps) that starts only after the first user interaction.
- Save the journal, records and settings in localStorage. Add a "Reset journal" button with a confirm step.
- Full keyboard, mouse and touch support. Respect prefers-reduced-motion by reducing ripples and firefly movement.
- 60 fps with requestAnimationFrame, delta-time based movement, and no console errors.

When done, explain the game loop structure, how the fish table and weighted spawn logic work, and give 3 ideas for adding an AI model later (for example, generating fresh flavor text for each catch).
```

## Success Criteria
- Opening index.html shows an animated night pond with lanterns, ripples and fireflies, and the game clock advances.
- You can cast, wait for a nibble and bite, and land a fish with the hold-and-release reel minigame on keyboard, mouse and touch.
- At least 12 fish exist, and some only appear at certain hours or in certain weather, so the journal takes more than one sitting to complete.
- The field journal shows silhouettes and hints for unknown fish, and real stats for caught fish, and it survives a page reload.
- Nothing punishes the player: a missed bite or a lost fish just gives a friendly message and lets you cast again.

## Optional Extensions
- Add a tiny shop where you trade fish for cosmetic bobbers, lantern colors or a cat that sits on the dock and reacts to catches.
- Let an LLM write a fresh two-line journal entry for each catch, with a cached fallback so the game works offline.
- Add seasons that rotate every few in-game nights with new fish and decorations.
- Export your journal as a shareable PNG postcard drawn on an offscreen canvas.
