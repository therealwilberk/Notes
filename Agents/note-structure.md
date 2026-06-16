# Note Structure

## Directory Layout

```
MOCs/
  <Topic> -- Map of Content.md    # Hub file linking to all notes for a topic

Notes/
  <Domain>/
    <Subdomain>/
      <note-name>.md              # Individual note files

Reads/
  <Publication>/
    <YYYY-MM-DD_slug>.md          # Saved articles (read-only reference)

Research/
  <Topic>/
    <note-name>.md                # Deep-dive research notes
```

## Domain Boundaries

Cross-domain content (e.g., pandas is both Python and ML) lives in its primary domain. The other domain's MOC cross-links to it. Tags provide secondary discoverability.

| Domain | Subdirectories | Prefix |
|--------|---------------|--------|
| `Notes/ML/` | `Concepts/`, `Tools/` | `ml-` |
| `Notes/Programming/Python/` | `Python-Hitchhikers-Guide/`, `Data/`, `Serving/`, `Tooling/` | `py-`, `python-hg-` |
| `Notes/Programming/Docker/` | `exercises/` | `docker-` |
| `Notes/Programming/Rust/` | `exercises/` | `rust-` |
| `Notes/EEE/` | — | — |

Examples from this vault:

```
MOCs/Rust -- Map of Content.md
MOCs/ML & Data Science Packages -- Map of Content.md
MOCs/Python -- Map of Content.md

Notes/ML/Tools/ml-lightgbm.md
Notes/ML/Concepts/Class Imbalance.md
Notes/Programming/Python/Data/py-pandas.md
Notes/Programming/Python/Python-Hitchhikers-Guide/python-hg-c1-functions-vs-classes.md
Notes/Programming/Python/Serving/py-fastapi.md
Notes/Programming/Python/Tooling/py-uv.md
Notes/Programming/Rust/rust-ownership.md
Notes/Programming/Docker/docker-m1-containers.md
```

Keep subdirectories small (≤15 files). When a folder grows beyond that, subdivide into more specific subdirectories.

## File Naming

- Lowercase, hyphen-separated (`rust-structs.md`, not `RustStructs.md` or `rust_structs.md`)
- Prefix with category for discoverability (`ml-lightgbm.md`, `py-pandas.md`, `docker-m1-containers.md`)
- When moving a file to a new domain, rename the prefix AND add the old name to `aliases:` for backwards compatibility
- MOCs use the title as the filename (`Topic -- Map of Content.md` — always use double-dash)
- Exercises live in `exercises/<module-n>/` with `README.md` per module
- Module notes use `<topic>-m<number>-<short-name>.md` (e.g., `docker-m1-containers.md`, `fe-m2-missing-values.md`)

## Frontmatter Template

Every note file must have frontmatter:

```yaml
---
tags: [topic1, topic2, subtopic]
aliases: ["Alternative Name", "Common Abbreviation"]
parent: "[[Topic MOC]]"
created: YYYY-MM-DD
status: complete | in-progress | draft
exercises: "[[exercises/module-n]]"   # only if exercises exist
---
```

- `tags`: lowercase, plural. Broad categories first, specific later.
- `aliases`: short names the note might be referred to as. **Required when renaming a file** — add the old name so existing wikilinks resolve.
- `parent`: **required** — wikilink to the topic's MOC file. Always include `MOCs/` prefix in the path.
- `status`: `draft` (just created), `in-progress` (being worked), `complete` (ready).
- `exercises`: optional wikilink to companion exercises directory.

## Folder Rules

- All notes go under `Notes/<Domain>/<Subdomain>/`
- MOCs go directly in `MOCs/`
- Exercises go alongside the note file (e.g., `Notes/Programming/Docker/exercises/`)
- Never create top-level note files outside `Notes/` or `MOCs/`

## Curriculum & Exercises

Curriculum building and exercise schema are documented in `lessons-process.md`. This file covers vault structure only.

## Git Commits

- Commit after every significant change (restructure, new notes, deleted files)
- Commit message format: concise, lowercase, hyphen-separated
- Example: `restructure: split ML into Concepts/Tools, move Python tools to Programming/Python/`
- Do not leave uncommitted changes between sessions
