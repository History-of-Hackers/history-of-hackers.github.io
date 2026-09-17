#!/usr/bin/env python3
"""Restore the canonical static person-page shell for generated person pages."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "people" / "marcus-hutchins-wannacry.html"
ISSUES_URL = "https://github.com/History-of-Hackers/history-of-hackers.github.io/issues/new"


def esc(value):
    return html.escape(str(value), quote=True)


def article(data):
    timeline = "".join(
        f'<li><span class="t-date">{esc(item["date"])}</span><span>{esc(item["event"])}</span></li>'
        for item in data.get("timeline", [])
    )
    sources = "".join(
        f'<li><a href="{esc(source["url"])}" target="_blank" rel="noopener noreferrer">{esc(source["title"])}</a></li>'
        for source in data.get("sources", [])
    )
    details = [
        ("Type", "Person"), ("Era", data.get("era", "")),
    ]
    if data.get("born"):
        details.append(("Born", data["born"]))
    if data.get("died"):
        details.append(("Died", data["died"]))
    if data.get("knownFor"):
        details.append(("Known for", "; ".join(data["knownFor"])))
    if data.get("tags"):
        details.append(("Tags", ", ".join(data["tags"])))
    infobox = "".join(f"<dt>{esc(label)}</dt><dd>{esc(value)}</dd>" for label, value in details)
    created_by = data.get("editorial", {}).get("createdBy") or "the History of Hackers community"
    credit = (
        f'<div class="page-credit">Created by <strong>{esc(created_by)}</strong> &middot; Something wrong or want it removed? '
        f'<a href="{ISSUES_URL}" target="_blank" rel="noopener noreferrer">Open an issue</a>.</div>'
    )
    return f'''\n<div class="breadcrumbs"><a href="../">Home</a> &raquo; <a href="./">People</a> &raquo; {esc(data["title"])}</div>
<article class="entity">
<div class="entity-layout">
<div>
<h1>{esc(data["title"])}</h1>
<div class="why-matters">{esc(data.get("whyThisMatters", ""))}</div>
<div id="tocSlot"></div>
<div class="entity-content">{data["sections"]["overview"]}<h2>Timeline</h2><ul class="timeline-list">{timeline}</ul></div>
<div class="sources"><h2>Sources</h2><ol>{sources}</ol></div>
</div>
<div><div class="infobox"><div class="infobox-title">{esc(data["title"])}</div><dl>{infobox}</dl></div></div>
</div>
{credit}
</article>
'''


canonical = CANONICAL.read_text()
main_open = '<main class="content" id="main">'
start = canonical.index(main_open) + len(main_open)
end = canonical.rindex("\n</main>")
head = canonical[:start]
tail = canonical[end:]
manifest = json.loads((ROOT / "data" / "manifest.json").read_text())
fixed = []

for entry in manifest:
    if entry.get("type") != "person":
        continue
    page = ROOT / entry["url"]
    existing = page.read_text()
    if 'aside class="sidebar desktop-only"' in existing:
        continue
    data = json.loads((ROOT / "data" / "people" / f'{entry["slug"]}.json').read_text())
    title = f'{data["title"]} - History of Hackers'
    description = data["summary"]
    url = f'https://historyofhackers.org/people/{data["slug"]}.html'
    ld = json.dumps({"@context": "https://schema.org", "@type": "Person", "name": data["name"], "description": description})
    page_head = re.sub(r'<title>.*?</title>', f'<title>{esc(title)}</title>', head, count=1, flags=re.S)
    page_head = re.sub(r'<meta name="description" content=".*?" />', f'<meta name="description" content="{esc(description)}" />', page_head, count=1)
    page_head = re.sub(r'<link rel="canonical" href=".*?" />', f'<link rel="canonical" href="{url}" />', page_head, count=1)
    page_head = re.sub(r'<meta property="og:title" content=".*?" />', f'<meta property="og:title" content="{esc(title)}" />', page_head, count=1)
    page_head = re.sub(r'<meta property="og:description" content=".*?" />', f'<meta property="og:description" content="{esc(description)}" />', page_head, count=1)
    page_head = re.sub(r'<meta property="og:url" content=".*?" />', f'<meta property="og:url" content="{url}" />', page_head, count=1)
    ld_tag = f'<script type="application/ld+json">\n{ld}\n</script>'
    page_head = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda _: ld_tag, page_head, count=1, flags=re.S)
    page.write_text(page_head + article(data) + tail)
    fixed.append(entry["slug"])

print(f"restored canonical shell for {len(fixed)} person pages")
