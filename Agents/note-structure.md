# Note Structure

## Directory Layout

```
MOCs/
  <Topic> -- Map of Content.md    # Hub file linking to all notes for a topic

Notes/
  <Category>/
    <Subcategory>/
      <note-name>.md              # Individual note files
```

Examples from this vault:

```
MOCs/Rust -- Map of Content.md
MOCs/ML & Data Science Packages -- Map of Content.md

Notes/Programming/Rust/rust-ownership.md
Notes/Programming/ML/ml-numpy.md
Notes/Programming/Docker/docker-m1-containers.md
```

## File Naming

- Lowercase, hyphen-separated (`rust-structs.md`, not `RustStructs.md` or `rust_structs.md`)
- Prefix with category for discoverability (`ml-numpy.md`, `docker-m1-containers.md`)
- MOCs use the title as the filename (`Rust -- Map of Content.md`)
- Exercises live in `exercises/<module-n>/` with `README.md` per module

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
- `aliases`: short names the note might be referred to as.
- `parent`: **required** -- wikilink to the topic's MOC file.
- `status`: `draft` (just created), `in-progress` (being worked), `complete` (ready).
- `exercises`: optional wikilink to companion exercises directory.

## Folder Rules

- All notes go under `Notes/<Category>/<Subcategory>/`
- MOCs go directly in `MOCs/`
- Exercises go alongside the note file (e.g., `Notes/Programming/Docker/exercises/`)
- Never create top-level note files outside `Notes/` or `MOCs/`
