---
date: 2026-10-18
---
# #008 — Whistle Lamp: A Browser Toy You Control with Claps and Whistles
**Difficulty:** Beginner · **Time:** 1–2 hours · **Theme:** Tech toys

## Description
Build a playful browser toy that listens through your microphone and drives a glowing virtual lamp with sound alone. Clap twice to switch it on or off, whistle high or low to sweep the color around the rainbow, and hum louder to make it brighter. It runs entirely in the browser with the Web Audio API, needs no server or account, and is the kind of tiny tech toy you can show a friend in ten seconds.

## Starter Prompt
```
Build "Whistle Lamp", a single-page browser toy that controls a virtual lamp using only sound from the microphone. Use one index.html file with vanilla JS and CSS, the Web Audio API (getUserMedia + AnalyserNode), and no external libraries, CDNs or network calls. All audio stays on the device.

Start screen:
- A big "Start listening" button (browsers require a user gesture before audio starts). Explain in one line that audio never leaves the device.
- If microphone permission is denied or unavailable, show a friendly message and enable "Keyboard mode" (C = clap, Up/Down = whistle pitch, Shift = volume) so the toy still works.

The lamp:
- A large centered lamp (CSS or Canvas) with a soft radial glow on a dark background. State: on/off, hue (0-360), brightness (0-1).
- Smoothly animate every change (ease hue and brightness over ~150 ms; never jump).
- When off, show a dim outline of the bulb.

Sound controls:
1. Double clap toggles the lamp. Detect a clap as a sharp transient: short-term RMS jumps above ~3x the rolling background level, then decays within ~100 ms. Two claps 150-600 ms apart = toggle. Ignore single claps and long noises. Add a 1 s cooldown after a toggle.
2. Whistle sets the color. Detect a whistle as a strong, narrow peak in the frequency data between ~500 Hz and ~3,000 Hz (peak at least ~20 dB above the median band level, held for 150 ms+). Map the pitch on a log scale to hue: low whistle = red, high whistle = violet. Keep the last color when the whistle stops.
3. Loudness sets brightness while humming or talking: map smoothed RMS (with an adjustable noise floor) to brightness between 0.2 and 1.0.

Debug panel (toggle with D):
- Live level meter with the background noise line, the detected peak frequency in Hz, a mini spectrum bar chart, and a log of the last 5 detected events ("double clap", "whistle 1,240 Hz").
- Sliders for clap sensitivity, whistle sensitivity and noise floor, saved to localStorage.

Polish:
- A tiny "pop" visual on each detected clap and a color trail ring while whistling.
- Works on desktop Chrome, Firefox and Safari, and on mobile (handle AudioContext resume on tap).
- Runs at 60 fps with requestAnimationFrame; analysis uses an FFT size of 2048.

When done, explain how clap and whistle detection work in plain words, which thresholds you tuned and why, and 3 ideas for using an AI model later (for example, recognizing spoken color names on-device).
```

## Success Criteria
- Opening index.html and pressing Start asks for the mic once, and the debug meter visibly reacts to sound.
- Two quick claps toggle the lamp reliably, while a single clap, talking or a door slam does not.
- Whistling low then high sweeps the lamp color from warm to cool, and the color holds after the whistle stops.
- Denying the microphone still leaves a working toy in Keyboard mode with no console errors.
- A friend can figure out how to use it within 10 seconds from the on-screen hints.

## Optional Extensions
- Connect a real smart bulb or an LED strip on an ESP32 over Web Serial or Web Bluetooth so the physical light follows the virtual one.
- Add "party mode": the lamp pulses to the beat of music detected through the mic.
- Let users record a short sound pattern (like three knocks) as a custom trigger.
- Add on-device speech commands ("blue", "dim", "off") with the Web Speech API where it is available.
