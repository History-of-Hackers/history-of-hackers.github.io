#!/usr/bin/env python3
"""Recount data/<type>/*.json and rewrite the hardcoded numbers on the homepage.

Run after adding or removing entries:

    python3 scripts/update_home_counts.py

Updates both the stats row (<div class="num">N</div><div class="label">…</div>)
and the "Explore by type" cards (<a href="<dir>/">…</a></h3><p>N entries.).
Exits non-zero if a section could not be matched, so drift is loud.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

# homepage label -> data directory
SECTIONS = [
    ("People", "people"),
    ("Groups", "groups"),
    ("Tools", "tools"),
    ("Vulnerabilities & Discoveries", "vulnerabilities"),
    ("Attacks & Breaches", "attacks"),
    ("Events", "events"),
    ("Publications", "publications"),
    ("Fields", "fields"),
]


def main():
    html = INDEX.read_text()
    changed = []
    for label, folder in SECTIONS:
        count = len(list((ROOT / "data" / folder).glob("*.json")))

        stat_re = re.compile(rf'(<div class="num">)(\d+)(</div><div class="label">{re.escape(label)}</div>)')
        card_re = re.compile(rf'(<a href="{folder}/">[^<]*</a></h3><p>)(\d+)( entries\.)')
        for name, rx in (("stat", stat_re), ("card", card_re)):
            m = rx.search(html)
            if not m:
                print(f"error: could not find {name} block for {label!r} in index.html", file=sys.stderr)
                return 1
            if int(m.group(2)) != count:
                changed.append(f"{label} ({name}): {m.group(2)} -> {count}")
                html = rx.sub(rf"\g<1>{count}\g<3>", html, count=1)

    if changed:
        INDEX.write_text(html)
        print("updated index.html:")
        for line in changed:
            print("  " + line)
    else:
        print("index.html counts already up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
