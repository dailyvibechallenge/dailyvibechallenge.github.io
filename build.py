#!/usr/bin/env python3
"""Zero-dependency static site builder for Daily Vibe Challenge.
Reads challenges/NNN-slug.md (optional front matter: date, description) -> _site/."""
import html, json, os, re, shutil, datetime, subprocess

SITE = "https://dailyvibechallenge.github.io"
NAME = "Daily Vibe Challenge"
TAGLINE = "Daily AI vibe-coding challenges with copy-paste starter prompts for Claude Code, Cursor, Replit Agent and Lovable."
EMAIL = "dailyvibe@mail.grokbot.com"
REPO = "https://github.com/dailyvibechallenge/dailyvibechallenge.github.io"
SUBMIT = REPO + "/issues/new?template=submit-build.yml"
STATS = {"challenges": None, "subscribers": "0 (just launched)", "bluesky": "new account", "launched": "October 2026"}
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "_site")
esc = html.escape

def inline(t):
    t = esc(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*(?!\s)(.+?)\*", r"<em>\1</em>", t)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+|/[^)\s]*)\)", r'<a href="\2">\1</a>', t)
    return t

def md(text, prompt_section=None):
    """Tiny markdown: headings, paragraphs, lists, fenced code. Code inside
    the 'Starter Prompt' section gets a copy button."""
    out, lines, i, section, para, lst = [], text.split("\n"), 0, "", [], None
    def flush():
        nonlocal para, lst
        if para: out.append("<p>" + inline(" ".join(para)) + "</p>"); para = []
        if lst: out.append(f"<{lst[0]}>" + "".join(f"<li>{inline(x)}</li>" for x in lst[1]) + f"</{lst[0]}>"); lst = None
    while i < len(lines):
        l = lines[i]
        if l.startswith("```"):
            flush(); i += 1; buf = []
            while i < len(lines) and not lines[i].startswith("```"): buf.append(lines[i]); i += 1
            code = esc("\n".join(buf))
            if section.lower().startswith("starter prompt"):
                out.append('<div class="prompt"><button class="copy" type="button" data-copy>Copy prompt</button>'
                           f'<pre id="prompt"><code>{code}</code></pre></div>')
            else:
                out.append(f"<pre><code>{code}</code></pre>")
        elif m := re.match(r"(#{1,6})\s+(.*)", l):
            flush(); n = min(len(m.group(1)) + 1, 6); section = m.group(2).strip()
            sid = re.sub(r"[^a-z0-9]+", "-", section.lower()).strip("-")
            out.append(f'<h{n} id="{sid}">{inline(section)}</h{n}>')
        elif m := re.match(r"\s*[-*]\s+(.*)", l):
            if para: flush()
            if not lst or lst[0] != "ul": flush(); lst = ["ul", []]
            lst[1].append(m.group(1))
        elif m := re.match(r"\s*\d+[.)]\s+(.*)", l):
            if para: flush()
            if not lst or lst[0] != "ol": flush(); lst = ["ol", []]
            lst[1].append(m.group(1))
        elif not l.strip(): flush()
        else:
            if lst: flush()
            para.append(l.strip())
        i += 1
    flush()
    return "\n".join(out)

def git_date(path):
    try:
        d = subprocess.run(["git", "log", "--diff-filter=A", "--format=%cs", "-1", "--", path],
                           cwd=ROOT, capture_output=True, text=True).stdout.strip()
        if d: return d
    except Exception: pass
    return datetime.date.today().isoformat()

def load():
    items = []
    d = os.path.join(ROOT, "challenges")
    for fn in sorted(os.listdir(d)):
        m = re.match(r"(\d+)-([a-z0-9-]+)\.md$", fn)
        if not m: continue
        raw = open(os.path.join(d, fn), encoding="utf-8").read()
        fm = {}
        if raw.startswith("---\n"):
            head, _, raw = raw[4:].partition("\n---\n")
            for ln in head.splitlines():
                if ":" in ln: k, v = ln.split(":", 1); fm[k.strip()] = v.strip().strip('"')
        body = raw.strip() + "\n"
        tm = re.search(r"^#\s+(.*)$", body, re.M)
        full_title = tm.group(1).strip() if tm else fn
        title = re.sub(r"^#?\d+\s*[—–-]\s*", "", full_title)
        meta = {}
        mm = re.search(r"^\*\*Difficulty:\*\*.*$", body, re.M)
        if mm:
            for part in mm.group(0).split("·"):
                kv = re.match(r"\s*\*\*(.+?):\*\*\s*(.*)", part)
                if kv: meta[kv.group(1).lower()] = kv.group(2).strip()
        dm = re.search(r"## Description\s*\n+(.+?)(\n\n|\n#|$)", body, re.S)
        desc = fm.get("description") or (re.sub(r"\s+", " ", dm.group(1)).strip() if dm else TAGLINE)
        pm = re.search(r"## Starter Prompt\s*\n+```[^\n]*\n(.*?)\n```", body, re.S)
        items.append(dict(num=m.group(1), slug=f"{m.group(1)}-{m.group(2)}", title=title, full_title=full_title,
            date=fm.get("date") or git_date(f"challenges/{fn}"), difficulty=meta.get("difficulty", ""),
            time=meta.get("time", ""), theme=meta.get("theme", ""), description=desc,
            prompt=pm.group(1) if pm else "", body=body))
    items.sort(key=lambda c: (c["date"], c["num"]), reverse=True)
    return items

CSS = """:root{--bg:#fbfaf7;--fg:#1d1d1f;--mut:#61646b;--card:#fff;--line:#e6e3dc;--acc:#5b3df5;--code:#f3f1ec}
@media(prefers-color-scheme:dark){:root{--bg:#0f1013;--fg:#e9e9ec;--mut:#9a9ca5;--card:#17181d;--line:#2a2c33;--acc:#a594ff;--code:#1d1f25}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.6 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
a{color:var(--acc)}.wrap{max-width:760px;margin:0 auto;padding:0 18px}
header.site{border-bottom:1px solid var(--line)}header.site .wrap{display:flex;gap:16px;align-items:center;justify-content:space-between;padding:14px 18px;flex-wrap:wrap}
.brand{font-weight:800;text-decoration:none;color:var(--fg)}.brand span{color:var(--acc)}nav a{margin-left:14px;color:var(--mut);text-decoration:none}nav a:hover{color:var(--fg)}
main{padding:28px 0 48px}h1{line-height:1.2;font-size:2rem;margin:.2em 0}h2{margin-top:1.8em}
.meta{color:var(--mut);font-size:.92rem}.tag{display:inline-block;border:1px solid var(--line);border-radius:99px;padding:1px 10px;margin:2px 4px 2px 0;font-size:.85rem}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px 22px;margin:16px 0}.hero h2{margin:.2em 0;font-size:1.6rem}.hero h2 a{color:var(--fg);text-decoration:none}
.btn{display:inline-block;background:var(--acc);color:#fff;border:0;border-radius:10px;padding:9px 16px;font:inherit;font-weight:600;text-decoration:none;cursor:pointer}
@media(prefers-color-scheme:dark){.btn,.copy{color:#0f1013!important}}
pre{background:var(--code);border:1px solid var(--line);border-radius:10px;padding:14px;overflow:auto;font-size:.88rem;line-height:1.5;white-space:pre-wrap}
code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}.prompt{position:relative}.copy{position:absolute;top:8px;right:8px;background:var(--acc);color:#fff;border:0;border-radius:8px;padding:6px 12px;font-weight:600;cursor:pointer}
.prompt pre{padding-top:46px}ul.list{list-style:none;padding:0}ul.list li{padding:10px 0;border-bottom:1px solid var(--line)}
table{border-collapse:collapse;width:100%;font-size:.95rem}td,th{text-align:left;padding:8px 6px;border-bottom:1px solid var(--line)}
.newsletter{border-style:dashed}input[type=email]{font:inherit;padding:8px 10px;border-radius:8px;border:1px solid var(--line);background:var(--bg);color:var(--fg);min-width:220px}
footer{border-top:1px solid var(--line);color:var(--mut);font-size:.9rem;padding:20px 0 40px}"""

JS = """document.addEventListener('click',async e=>{const b=e.target.closest('[data-copy]');if(!b)return;
const t=b.parentElement.querySelector('pre').innerText;try{await navigator.clipboard.writeText(t)}catch(_){const a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();document.execCommand('copy');a.remove()}
const o=b.textContent;b.textContent='Copied ✓';setTimeout(()=>b.textContent=o,1600)});"""

NEWSLETTER = f"""<section class="card newsletter" id="newsletter">
<h2 style="margin-top:0">⚡ Get tomorrow's challenge before everyone else</h2>
<p class="meta">One fresh challenge + copy-paste starter prompt in your inbox every morning, plus a weekly roundup of the best community builds. Free, no spam, unsubscribe in one click.</p>
<form action="https://buttondown.com/api/emails/embed-subscribe/dailyvibe" method="post" target="popupwindow" onsubmit="window.open('https://buttondown.com/dailyvibe','popupwindow')" style="display:flex;gap:8px;flex-wrap:wrap">
<input type="email" name="email" id="bd-email" placeholder="you@example.com" aria-label="Email address" required>
<input type="hidden" value="1" name="embed"><button class="btn" type="submit">Subscribe</button></form>
<p class="meta">Or follow on <a href="https://bsky.app/profile/dailyvibechallenge.bsky.social">Bluesky</a> · <a href="/feed.xml">RSS/Atom</a> · <a href="https://buttondown.com/dailyvibe/archive">Newsletter archive</a></p>
</section>"""

def page(path, title, desc, body, jsonld=None, og_type="website", md_alt=None):
    url = SITE + path
    ld = "".join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in (jsonld or []))
    alt = f'<link rel="alternate" type="text/markdown" href="{md_alt}">' if md_alt else ""
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}"><link rel="canonical" href="{url}">
<meta name="color-scheme" content="light dark"><link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⚡</text></svg>">
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{NAME}"><meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{SITE}/og.png"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}">
<link rel="alternate" type="application/atom+xml" title="{NAME}" href="/feed.xml">{alt}
<style>{CSS}</style>{ld}</head><body>
<header class="site"><div class="wrap"><a class="brand" href="/">Daily <span>Vibe</span> Challenge</a>
<nav><a href="/archive/">Archive</a><a href="/roundup/">Roundup</a><a href="/topics/">Topics</a><a href="/showcase/">Showcase</a><a href="/sponsor/">Sponsor</a><a href="/about/">About</a><a href="/#newsletter" class="btn" style="color:#fff;padding:5px 12px">Subscribe</a></nav></div></header>
<main class="wrap">{body}</main>
<footer><div class="wrap">© {NAME} · <a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="/llms.txt">llms.txt</a> · <a href="/challenges.json">JSON</a> · No trackers.</div></footer>
<script>{JS}</script></body></html>"""

def tags(c):
    return "".join(f'<span class="tag">{esc(x)}</span>' for x in (c["difficulty"], c["time"], c["theme"]) if x)

def write(rel, content):
    p = os.path.join(OUT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(content)


TOPICS = [
    {
        "slug": "agents",
        "title": "AI Agents & Tool Use",
        "meta": "AI agent coding challenges and tool-use vibe coding prompts — build inspectable agents, research desks, and LLM NPCs.",
        "blurb": "Build agents you can actually understand: tool loops, research desks, and LLM-powered NPCs inside fair game engines.",
        "keywords": ("agent", "tool use", "text adventure"),
    },
    {
        "slug": "games",
        "title": "Games & Play",
        "meta": "Vibe coding game project ideas — cozy idle games, pixel art jams, and tiny multiplayer browser games with starter prompts.",
        "blurb": "Ship playable browser games in an afternoon: cozy idle loops, pixel dungeon dashes, and cross-tab multiplayer duels.",
        "keywords": ("game", "pixel", "multiplayer", "cozy"),
    },
    {
        "slug": "prototyping",
        "title": "Rapid Prototyping & Toys",
        "meta": "Rapid prototyping and tech-toy vibe coding challenges — napkin specs to clickable prototypes, git visualizations, and browser toys.",
        "blurb": "Go from idea to demo fast: clickable phone prototypes from plain text, git history time-lapses, and microphone-powered browser toys.",
        "keywords": ("prototyp", "dev tool", "tech toy"),
    },
]

def topic_matches(c, topic):
    t = (c.get("theme") or "").lower()
    return any(k in t for k in topic["keywords"])

def iso_week_key(date_str):
    y, m, d = map(int, date_str.split("-"))
    iso = datetime.date(y, m, d).isocalendar()
    return f"{iso.year}-w{iso.week:02d}", iso

def week_label(week_key, dates):
    """Human range from challenge dates in the week, e.g. Oct 14–18, 2026."""
    ds = sorted(datetime.date.fromisoformat(d) for d in dates)
    a, b = ds[0], ds[-1]
    if a.year == b.year and a.month == b.month:
        return f"{a.strftime('%b')} {a.day}–{b.day}, {a.year}"
    if a.year == b.year:
        return f"{a.strftime('%b')} {a.day} – {b.strftime('%b')} {b.day}, {a.year}"
    return f"{a.strftime('%b')} {a.day}, {a.year} – {b.strftime('%b')} {b.day}, {b.year}"


def main():
    shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
    cs = load()
    website_ld = {"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": SITE + "/", "description": TAGLINE,
                  "publisher": {"@type": "Organization", "name": NAME, "email": EMAIL}}
    # challenge pages
    for c in cs:
        path = f"/challenges/{c['slug']}/"
        body_md = re.sub(r"^#\s+.*\n", "", c["body"], count=1)
        body_md = re.sub(r"^\*\*Difficulty:\*\*.*\n", "", body_md, count=1, flags=re.M)
        ld = {"@context": "https://schema.org", "@type": "HowTo", "name": c["full_title"], "description": c["description"],
              "url": SITE + path, "datePublished": c["date"], "inLanguage": "en",
              "author": {"@type": "Organization", "name": NAME}, "publisher": {"@type": "Organization", "name": NAME},
              "educationalLevel": c["difficulty"], "keywords": f"vibe coding, AI coding challenge, {c['theme']}",
              "tool": [{"@type": "HowToTool", "name": n} for n in ("Claude Code", "Cursor", "Replit Agent", "Lovable")],
              "step": [{"@type": "HowToStep", "name": "Copy the starter prompt", "text": c["prompt"][:4000]},
                       {"@type": "HowToStep", "name": "Paste it into your AI coding agent and iterate", "text": "Run the prompt in Claude Code, Cursor, Replit Agent or Lovable and iterate until the success criteria pass."}]}
        body = f"""<article><p class="meta">Challenge #{c['num']} · <time datetime="{c['date']}">{c['date']}</time></p>
<h1>{esc(c['title'])}</h1><p>{tags(c)}</p>{md(body_md)}
<section class="card"><strong>Built it?</strong> Share your build and get featured in the <a href="/showcase/">showcase</a> &amp; weekly roundup: <a class="btn" href="{SUBMIT}">Submit your build →</a></section>
<p class="meta">Plain markdown: <a href="/challenges/{c['slug']}.md">{c['slug']}.md</a></p></article>{NEWSLETTER}"""
        write(f"challenges/{c['slug']}/index.html", page(path, f"#{c['num']} {c['title']} — {NAME}", c["description"], body, [ld], "article", f"/challenges/{c['slug']}.md"))
        write(f"challenges/{c['slug']}.md", c["body"])
    # home
    if cs:
        t = cs[0]
        hero = f"""<section class="card hero"><p class="meta">Latest challenge · #{t['num']} · {t['date']}</p>
<h2><a href="/challenges/{t['slug']}/">{esc(t['title'])}</a></h2><p>{tags(t)}</p><p>{esc(t['description'])}</p>
<div class="prompt"><button class="copy" type="button" data-copy>Copy prompt</button><pre><code>{esc(t['prompt'])}</code></pre></div>
<p><a class="btn" href="/challenges/{t['slug']}/">Open full challenge →</a></p></section>"""
    else: hero = "<p>No challenges yet.</p>"
    recent = "".join(f'<li><a href="/challenges/{c["slug"]}/">#{c["num"]} {esc(c["title"])}</a><br><span class="meta">{c["date"]} · {esc(c["difficulty"])} · {esc(c["theme"])}</span></li>' for c in cs[1:8])
    home = f"""<h1>A new AI vibe-coding challenge every day</h1><p class="meta">{esc(TAGLINE)}</p><p><a class="btn" href="#newsletter">Get it daily by email — free</a> &nbsp;<a href="{SUBMIT}">Submit a build</a></p>{hero}
{('<h2>Recent challenges</h2><ul class="list">' + recent + '</ul><p><a href="/archive/">Full archive →</a></p>') if recent else ''}{NEWSLETTER}"""
    write("index.html", page("/", f"{NAME} — daily AI vibe-coding challenges & starter prompts", TAGLINE, home, [website_ld]))
    # archive
    rows = "".join(f'<tr><td>{c["num"]}</td><td>{c["date"]}</td><td><a href="/challenges/{c["slug"]}/">{esc(c["title"])}</a></td><td>{esc(c["difficulty"])}</td><td>{esc(c["theme"])}</td></tr>' for c in cs)
    write("archive/index.html", page("/archive/", f"Archive — all challenges — {NAME}", f"All {len(cs)} Daily Vibe Challenges: AI agents, games, tech and rapid prototyping prompts.",
        f'<h1>Archive</h1><div style="overflow-x:auto"><table><thead><tr><th>#</th><th>Date</th><th>Title</th><th>Difficulty</th><th>Theme</th></tr></thead><tbody>{rows}</tbody></table></div>',
        [{"@context": "https://schema.org", "@type": "CollectionPage", "name": "Archive", "url": SITE + "/archive/"}]))
    # about
    about = f"""<h1>About</h1><p><strong>{NAME}</strong> publishes one bite-sized AI vibe-coding challenge every day — AI agents, games, tech and rapid prototyping.</p>
<p>Each challenge comes with a copy-paste <strong>starter prompt</strong> that works in Claude Code, Cursor, Replit Agent, Lovable or any capable coding agent, plus success criteria and optional extensions.</p>
<h2>How to play</h2><ol><li>Open today's challenge.</li><li>Click <em>Copy prompt</em> and paste it into your AI coding tool.</li><li>Iterate until the success criteria pass, then try an extension.</li></ol>
<h2>For AI agents</h2><p>Machine-readable: <a href="/llms.txt">/llms.txt</a>, <a href="/llms-full.txt">/llms-full.txt</a>, <a href="/challenges.json">/challenges.json</a>, and a raw <code>.md</code> for every challenge.</p>
<h2>Contact</h2><p><a href="mailto:{EMAIL}">{EMAIL}</a></p><p class="meta">This site uses no cookies, analytics or trackers.</p>{NEWSLETTER}"""
    write("about/index.html", page("/about/", f"About — {NAME}", f"What {NAME} is and how to use the daily starter prompts.", about))
    # sponsor
    sponsor = f"""<h1>Sponsor Daily Vibe Challenge</h1>
<p>Reach builders who ship with AI every day: developers, indie hackers and makers who use Claude Code, Cursor, Replit Agent, Lovable, Bolt and v0 to turn prompts into working agents, games and prototypes.</p>
<h2>Audience (live numbers)</h2><table><tbody>
<tr><td>Challenges published</td><td>{len(cs)} (one new challenge every day)</td></tr>
<tr><td>Newsletter subscribers</td><td>{STATS['subscribers']}</td></tr>
<tr><td>Bluesky</td><td>{STATS['bluesky']}</td></tr>
<tr><td>Launched</td><td>{STATS['launched']}</td></tr></tbody></table>
<p class="meta">We're early and honest about it: numbers above are updated from real metrics, never inflated. Founding sponsors get launch pricing locked in.</p>
<h2>Placements</h2><ul>
<li><strong>Presented-by challenge</strong> — "Today's challenge is built with &lt;your tool&gt;": the starter prompt is written for your product, with a logo + link on the challenge page, newsletter and social post.</li>
<li><strong>Newsletter sponsor slot</strong> — one short text ad (50–80 words + link) at the top of the daily email.</li>
<li><strong>Weekly roundup sponsor</strong> — top slot in the weekly "best builds" email and page.</li>
<li><strong>Challenge week / game jam</strong> — a themed 5–7 day series with prizes or credits for the best community builds.</li></ul>
<h2>Rates</h2><p>Rates TBD — founding-sponsor pricing available. Email <a href="mailto:{EMAIL}?subject=Sponsorship">{EMAIL}</a> with your product and dates.</p>
<p class="meta">Sponsored content is always labelled. We only feature tools our readers can actually build with.</p>{NEWSLETTER}"""
    write("sponsor/index.html", page("/sponsor/", f"Sponsor — {NAME}", "Sponsor a daily AI vibe-coding challenge: reach developers and makers building with Claude Code, Cursor, Replit, Lovable, Bolt and v0.", sponsor))
    # showcase
    showcase = f"""<h1>Showcase</h1><p>Built something from a challenge? Share it — the best builds are featured here, in the weekly roundup email and on Bluesky.</p>
<p><a class="btn" href="{SUBMIT}">Submit your build →</a></p>
<h2>How to submit</h2><ol><li>Finish (or half-finish!) any challenge from the <a href="/archive/">archive</a>.</li>
<li>Open the <a href="{SUBMIT}">submission form</a> (free GitHub account) — add the challenge number, a demo or repo link, the AI tool you used and a screenshot.</li>
<li>Or post in <a href="{REPO}/discussions">GitHub Discussions</a>, tag <strong>#DailyVibeChallenge</strong> on Bluesky, or email <a href="mailto:{EMAIL}?subject=My%20build">{EMAIL}</a>.</li></ol>
<h2>Featured builds</h2><p class="meta">No featured builds yet — yours could be the first. See <a href="{REPO}/issues?q=label%3Asubmission">all submissions</a>.</p>{NEWSLETTER}"""
    write("showcase/index.html", page("/showcase/", f"Showcase — community builds — {NAME}", "Community builds from Daily Vibe Challenge: AI agents, games and prototypes made with copy-paste starter prompts.", showcase))
    # weekly roundups
    weeks = {}
    for c in cs:
        wk, _ = iso_week_key(c["date"])
        weeks.setdefault(wk, []).append(c)
    roundup_urls = []
    for wk, items in sorted(weeks.items(), reverse=True):
        items_asc = sorted(items, key=lambda c: (c["date"], c["num"]))
        label = week_label(wk, [c["date"] for c in items_asc])
        title = f"Week in Vibes — {label}"
        desc = f"Weekly roundup of {len(items_asc)} Daily Vibe Challenges ({label}): AI agents, games, prototyping and tech toys with copy-paste starter prompts."
        lis = "".join(
            f'<li><a href="/challenges/{c["slug"]}/">#{c["num"]} {esc(c["title"])}</a> '
            f'<span class="tag">{esc(c["theme"])}</span><br>'
            f'<span class="meta">{esc(c["description"][:180] + ("…" if len(c["description"]) > 180 else ""))}</span></li>'
            for c in items_asc
        )
        body = f"""<article>
<p class="meta">Weekly roundup · ISO week {esc(wk)}</p>
<h1>{esc(title)}</h1>
<p>A full week of bite-sized AI vibe-coding challenges — each with a copy-paste starter prompt for Claude Code, Cursor, Replit Agent or Lovable. Here's everything we shipped this week.</p>
<h2>This week's challenges</h2>
<ul class="list">{lis}</ul>
<h2>Showcase</h2>
<p class="meta">No community builds submitted yet this week. Be the first — finish any challenge and <a href="{SUBMIT}">submit your build</a> to get featured here and in next Sunday's roundup.</p>
<p><a class="btn" href="{SUBMIT}">Submit your build →</a></p>
<h2>Tool tip of the week</h2>
<p>Paste the starter prompt straight into <strong>Claude Code</strong> or <strong>Cursor</strong> Agent chat, then iterate against the success criteria section. Keep the prompt file open beside your editor so you can tweak constraints without rewriting from scratch.</p>
</article>{NEWSLETTER}"""
        path = f"/roundup/{wk}/"
        write(f"roundup/{wk}/index.html", page(path, f"{title} — {NAME}", desc, body,
            [{"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "url": SITE + path,
              "description": desc, "isPartOf": {"@type": "WebSite", "name": NAME, "url": SITE + "/"}}]))
        roundup_urls.append((path, items_asc[-1]["date"], wk, label, len(items_asc)))
    # roundup index
    rrows = "".join(
        f'<li><a href="{u}">Week in Vibes — {esc(lab)}</a><br><span class="meta">{n} challenges · {esc(wk)}</span></li>'
        for u, _d, wk, lab, n in roundup_urls
    )
    write("roundup/index.html", page("/roundup/", f"Week in Vibes roundups — {NAME}",
        "Weekly roundups of Daily Vibe Challenge: every AI vibe-coding challenge of the week, plus community builds and a tool tip.",
        f'<h1>Week in Vibes</h1><p class="meta">Sunday roundups of the week\'s challenges, showcase builds, and one tool tip.</p><ul class="list">{rrows or "<li>No roundups yet.</li>"}</ul>{NEWSLETTER}',
        [{"@context": "https://schema.org", "@type": "CollectionPage", "name": "Week in Vibes roundups", "url": SITE + "/roundup/"}]))
    # topic hubs
    topic_urls = []
    for topic in TOPICS:
        matched = [c for c in cs if topic_matches(c, topic)]
        matched = sorted(matched, key=lambda c: (c["date"], c["num"]), reverse=True)
        lis = "".join(
            f'<li><a href="/challenges/{c["slug"]}/">#{c["num"]} {esc(c["title"])}</a><br>'
            f'<span class="meta">{c["date"]} · {esc(c["difficulty"])} · {esc(c["theme"])}</span><br>'
            f'{esc(c["description"][:200] + ("…" if len(c["description"]) > 200 else ""))}</li>'
            for c in matched
        ) or '<li class="meta">No challenges in this topic yet — check back soon.</li>'
        path = f"/topics/{topic['slug']}/"
        body = f"""<article>
<h1>{esc(topic["title"])}</h1>
<p>{esc(topic["blurb"])}</p>
<p class="meta">{len(matched)} challenge{"s" if len(matched) != 1 else ""} · <a href="/topics/">All topics</a></p>
<ul class="list">{lis}</ul>
</article>{NEWSLETTER}"""
        write(f"topics/{topic['slug']}/index.html", page(path, f"{topic['title']} — {NAME}", topic["meta"], body,
            [{"@context": "https://schema.org", "@type": "CollectionPage", "name": topic["title"], "url": SITE + path,
              "description": topic["meta"], "about": topic["title"],
              "isPartOf": {"@type": "WebSite", "name": NAME, "url": SITE + "/"}}]))
        topic_urls.append((path, topic, len(matched)))
    tlis = "".join(
        f'<li><a href="{u}">{esc(t["title"])}</a><br><span class="meta">{n} challenge{"s" if n != 1 else ""} · {esc(t["blurb"])}</span></li>'
        for u, t, n in topic_urls
    )
    write("topics/index.html", page("/topics/", f"Topics — vibe coding challenge hubs — {NAME}",
        "Browse Daily Vibe Challenge by topic: AI agents, games, rapid prototyping and tech toys. Long-tail vibe coding project ideas with starter prompts.",
        f'<h1>Topics</h1><p class="meta">Browse challenges by theme — great if you\'re hunting for a weekend project idea.</p><ul class="list">{tlis}</ul>{NEWSLETTER}',
        [{"@context": "https://schema.org", "@type": "CollectionPage", "name": "Topics", "url": SITE + "/topics/"}]))
    shutil.copy(os.path.join(ROOT, "static", "og.png"), os.path.join(OUT, "og.png"))
    shutil.copy(os.path.join(ROOT, "static", "googlebf1cb2597616669f.html"), os.path.join(OUT, "googlebf1cb2597616669f.html"))
    # 404
    write("404.html", page("/404.html", f"Not found — {NAME}", "Page not found.", '<h1>Not found</h1><p><a href="/">Go to today\'s challenge →</a></p>'))
    # feed (Atom)
    now = (cs[0]["date"] if cs else datetime.date.today().isoformat()) + "T00:00:00Z"
    entries = "".join(f"""<entry><title>{esc('#'+c['num']+' '+c['title'])}</title><link href="{SITE}/challenges/{c['slug']}/"/><id>{SITE}/challenges/{c['slug']}/</id>
<updated>{c['date']}T00:00:00Z</updated><summary>{esc(c['description'])}</summary><content type="html">{esc(md(c['body']))}</content></entry>""" for c in cs[:30])
    write("feed.xml", f"""<?xml version="1.0" encoding="utf-8"?><feed xmlns="http://www.w3.org/2005/Atom"><title>{NAME}</title><subtitle>{esc(TAGLINE)}</subtitle>
<link href="{SITE}/"/><link rel="self" href="{SITE}/feed.xml"/><id>{SITE}/</id><updated>{now}</updated><author><name>{NAME}</name></author>{entries}</feed>""")
    # sitemap / robots
    urls = [("/", now[:10]), ("/archive/", now[:10]), ("/roundup/", now[:10]), ("/topics/", now[:10]), ("/about/", now[:10]), ("/sponsor/", now[:10]), ("/showcase/", now[:10])]
    urls += [(u, d) for u, d, *_ in roundup_urls]
    urls += [(u, now[:10]) for u, _t, _n in topic_urls]
    urls += [(f"/challenges/{c['slug']}/", c["date"]) for c in cs]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
          "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{d}</lastmod></url>" for u, d in urls) + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    # agent files
    write("challenges.json", json.dumps({"name": NAME, "url": SITE + "/", "challenges": [
        {k: c[k] for k in ("num", "slug", "title", "date", "difficulty", "time", "theme", "description", "prompt")} |
        {"url": f"{SITE}/challenges/{c['slug']}/", "markdown_url": f"{SITE}/challenges/{c['slug']}.md"} for c in cs]}, indent=2, ensure_ascii=False))
    write("llms.txt", f"# {NAME}\n\n> {TAGLINE}\n\nOne new challenge per day: AI agents, games, tech and rapid prototyping. Each has a description, a copy-paste starter prompt, success criteria and optional extensions. Contact: {EMAIL}\n\n"
          f"## Challenges\n\n" + "".join(f"- [#{c['num']} {c['title']}]({SITE}/challenges/{c['slug']}.md): {c['date']} · {c['difficulty']} · {c['theme']}. {c['description']}\n" for c in cs) +
          f"\n## Roundups\n\n- [Week in Vibes index]({SITE}/roundup/)\n" +
          "".join(f"- [Week in Vibes — {lab}]({SITE}{u})\n" for u, _d, wk, lab, n in roundup_urls) +
          f"\n## Topics\n\n- [Topics index]({SITE}/topics/)\n" +
          "".join(f"- [{t['title']}]({SITE}{u})\n" for u, t, n in topic_urls) +
          f"\n## Machine-readable\n\n- [All challenges in one markdown file]({SITE}/llms-full.txt)\n- [JSON index]({SITE}/challenges.json)\n- [Atom feed]({SITE}/feed.xml)\n\n## Optional\n\n- [About]({SITE}/about/)\n- [Archive]({SITE}/archive/)\n")
    write("llms-full.txt", f"# {NAME} — all challenges\n\n> {TAGLINE}\n\n" + "\n\n---\n\n".join(f"<!-- {SITE}/challenges/{c['slug']}/ · {c['date']} -->\n{c['body']}" for c in cs))
    write(".nojekyll", "")
    print(f"Built {len(cs)} challenges -> {OUT}")

if __name__ == "__main__":
    main()
