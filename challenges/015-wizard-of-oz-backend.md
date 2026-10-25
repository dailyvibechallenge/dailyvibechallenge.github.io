---
date: 2026-10-25
---
# #015 — Wizard-of-Oz Backend: Prototype Any App Against an API That an AI Fakes on the Fly
**Difficulty:** Intermediate · **Time:** 2–3 hours · **Theme:** Rapid prototyping

## Description
The slowest part of prototyping an app is usually the backend you have not built yet. Today you build a tiny mock server that answers any REST request your frontend makes by asking an AI to invent a believable JSON response, shaped by a one-paragraph description of the app and an optional schema. It remembers what it made up, so a POST to /todos really shows up in the next GET, and every response can be frozen into a fixture file once you like it. Point a throwaway frontend at it and you can click through a "real" app in minutes, then swap in the real API later without touching the UI.

## Starter Prompt
```
Build "Wizard-of-Oz Backend", a local mock API server for rapid prototyping. Node.js 18+ with no dependencies (built-in http, fs, fetch). Files: server.js, oz.config.json, a fixtures/ folder, a demo/ folder with a tiny frontend, and README.md.

How it works
- `node server.js` listens on port 4010 and accepts ANY method and path under /api (e.g. GET /api/recipes, GET /api/recipes/42, POST /api/recipes, DELETE /api/recipes/42). Enable CORS for every origin so any local frontend can call it.
- oz.config.json holds: "app" (one paragraph describing the app, e.g. "a recipe box for busy parents"), optional "schemas" (resource name -> example object or field list), "latencyMs" (simulated delay), and "llm" settings (OpenAI-compatible baseUrl, model, and the env var name that holds the API key; never write keys to disk or logs).
- For each request the server first checks fixtures/<METHOD>_<path>.json; if a fixture exists it is returned as-is. Otherwise it asks the LLM for a response: send the app description, the schema for that resource, the method, path, query, request body, and the current in-memory state for that resource; require strict JSON back (validate with JSON.parse, retry once with the parse error, then fall back).
- Offline fallback: if no API key is set, generate plausible data locally from the schema (field names like name, email, price, date, imageUrl get sensible fake values) so the project works with zero setup.

Memory (what makes it feel real)
- Keep an in-memory store per resource. Generated lists are saved, so the same GET returns the same items. POST adds an item with a new id, PUT/PATCH updates it, DELETE removes it, and later GETs reflect all of that. Ids stay consistent between list and detail routes.
- `?_reset=1` on any request clears that resource; `POST /_oz/reset` clears everything.

Freezing and inspecting
- `POST /_oz/freeze` writes every response served so far into fixtures/ so the prototype becomes deterministic and works offline.
- `GET /_oz` serves a small HTML dashboard: a live log of requests (method, path, status, source = fixture / llm / fallback, ms), a button to freeze one response, and the current store as pretty JSON.
- Honor an `X-Oz-Status` request header (e.g. 500 or 404) to simulate errors, and add the configured latency to every response.

Demo
- demo/index.html: a single-page "recipe box" that lists, views, adds and deletes recipes using only fetch calls to http://localhost:4010/api. It must work against the fake backend with no code that knows it is fake.

Quality bar: server.js under ~400 lines, no crashes on malformed JSON or unknown routes, and a test.js (node test.js) with at least 8 checks covering fixture precedence, POST-then-GET persistence, DELETE, reset, the X-Oz-Status header and the offline fallback generator.

When done, show a short session log (create, list, delete a recipe), explain how the store keeps the AI's invented data consistent, and note which prompt instruction most reduced invalid JSON.
```

## Success Criteria
- Any request under /api gets a believable JSON response, from a fixture if one exists, otherwise from the LLM or the offline fallback.
- POST, PUT/PATCH and DELETE change what later GET requests return, and list and detail routes agree on ids.
- Freezing writes fixtures that are then served on the next request, so the demo works with the network off.
- The /_oz dashboard shows each request with its source and timing, and X-Oz-Status plus latency simulation work.
- The demo recipe app lists, views, adds and deletes recipes without any knowledge that the backend is fake, and node test.js passes.

## Optional Extensions
- Export an OpenAPI file inferred from all the traffic so far, as a starting spec for the real backend.
- "Chaos mode" that randomly adds latency spikes, empty lists and 500s to test loading and error states.
- Record and replay mode: proxy to a real API when it exists and fall back to the wizard for routes that do not.
- Let an AI agent build a second frontend (e.g. a mobile layout) against the frozen fixtures and report any endpoint it wished existed.
