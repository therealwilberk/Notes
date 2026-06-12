# MOC (Map of Content) Convention

A MOC is a hub file that links to all notes for a topic. It lives in `MOCs/` and serves as the entry point.

## Frontmatter

```yaml
---
type: moc
tags: [moc, topic1, topic2]
aliases: ["Topic MOC", "Alternative Name"]
created: YYYY-MM-DD
status: in-progress | complete
---
```

## Structure

```
# Topic -- Map of Content

Brief one-liner about what these notes cover (what, why, scope).

## Section Name

| # | Name | File | Status |
|---|------|------|--------|
| R1 | Topic Name | [[Notes/Path/note-name\|alias]] | Complete |

## Next Section
...
```

## Style Rules

- Use a table with `#`, `Name`, `File` (wikilink), `Status` columns
- Keep the one-liner at the top short -- this is a hub, not a readme
- Group notes into logical sections (e.g., "The Stack", "Core Concepts", "Project Tooling")
- Mark status: `Complete`, `In Progress`, `Draft`
- Update the section header to reflect the chapter/scope range (e.g., `## Core Concepts (Ch 4-5)`)
- Add a new row when a new note is created

## Example

```
# Rust -- Map of Content

Notes for The Rust Book. Compressed, example-heavy, no fluff -- skip the book and go straight to the gotchas.

## CLI & Toolchain

| # | Topic | Status |
|---|-------|--------|
| C0 | [[Notes/Programming/Rust/rust-cli\|80/20 CLI Reference]] | Complete |

## Core Concepts (Ch 4-5)

| # | Topic | Status |
|---|-------|--------|
| R1 | [[Notes/Programming/Rust/rust-ownership\|Ownership]] | Complete |
| R2 | [[Notes/Programming/Rust/rust-references\|References & Borrowing]] | Complete |
| R3 | [[Notes/Programming/Rust/rust-slices\|Slices]] | Complete |
| R4 | [[Notes/Programming/Rust/rust-structs\|Structs & Methods]] | Complete |
```
