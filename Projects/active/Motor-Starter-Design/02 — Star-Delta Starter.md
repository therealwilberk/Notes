---
type: project
tags:
  - project
  - motor-starter
  - star-delta
parent: "[[Motor Starter Design — Map of Content]]"
created: 2026-05-21
status: in-progress
---

# Drawing 2 — Star-Delta Starter

## Power Circuit

Supply → MCCB → K1 (main/line contactor) → Motor terminals (U1/V1/W1)

K2 (star contactor) → short circuits U2/V2/W2

K3 (delta contactor) → connects U2-V1, V2-W1, W2-U1

Both K2 and K3 connected to motor terminals (U2/V2/W2).

## Control Circuit

- Start/Stop rungs (same Stop NC / OL NC logic as DOL)
- K1 + K2 energise simultaneously on start
- Timer relay KT starts when K1 energises
- On KT timeout: K2 coil de-energised → K3 coil energises
- Electrical interlock: K2 NC auxiliary in series with K3 coil; K3 NC auxiliary in series with K2 coil
- Mechanical interlock notation shown on drawing

## What You're Demonstrating

3-contactor architecture, timer logic, interlock design, open-transition switching.
