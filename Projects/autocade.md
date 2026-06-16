---
tags: [autocade, electrical, schematic, project]
parent: "[[Projects -- Map of Content]]"
status: planning
start: 2026-06-16
target: 2026-10-01
estimate: 14 weeks @ ~10 hrs/wk
---

# AutoCADE — SLD Recreation Project

## Scope

Recreate an IEC electrical schematic from scratch in AutoCAD, using a source PDF as reference. Goal is not the drawing — it's understanding the system, the standards, and the tool well enough to do original design work by Phase 12.

**Source:** `~/Documents/PDFs/IEC-Schematic-Learning-Resource-VER1.1.pdf`

**Total: ~14 weeks at ~10 hrs/week** (140 hrs)

---

## Phase Breakdown

### Phase 1 — Reconnaissance (Weeks 1-2, ~20 hrs)

Don't open AutoCAD. Read the entire schematic package. Build a mental model.

- [ ] Read cover to cover, noting every page type
- [ ] Identify every major device, motor, relay, PLC module, power source
- [ ] Create an "Unknowns" page — every symbol, acronym, component you don't understand
- [ ] Research unknowns one by one
- [ ] Write a one-page description: what the system does + list of major subsystems

**Deliverable:** One-page system description + unknowns archive

---

### Phase 2 — Standards Discovery (Weeks 2-3, ~15 hrs)

Understand how the drawing itself is constructed.

- [ ] Study title blocks, page numbering, wire numbering
- [ ] Figure out device naming: K1, TOR1, Q1, PLC1 conventions
- [ ] Understand cross-references between pages
- [ ] Note coordinate system and symbol conventions
- [ ] Document every rule you find

**Deliverable:** Written drawing rules document

---

### Phase 3 — AutoCAD Fundamentals (Weeks 3-4, ~15 hrs)

Only the commands you'll actually need.

- [ ] Lines, polylines, layers, blocks, attributes
- [ ] Object snaps, copying, mirroring, arrays
- [ ] Text, dimensions, plotting
- [ ] Practice exercises — nothing related to the project

**Deliverable:** Familiarity with essential AutoCAD operations

---

### Phase 4 — Symbol Library Construction (Weeks 4-5, ~10 hrs)

Build reusable blocks for everything the project needs.

- [ ] Motors, contactors, overload relays
- [ ] Pushbuttons, selector switches, pilot lights
- [ ] Terminal blocks, PLC modules, relays
- [ ] Power supplies, breakers

**Deliverable:** Clean, reusable symbol library

---

### Phase 5 — First Page Recreation (Weeks 5-6, ~10 hrs)

- [ ] Pick the simplest page
- [ ] Recreate from scratch
- [ ] Compare against original, fix mistakes
- [ ] Do not move on until it's correct

**Deliverable:** One correctly recreated page

---

### Phase 6 — Repetition & Pattern Recognition (Weeks 6-8, ~20 hrs)

- [ ] Continue recreating pages one at a time
- [ ] Track time per page — look for acceleration
- [ ] Document repeating patterns vs unique elements

**Deliverable:** Growing page collection + pattern list

---

### Phase 7 — Subsystem Analysis (Weeks 8-9, ~10 hrs)

Stop drawing. Trace signals.

- [ ] Follow signal from pushbutton → relays → PLC → contactor → motor
- [ ] Trace wire references between pages
- [ ] Document information flow through the system

**Deliverable:** End-to-end explanation of any major function

---

### Phase 8 — Layout Work (Weeks 9-10, ~10 hrs)

- [ ] Learn device mounting locations
- [ ] Study terminal block organization
- [ ] Understand panel physical arrangement
- [ ] Recreate panel layout and front-panel layout

**Deliverable:** Recreated physical layout drawings

---

### Phase 9 — Validation (Weeks 10-11, ~10 hrs)

Review as if you're checking another engineer's work.

- [ ] Check device tags, wire numbers, references
- [ ] Check terminal assignments, symbol consistency
- [ ] Check layer usage, spacing, readability
- [ ] Compare against source, fix discrepancies

**Deliverable:** Corrected, internally consistent drawing package

---

### Phase 10 — Reconstruction from Memory (Week 11, ~5 hrs)

- [ ] Close the original
- [ ] Recreate one subsystem from memory
- [ ] Note every mistake — each reveals a knowledge gap

**Deliverable:** List of concepts needing further study

---

### Phase 11 — Extension (Weeks 11-12, ~5 hrs)

Add something original:

- [ ] Another motor circuit
- [ ] Another PLC input
- [ ] Another pilot light or safety device

**Deliverable:** First piece of original design work

---

### Phase 12 — Reflection & Documentation (Weeks 12-14, ~10 hrs)

- [ ] Write down what slowed you down
- [ ] Which concepts appeared repeatedly?
- [ ] Which AutoCAD skills mattered most?
- [ ] Which research sources were useful?
- [ ] Write your personal playbook for the next project

**Deliverable:** Reusable personal process document

---

## Weekly Distribution

| Week | Phase(s) | Hours |
|------|----------|-------|
| 1-2  | P1: Reconnaissance | 10/wk |
| 2-3  | P2: Standards | 10/wk |
| 3-4  | P3: AutoCAD basics | 10/wk |
| 4-5  | P4: Symbol library | 10/wk |
| 5-6  | P5: First page | 10/wk |
| 6-8  | P6: Repetition | 10/wk |
| 8-9  | P7: Subsystem analysis | 10/wk |
| 9-10 | P8: Layout | 10/wk |
| 10-11| P9: Validation | 10/wk |
| 11   | P10: Memory recon | 5/wk |
| 11-12| P11: Extension | 5/wk |
| 12-14| P12: Documentation | 5/wk |

**End date target: 2026-10-01**
