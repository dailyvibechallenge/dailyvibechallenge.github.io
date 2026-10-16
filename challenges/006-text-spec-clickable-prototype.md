---
date: 2026-10-16
---
# #006 — Napkin Spec: Turn Plain Text into a Clickable Phone Prototype
**Difficulty:** Beginner · **Time:** 1–3 hours · **Theme:** Rapid prototyping

## Description
Build a tiny prototyping tool where you type an app idea as a few lines of indented plain text and instantly get a clickable phone mockup beside it. Screens, buttons, lists and inputs render live, buttons jump between screens, and the whole prototype lives in the URL so you can share it with one link. It is the fastest possible loop from "what if the app did this?" to something a friend can tap through on their phone.

## Starter Prompt
```
Build "Napkin Spec", a browser tool that turns a short indented text spec into a live, clickable phone prototype. Use a single index.html plus app.js and style.css, vanilla JS, no build step, no backend, no external libraries.

Layout:
- Left half: a monospace textarea editor with line numbers. Right half: a phone frame (about 390x780, rounded corners, notch) that renders the current screen.
- Re-render on every keystroke (debounced ~150 ms). Parse errors show inline under the editor with the line number, and the last valid render stays visible.

Spec language (document it in a Help panel):
- "# Screen Name" starts a screen. The first screen is the start screen.
- Lines inside a screen are components, one per line:
  title: Some heading
  text: A paragraph of text
  button: Label -> Other Screen        (tapping navigates to that screen)
  input: Placeholder text
  list: Item one, Item two, Item three  (each item may use "-> Screen" to navigate)
  image: a short caption               (render a grey placeholder box with the caption)
  tabs: Home, Search, Profile           (bottom tab bar; each tab navigates to the screen of the same name)
  back                                 (a back arrow in the header using navigation history)
- Comments start with //. Blank lines are ignored. Indentation is optional.
- Validate links: a "-> Missing Screen" shows a warning in the error panel and the button gets a dashed red outline.

Prototype behavior:
- Tapping buttons/list items/tabs navigates with a quick slide transition; keep a history stack for back.
- A screen picker dropdown above the phone jumps to any screen. A "Restart" button returns to the start screen.
- "Flow map" toggle: replace the phone with a simple SVG graph of screens as boxes and links as arrows (auto-layout in a grid is fine).

Sharing and saving:
- Encode the spec into the URL hash (base64 of UTF-8 text, compressed with CompressionStream if available, plain base64 fallback). Loading a URL with a hash restores it.
- "Copy share link" button. Autosave to localStorage too.
- "Present" mode: hide the editor and center the phone full screen, so the link works as a demo on a real phone.

Ship it with a built-in example spec for a 4-screen coffee-ordering app (Menu, Item Detail, Cart, Order Placed) that shows off every component type.

When done, explain the parser design, list the spec syntax, and suggest 3 ways an LLM could plug in later (e.g. generating a spec from a one-sentence idea).
```

## Success Criteria
- Typing the example spec from scratch updates the phone live with no page reload and no console errors.
- Every button, list item and tab in the example navigates to the right screen, and back returns along the real history.
- A broken link ("-> Nowhere") shows a clear warning with its line number instead of crashing.
- Copying the share link, opening it in a private window, shows the exact same prototype.
- Present mode on a real phone (or device emulation) is tappable and looks like an app, not a web page.

## Optional Extensions
- Add an "Idea to spec" box: send one sentence to an LLM (OpenAI-compatible endpoint + key in localStorage) and paste the generated spec into the editor.
- Export the current prototype as a single self-contained HTML file.
- Add light/dark themes and an accent color line in the spec, like "theme: dark, #ff6b35".
- Record taps in Present mode and show a heatmap of where testers clicked.
