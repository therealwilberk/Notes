---
tags:
  - project
  - motor-starter
  - vfd
parent: "[[Motor Starter Design — Map of Content]]"
created: 2026-05-21
---

# Drawing 3 — VFD-Fed Motor Circuit

## Power Circuit

Supply → MCCB (supply-side protection) → VFD input terminals (L1/L2/L3)

VFD output terminals (U/V/W) → Motor terminals (U1/V1/W1)

Bypass contactor KB shown in parallel with VFD output (closed after motor at full speed).

Screened motor cable notation shown. Earth continuity from motor frame to VFD earth terminal to MET.

## Control Interface (Simplified)

- VFD enable via digital input DI1 (from remote start/stop PB circuit, 24V DC)
- Run/fault signal via digital output DO1 to indicator lamp
- VFD parameter table as drawing note: motor FLC setting, acceleration time, deceleration time, overload protection set internally

## What You're Demonstrating

VFD circuit architecture differs from contactor-based starters; bypass contactor purpose; screened cable requirement; earth continuity path specific to VFD installations.
