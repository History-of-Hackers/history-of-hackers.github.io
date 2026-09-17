# Data Directory

Canonical content for the site, one JSON file per entity, matching the
schemas in [`/templates`](../templates). The old single `ARTICLES` array in
`index.html` has been migrated here — every page under `/people/`,
`/groups/`, `/tools/`, `/vulnerabilities/`, `/events/`, `/publications/`,
and `/fields/` is generated from these records plus [`manifest.json`](manifest.json)
(the flat index the client-side search/filter code reads).

## Layout

```
data/
├── manifest.json     # flat list of {id,type,title,slug,era,tags,summary,url} for all entities — powers search/filters
├── people/           # matching templates/person.json
├── groups/           # matching templates/group.json
├── tools/            # matching templates/tool.json
├── vulnerabilities/  # matching templates/vulnerability.json
├── events/           # matching templates/event.json
├── publications/     # matching templates/publication.json
└── fields/           # matching templates/field.json
```

## Adding a new entity

1. Copy the matching file from `/templates` into the right `data/<type>/`
   subfolder, named `<slug>.json`.
2. Fill it with sourced facts only — no invented fields. See
   [STYLE_GUIDE.md](../STYLE_GUIDE.md) and [SOURCES.md](../SOURCES.md).
   Set `editorial.createdBy` to your name — it is rendered on the page as
   "Created by …" so readers know who authored the entry.
3. Add an entry to `manifest.json` (same `id`/`type`/`title`/`slug`/`era`/
   `tags`/`summary`/`url` shape as the existing entries).
4. Copy an existing page of the same type (e.g. `people/adrian-lamo.html`)
   as a template for the new static page, and swap in the new content
   (infobox, `why-matters` line, body, timeline, sources). Keep the same
   `<head>` structure (title/description/canonical/JSON-LD) updated for the
   new entity.
5. If the entry has explicitly dated milestones, they'll also want to
   appear in `/timeline/` — that page is generated from every entity's
   `timeline` array, so make sure dates match what's in the JSON record.

There is no build step: whatever HTML you write/copy is what ships. A
one-time migration script produced the current batch of pages but isn't
part of the repository — pages are meant to be hand-maintained JSON +
HTML going forward, consistent with the project's "no build tooling"
constraint.
