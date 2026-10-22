---
date: 2026-10-22
---
# #012 — Sprite Style Linter: Snap Messy AI Sprites onto One Palette and Pixel Grid
**Difficulty:** Intermediate · **Time:** 2–3 hours · **Theme:** Pixel-art consistency

## Description
AI image models are great at pixel-art ideas and terrible at pixel-art rules: every sprite comes back at a different fake resolution, with blurry anti-aliased edges, 200 near-identical colors and a light source that wanders. Build a browser tool that fixes that. Drop in a batch of sprites, and it detects each image's real pixel size, snaps it back onto a clean grid, quantizes it to one shared palette, checks outlines and lighting against a style sheet, and shows a lint report with one-click fixes plus a side-by-side sprite sheet so you can see the whole set finally look like it belongs in one game.

## Starter Prompt
```
Build "Sprite Style Linter", a browser tool that makes a batch of inconsistent (often AI-generated) pixel-art sprites follow one shared style. Single index.html plus app.js and style.css, vanilla JS and HTML5 Canvas (2D, imageSmoothingEnabled = false everywhere), no build step, no frameworks, no server, no external network calls. Everything runs locally on the user's images.

Input:
- Drag-and-drop or file picker for multiple PNG/JPG/WebP images. Also a "Load demo set" button that generates 6 deliberately messy test sprites in code (different upscale factors like 7x and 9.5x, JPEG-style noise, anti-aliased edges, slightly-off colors, one with a bottom-right light source) so the tool can be tested with no files.
- Each image becomes a card in a left sidebar with thumbnail, file name and a lint score (0-100).

Style sheet (right panel, saved to localStorage, exportable/importable as style.json):
- Target sprite size: 16x16, 24x24 or 32x32 (default 16).
- Palette: pick a preset (PICO-8 16 colors, a 4-color GB green, or "Auto: build an N-color palette from the whole batch" with N = 8..32 using median-cut on all images combined). Show swatches; allow editing a color with a color input and locking it.
- Outline rule: none | 1px darkest-palette-color outline | 1px outline darker than the neighbouring fill (selective outline).
- Light direction: top-left | top | top-right.
- Max colors per sprite (default 8). Transparent background required: yes/no.

Processing pipeline per image (each step is its own pure function with a short comment, so it can be unit tested):
1. Background removal: if the image has no alpha, treat the most common border color (within a tolerance) as background and make it transparent.
2. Fake-resolution detection: estimate the real pixel size by measuring run lengths of identical-ish colors along rows and columns and taking the most common block width (allow non-integer scales like 9.5). Show the detected scale and confidence.
3. Grid snap: downsample to the logical grid by taking the dominant (mode) color in each cell, not the average, so edges stay crisp. Then crop to the content bounding box and center it on the target canvas size (scale down with mode-sampling if it is too big, never smooth).
4. Palette quantization: map each pixel to the nearest palette color using a perceptual distance (convert to OKLab), with an optional ordered-dither toggle that is OFF by default.
5. Cleanup: remove orphan pixels (single pixels that differ from all 4 neighbours), and remove anti-alias halo pixels on the transparent edge.
6. Outline: apply the chosen outline rule.

Lint report (per sprite, recalculated live):
- Rules with pass/warn/fail and a one-line explanation: wrong size, off-palette colors (count), too many colors, semi-transparent pixels, missing or broken outline (gaps), orphan pixels, light-direction mismatch (estimate from average luminance of the top-left vs bottom-right half of the non-outline pixels), and "looks upscaled/blurry" if scale detection confidence is low.
- Each failing rule has a "Fix" button that applies only that step, and there is a "Fix all" for the sprite and "Fix whole batch".
- Lint score = 100 minus weighted penalties; show it on the card and color the card.

Views:
- Center: before/after for the selected sprite at 1x and at a large integer zoom (8x) with an optional pixel-grid overlay, plus a highlight mode that outlines the exact pixels breaking a rule in red.
- "Sheet" tab: all fixed sprites side by side on one background color at 1x, 2x and 4x so inconsistencies jump out; toggle between original and fixed for the whole sheet.
- Palette usage bar: how many pixels of each palette color the batch uses.

Export:
- Download each fixed sprite as PNG at 1x and an optional chosen integer scale, a packed sprite sheet PNG, a sheet.json (name, x, y, w, h for each sprite), and the style.json. Bundle into a zip with a tiny self-written STORE-only zip writer (no library).

Quality bar: no console errors, processing a batch of 20 images at up to 1024x1024 takes under 3 seconds (use OffscreenCanvas or a Web Worker if needed), keyboard accessible, total code under ~1000 lines. Add a tests.html that runs the pure functions against small hand-made pixel arrays and prints pass/fail.

When done, explain how the fake-resolution detection works and where it fails, why mode-sampling beats averaging for pixel art, why OKLab distance gives better palette matches than RGB distance, and list the three rules that most improved how consistent the demo set looks.
```

## Success Criteria
- The demo set (or your own AI-generated sprites) goes from a mismatched mess to a sprite sheet that clearly shares one size, one palette, crisp edges and consistent outlines.
- Scale detection recovers the true logical size of a sprite that was upscaled by a non-integer factor (for example 9.5x) and reports its confidence.
- Every pixel in exported sprites is either fully transparent or an exact palette color, verified by the linter itself (score 100 on rules for palette and transparency).
- Individual "Fix" buttons apply only their own step, and the before/after view with red highlights makes each rule's effect visible.
- Exported zip contains PNGs, a sheet PNG, sheet.json and style.json that re-import correctly.

## Optional Extensions
- "Style from reference": drop in one sprite you love and auto-derive the palette, outline rule and light direction from it.
- Add a prompt helper that turns the style sheet into a reusable text prompt block for your image model (size, palette hex codes, outline, lighting) so future generations start closer to the target.
- Animation check: load a strip of frames and lint for frame-to-frame jitter (moving outline pixels, palette flicker, bounding-box wobble).
- Command-line version in Node that lints a whole folder in CI and fails the build if any sprite scores below 90.
