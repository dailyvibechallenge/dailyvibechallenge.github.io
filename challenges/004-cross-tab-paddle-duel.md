---
date: 2026-10-14
---
# #004 — Cross-Tab Paddle Duel
**Difficulty:** Beginner · **Time:** 1–3 hours · **Theme:** Simple multiplayer

## Description
Build a two-player Pong-style duel where each player lives in their own browser tab and the tabs sync in real time with the BroadcastChannel API. No server, no accounts: open two windows side by side and play. It is a tiny, honest intro to host authority, state sync and lag handling.

## Starter Prompt
```
Build "Paddle Duel", a two-player Pong-style game where each player plays in a separate browser tab on the same machine. Use a single index.html plus game.js, vanilla JS and HTML5 Canvas, no build step and no server. Tabs communicate only through the BroadcastChannel API (channel name "paddle-duel").

Networking model:
- The first tab to open becomes HOST; the next becomes GUEST. Implement a tiny handshake: on load, post {type:"hello", id}; if no "host-here" reply arrives within 300ms, become host. A third tab becomes a SPECTATOR that only renders.
- The host is authoritative: it runs physics at a fixed 60Hz step and broadcasts a compact state snapshot {ball:{x,y,vx,vy}, paddles:[y1,y2], score:[a,b], tick} every tick.
- The guest only sends its input {type:"input", up, down, tick} and renders the latest snapshot, interpolating the ball between the last two snapshots.
- Handle disconnects: on "beforeunload" post {type:"bye"}; if the host disappears (no snapshot for 1s), the guest promotes itself to host and keeps the score.

Gameplay:
- 800x500 canvas, paddles on left (host) and right (guest), W/S or Up/Down to move.
- Ball speeds up 5% on each paddle hit and bounces at an angle based on where it hits the paddle.
- First to 7 wins; show a "Rematch" button that both players must click (ready-check over the channel).

UI:
- Top bar shows your role (HOST, GUEST or SPECTATOR), both scores, and a live "ping" in ms measured with timestamped ping/pong messages every second.
- A debug toggle (press D) that overlays tick number, snapshot rate and the last message received.

Keep the code clean with small functions (net.js-style section, physics section, render section) and explain how to test it: open index.html in two windows side by side. When done, list any edge cases you handled.
```

## Success Criteria
- Opening two tabs auto-assigns HOST and GUEST without any manual setup; a third tab becomes a spectator.
- Both tabs show the same ball position and score with no visible desync.
- Closing the host tab lets the guest take over within about a second without losing the score.
- Rematch only starts after both players click it.
- Works offline from a local file or any static host.

## Optional Extensions
- Swap BroadcastChannel for a WebSocket relay (about 30 lines of Node) so two different computers can play.
- Add artificial latency and packet loss sliders to the debug overlay to see interpolation in action.
- Power-ups (bigger paddle, split ball) spawned deterministically from a shared seed.
- An AI paddle that fills in when only one tab is open.
