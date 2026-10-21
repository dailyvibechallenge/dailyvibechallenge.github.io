---
date: 2026-10-21
---
# #011 — Doodle Duel: A Peer-to-Peer Draw-and-Guess Game with No Server
**Difficulty:** Intermediate · **Time:** 2–4 hours · **Theme:** Simple multiplayer

## Description
Build a two-player draw-and-guess game that runs directly between two browsers over a WebRTC data channel, with no game server and no accounts. Players connect by swapping a short invite code (copy-paste or QR), then take turns: one draws a secret word against a 60-second timer while the other types guesses, and strokes stream live to the guesser. It is a hands-on intro to peer-to-peer networking, manual signaling, message protocols and turn-based state sync, and it works across two phones on the same Wi-Fi.

## Starter Prompt
```
Build "Doodle Duel", a two-player draw-and-guess game that runs peer-to-peer between two browsers using a WebRTC RTCDataChannel. Single index.html plus app.js and style.css, vanilla JS and HTML5 Canvas, no build step, no frameworks, and no game server. The only external network use allowed is a public STUN server (stun:stun.l.google.com:19302) for ICE.

Connection (manual signaling, no server):
- Home screen with two buttons: "Host a game" and "Join a game".
- Host: create an RTCPeerConnection and a data channel named "doodle" (ordered: true). Create an offer, wait until ICE gathering is complete (iceGatheringState === "complete", with a 3 s fallback), then show the full localDescription as an invite code: JSON -> compress with CompressionStream("deflate-raw") -> base64url. Show it in a read-only textarea with a Copy button and as a QR code (draw the QR with a small self-written or inlined MIT QR encoder; no CDN).
- Guest: paste the invite code (or open a link with it in the URL hash, e.g. #offer=...), decode it, set it as remote description, create an answer, wait for ICE gathering, and show the answer code the same way.
- Host pastes the answer code. When the channel opens, both screens switch to the lobby and show "Connected" plus measured round-trip time (ping/pong every 2 s, show a rolling average).
- A "Same-device test" link opens a second tab and does the whole handshake automatically via BroadcastChannel, so the game can be tested on one machine. Keep this path clearly separate from the real P2P path.

Message protocol (JSON over the data channel, every message has {t, seq}):
- hello {name, version}; ping {ts}; pong {ts}
- round-start {round, drawer, wordLength, endsAt} (the word itself is sent only to the drawer's own UI, never over the wire to the guesser)
- stroke {id, color, size, points:[[x,y],...]} with coordinates normalized to 0..1 so different screen sizes match; batch points and send at most every 50 ms
- clear {}; undo {strokeId}
- guess {text}; guess-result {text, correct, closeness} where closeness is "cold" | "warm" | "hot" based on edit distance
- round-end {round, word, guessedBy, scores}
- Ignore unknown message types and log them, so either peer can be updated without breaking the other.

Authority and turns:
- The host owns the game state: word list, timer, scores and turn order. The guest only sends strokes (when drawing), guesses and ready signals.
- Use a built-in list of at least 80 simple, drawable words in 3 difficulty tiers. The drawer picks one of three offered words.
- 60-second rounds, 6 rounds total, alternate drawer each round. Correct guess: guesser gets points based on time left, drawer gets a flat bonus. Show a final scoreboard and a "Rematch" button.
- Timer is based on the host clock: the host sends endsAt, and the guest corrects for clock offset estimated from ping/pong.

Drawing UI:
- Canvas with pointer events (mouse, touch and pen), 6 colors, 3 brush sizes, Undo and Clear. Smooth lines with quadratic curves between points.
- The guesser's canvas is read-only and redraws incoming strokes live as they arrive.
- Guess box with a chat-like history; correct guesses flash and lock the box until the next round.

Robustness:
- Detect disconnects (channel close, or no pong for 6 s), show a "Peer disconnected" banner, and offer "Back to home".
- Sanitize and length-limit all incoming text (guesses and names max 40 chars) and render with textContent only.
- Responsive layout that works on two phones in portrait.

Quality bar: no console errors, works in current Chrome, Firefox and Safari, keyboard accessible controls, total code under ~900 lines.

When done, explain how manual WebRTC signaling works (offer, answer, ICE candidates), why the host is authoritative, why coordinates are normalized, and list what you would need to add (a TURN server or a tiny signaling relay) for players on different networks.
```

## Success Criteria
- Two browsers on the same network connect by swapping invite codes (copy-paste or QR), with no game server involved, and show "Connected" with a live round-trip time.
- The drawer's strokes appear on the guesser's screen within a fraction of a second, at the right scale even on different screen sizes.
- Rounds, timer, word choice, scoring and turn alternation work for a full 6-round game, ending in a scoreboard with Rematch.
- The secret word is never sent to the guesser before the round ends (check the data channel messages in the console).
- Closing one tab shows a clear disconnect banner on the other instead of a frozen game.

## Optional Extensions
- Add spectators: the host relays the stroke stream to a third peer with its own invite code.
- Replay: record every stroke with timestamps and play the whole game back at 4x speed at the end.
- Add an "AI guesser" mode where an image model tries to guess the drawing and competes with the human.
- Add a tiny WebSocket signaling relay (under 50 lines) so players can join with a 4-letter room code instead of pasting codes.
