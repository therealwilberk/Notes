---
tags:
  - project
  - motor-starter
  - dol
parent: "[[Motor Starter Design — Map of Content]]"
created: 2026-05-21
---

# Drawing 1 — DOL Starter

## Power Circuit

Supply (L1/L2/L3) → MCCB → Contactor K1 → Thermal overload relay → Motor terminals (U1/V1/W1)

Earth conductor from motor frame to MET shown.

## Control Circuit (Ladder Diagram)

- Rung 1: Stop (NC) → Start (NO) → OL relay NC contact → K1 coil
- Rung 2: K1 auxiliary NO contact in parallel with Start (self-latch)
- Rung 3: Run indicator lamp (H1) via K1 NO auxiliary

## What You're Demonstrating

The simplest protection hierarchy, self-latching control logic, fail-safe stop design.
