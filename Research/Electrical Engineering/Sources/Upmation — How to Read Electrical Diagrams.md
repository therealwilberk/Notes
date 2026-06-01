---
type: source
tags: [eee, wiring-diagrams, source-reference, upmation]
created: 2026-06-01
status: complete
video: "https://www.youtube.com/watch?v=GHhcyH99inE"
---

# Upmation — How to Read Electrical Diagrams

> [!info] Source
> Free YouTube video. Covers IEC wiring diagram reading fundamentals — legend pages, reading direction, de-energized state, wire tags, cross-referencing, terminal strips, nomenclature.

---

## Content Covered

| Topic | Topic Note |
|-------|------------|
| Legend page, symbol variations by software | [[IEC Reference Designations]] |
| Reading direction (left to right, top to bottom) | [[Panel Layout & Structure]] |
| De-energized state (NO/NC appearance) | [[Panel Layout & Structure]] |
| Wire tags and device tags | [[Circuit Numbering & Wire Tags]] |
| Column numbers, page.column cross-referencing | [[Cross-Referencing Multi-Page Diagrams]] |
| Terminal strips, double-level terminal blocks | [[Panel Layout & Structure]] |
| Nomenclature prefixes (-KA, -KM) | [[Reading Relay Schematics]] |

## Raw Notes (for reference)

### General
- Wiring diagrams vary by country (standards), company (layout preferences), and software (EPLAN, AutoCAD Electrical)
- Range from single page to 200+ pages — same skill, different scale

### Legend Page
- Every proper diagram has a legend/abbreviation page (usually at the front)
- Symbols can look different depending on software — the legend defines what's what for *that document*

### Reading Direction
- Standard: left to right, top to bottom
- Designers break this when it gives a better layout — always check before assuming where power enters

### De-energized State
- All contacts shown in neutral, non-energized state
- NC contacts appear closed, NO contacts appear open
- Misreading this is a common source of confusion

### Wire Tags
- Numbers on wires aren't random — they're wire tags
- Each wire has a unique tag for tracing
- If a wire comes loose, look up the tag on the diagram to find where it goes
- Panels without wire tags are nightmares to troubleshoot

### Column Numbers & Cross-Referencing
- Pages divided into numbered columns (at top of page)
- Format: page.column (e.g., 2.0 = page 2, column 0)
- Arrow with number = "this signal continues at page X, column Y"
- Below a coil = list of all contacts with their page.column addresses
- Below a contact = where the driving coil lives
- Constantly flipping between pages is normal — that's how multi-page schematics work

### Terminal Strips
- Groups of terminal blocks get a strip designation (X0, XC)
- Usually grouped by shared voltage level or function
- Double-level terminal blocks: same footprint, two wires per side — saves panel space

### Nomenclature
- Label convention is drawing-specific — always check the legend
- -KA = relay, -KM = contactor (varies by drawing)
- Same symbol can mean different things depending on the nomenclature

### Design Note
- When designing, every component needs its datasheet consulted
- Assumptions about terminal layouts or connection sequences create hard-to-trace faults

## Resources Mentioned

| Resource | Type | Notes |
|----------|------|-------|
| [ControlByte](https://controlbyte.tech/blog/how-to-read-electrical-wiring-diagram/) | Blog | Deep dive on IEC conventions |
| WiredWhite | Course | "Basic Electrical Controls & Diagram Reading" — DOL, reversing, soft starters, VFDs |
| Udemy | Course | "Introduction to Electrical Controls & Diagram Reading" — goes on sale often ($10-15) |
