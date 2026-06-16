---
tags: [autocade, electrical, schematic, project]
parent: "[[Projects — Map of Content]]"
status: planning
start: 2026-06-16
target: 2026-08-25
estimate: 200 hrs over 10 weeks
pace: ~20 hrs/week (3-3.5 hrs/day, 6 days)
share: 40%
---

# AutoCADE — SLD Recreation Project

## Scope

Recreate an IEC electrical schematic from scratch in AutoCAD, using a source PDF as reference. Goal is not the drawing — it's understanding the system, the standards, and the tool.

**Source:** `~/Documents/PDFs/IEC-Schematic-Learning-Resource-VER1.1.pdf`

**Target: 10 weeks at ~20 hrs/week** (200 hrs total)

---

## Phase Breakdown

### Phase 1 — Reconnaissance (12 hrs)

Don't open AutoCAD. Read the PDF. Build a mental model.

- Read cover to cover, noting every page type
- Identify every major device, motor, relay, PLC module, power source
- Create an "Unknowns" page — every symbol, acronym, component you don't understand
- Research unknowns one by one
- Write a one-page description of the system + list of major subsystems

**Done when:** one-page description written, unknowns list complete with researched answers

### Phase 2 — Standards Discovery (10 hrs)

Understand how the drawing itself is constructed.

- Study title blocks, page numbering, wire numbering
- Figure out device naming conventions (K1, TOR1, Q1, PLC1...)
- Understand cross-references between pages
- Note coordinate system and symbol conventions
- Document every rule you find

**Done when:** written drawing rules document exists

### Phase 3 — AutoCAD Fundamentals (15 hrs)

Only the commands you'll need.

- Lines, polylines, layers, blocks, attributes
- Object snaps, copying, mirroring, arrays
- Text, dimensions, plotting
- Tiny practice exercises unrelated to the project

**Done when:** can draw a simple shape from memory without looking up commands

### Phase 4 — Symbol Library Construction (15 hrs)

Build reusable blocks for everything the project needs.

- Motors, contactors, overload relays
- Pushbuttons, selector switches, pilot lights
- Terminal blocks, PLC modules, relays
- Power supplies, breakers

**Done when:** all required symbols exist as reusable blocks

### Phase 5 — First Page Recreation (25 hrs)

- Pick the simplest page
- Recreate from scratch — slow, meticulous
- Compare against original, fix mistakes
- Do not move on until it's correct

**Done when:** page matches original (reviewer check)

### Phase 6 — Repetition & Pattern Recognition (40 hrs)

Heaviest phase. Continue recreating pages one at a time.

- Count total pages in source PDF first → define "done" as N pages complete
- Track time per page — look for acceleration
- Document repeating patterns vs unique elements
- Accept diminishing returns: pages that are 90% similar to previous ones are done faster

**Done when:** X out of Y pages recreated (set X before starting — e.g., 80% of non-trivial pages)

### Phase 7 — Subsystem Analysis (18 hrs)

Stop drawing. Trace signals.

- Follow signal from pushbutton → relays → PLC → contactor → motor
- Trace wire references between pages
- Document information flow through the system

**Done when:** can explain any major function end-to-end in plain English

### Phase 8 — Layout Work (18 hrs)

- Study device mounting, terminal block organization, panel arrangement
- Recreate panel layout and front-panel layout

**Done when:** layout drawings match source checkpoints

### Phase 9 — Validation (15 hrs)

- Check device tags, wire numbers, references, terminal assignments
- Check symbol consistency, layer usage, spacing, readability
- Compare against source, fix discrepancies

**Done when:** no discrepancies against source checklist

### Phase 10 — Reconstruction from Memory (8 hrs)

- Pick one subsystem you've already drawn — the most complex one you feel shaky on
- Close the original, recreate from memory
- Note every mistake — each reveals a knowledge gap

**Done when:** list of gaps documented

### Phase 11 — Extension (10 hrs)

Add something original — motor circuit, PLC input, safety device. Pick the simplest addition that forces a design decision.

**Done when:** one original element drawn and cross-referenced correctly

### Phase 12 — Documentation (14 hrs)

- What slowed you down, which concepts repeated, which skills mattered
- Which research sources were useful
- Write your personal playbook for the next project

**Done when:** playbook document that would help a beginner avoid your mistakes

---

## Weekly Schedule

| Week | Phases | Hrs | Cum |
|------|--------|-----|-----|
| 1 | P1 (12) + P2 start (8) | 20 | 20 |
| 2 | P2 finish (2) + P3 (15) + P4 start (3) | 20 | 40 |
| 3 | P4 finish (12) + P5 start (8) | 20 | 60 |
| 4 | P5 (17) | 20 | 80 |
| 5 | P5 finish (0) + P6 start (20) | 20 | 100 |
| 6 | P6 (20) | 20 | 120 |
| 7 | P7 (18) + P6 finish (2) | 20 | 140 |
| 8 | P8 (18) + P9 start (2) | 20 | 160 |
| 9 | P9 (13) + P10 (8) | 20 | 180 |
| 10 | P11 (10) + P12 (14) | 20 | 200 |

**Target end: 2026-08-25** (10 weeks)
