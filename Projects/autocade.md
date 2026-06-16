---
tags: [autocade, electrical, schematic, project]
parent: "[[Projects — Map of Content]]"
status: planning
start: 2026-06-16
target: 2026-08-18
estimate: 200 hrs over 9 weeks
pace: ~22 hrs/wk (3.5-4 hrs/day, 6 days)
share: 40%
---

# AutoCADE — SLD Recreation Project

## Scope

Recreate an IEC electrical schematic from scratch in AutoCAD, using a source PDF as reference. Goal is not the drawing — it's understanding the system, the standards, and the tool.

**Source:** `~/Documents/PDFs/IEC-Schematic-Learning-Resource-VER1.1.pdf`

**Target: 9 weeks at ~22 hrs/week** (200 hrs total)

---

## Phase Breakdown

### Phase 1 — Reconnaissance (12 hrs)

Don't open AutoCAD. Read the PDF. Build a mental model.

- Read cover to cover, noting every page type
- Identify every major device, motor, relay, PLC module, power source
- Create an "Unknowns" page — every symbol, acronym, component you don't understand
- Research unknowns one by one
- Write a one-page description of the system + list of major subsystems

### Phase 2 — Standards Discovery (10 hrs)

Understand how the drawing itself is constructed.

- Study title blocks, page numbering, wire numbering
- Figure out device naming conventions (K1, TOR1, Q1, PLC1...)
- Understand cross-references between pages
- Note coordinate system and symbol conventions
- Document every rule you find

### Phase 3 — AutoCAD Fundamentals (15 hrs)

Only the commands you'll need.

- Lines, polylines, layers, blocks, attributes
- Object snaps, copying, mirroring, arrays
- Text, dimensions, plotting
- Tiny practice exercises unrelated to the project

### Phase 4 — Symbol Library Construction (15 hrs)

Build reusable blocks for everything the project needs.

- Motors, contactors, overload relays
- Pushbuttons, selector switches, pilot lights
- Terminal blocks, PLC modules, relays
- Power supplies, breakers

### Phase 5 — First Page Recreation (25 hrs)

- Pick the simplest page
- Recreate from scratch — slow, meticulous
- Compare against original, fix mistakes
- Do not move on until it's correct

### Phase 6 — Repetition & Pattern Recognition (40 hrs)

Heaviest phase. Continue recreating pages one at a time.

- Track time per page — look for acceleration
- Document repeating patterns vs unique elements
- First pages will be slow, speed builds as patterns click

### Phase 7 — Subsystem Analysis (18 hrs)

Stop drawing. Trace signals.

- Follow signal from pushbutton → relays → PLC → contactor → motor
- Trace wire references between pages
- Document information flow through the system

### Phase 8 — Layout Work (18 hrs)

- Study device mounting, terminal block organization, panel arrangement
- Recreate panel layout and front-panel layout

### Phase 9 — Validation (15 hrs)

- Check device tags, wire numbers, references, terminal assignments
- Check symbol consistency, layer usage, spacing, readability
- Compare against source, fix discrepancies

### Phase 10 — Reconstruction from Memory (8 hrs)

- Close the original
- Recreate one subsystem from memory
- Note every mistake — each reveals a knowledge gap

### Phase 11 — Extension (10 hrs)

Add something original — motor circuit, PLC input, safety device.

### Phase 12 — Documentation (14 hrs)

- Write down what slowed you down, which concepts repeated, which skills mattered
- Which research sources were useful
- Write your personal playbook for the next project

---

## Weekly Schedule

| Week | Phases Active | Hrs | Cumulative |
|------|--------------|-----|------------|
| 1 | P1 (recon), P2 (standards) | 22 | 22 |
| 2 | P1 finish, P2 finish, P3 start (AutoCAD basics) | 22 | 44 |
| 3 | P3 (AutoCAD), P4 start (symbols) | 22 | 66 |
| 4 | P4 (symbols), P5 start (first page) | 22 | 88 |
| 5 | P5 (first page) | 22 | 110 |
| 6 | P5 finish, P6 start (repetition) | 22 | 132 |
| 7 | P6 (repetition) | 22 | 154 |
| 8 | P6 finish, P7 (subsystem), P8 start (layout) | 22 | 176 |
| 9 | P8-12 (layout → validation → memory → extension → docs) | 24 | 200 |

**Target end: 2026-08-18** (Week 9)
