---
type: project
tags:
  - project
  - motor-starter
  - schedule
parent: "[[Motor Starter Design — Map of Content]]"
created: 2026-05-21
status: in-progress
---

# Drawing 4 — Device & Cable Schedule

## Device Schedule

| Configuration | Device | Type | Rated current | Setting/note |
|---|---|---|---|---|
| DOL | MCCB | Motor-duty, type aM coordination | 25A | Instantaneous trip ≥10× In |
| DOL | Contactor K1 | AC-3 | 18A (LC1D18 or equivalent) | Coil: 230V AC |
| DOL | Overload relay | Class 10, adjustable | Set to 15.9A | |
| Star-delta | MCCB | Motor-duty | 25A | As DOL |
| Star-delta | Contactor K1 (main) | AC-3 | 18A | |
| Star-delta | Contactor K2 (star) | AC-3 | 9A (carries FLC/√3 = 9.2A) | |
| Star-delta | Contactor K3 (delta) | AC-3 | 18A | |
| Star-delta | Timer relay KT | ON-delay | Set: 8 seconds | Adjustable 2–15s |
| Star-delta | Overload relay | Class 10 | Set to 15.9A | |
| VFD | MCCB (supply side) | Standard | 25A | |
| VFD | VFD | 7.5kW, 400V | Set motor FLC: 15.9A | Internal motor protection |
| VFD | Bypass contactor KB | AC-3 | 18A | Closes post-ramp |

## Cable Schedule

| Configuration | Cable | Cross-section | Type | Sizing basis |
|---|---|---|---|---|
| DOL | Supply to MCCB | 4mm² Cu | 4-core + E | ≥FLC (15.9A); 4mm² = 27A clipped ✓ |
| DOL | MCCB to motor | 4mm² Cu | 4-core + E | As above |
| DOL | Control cable | 1.5mm² Cu | Multi-core | Standard control circuit |
| Star-delta | Supply to MCCB | 4mm² Cu | 4-core + E | As DOL |
| Star-delta | MCCB to motor (6-core) | 4mm² Cu | 6-core + E | All 6 motor terminals require individual conductors |
| Star-delta | Control cable | 1.5mm² Cu | Multi-core | Minimum 7-core (Stop, Start, K1, K2, K3, KT, OL) |
| VFD | Supply to VFD | 4mm² Cu | 4-core + E | Input current ≈ 16.8A (allow 105% FLC) |
| VFD | VFD to motor | 4mm² Cu | Screened, 4-core + E | Screened mandatory for VFD output |
| VFD | Control cable | 1.5mm² Cu screened | Multi-core screened | Screened to prevent VFD switching noise on signals |

## Cable Sizing Note

Motor FLC = 15.9A. Selected 4mm² Cu cable (current-carrying capacity 27A clipped to surface per IEC 60364-5-52, Table B.52.4). No derating factors applied — short run, single cable, ambient ≤40°C. Voltage drop at 15.9A over estimated 20m run: ΔV = 2 × 15.9 × 20 × 0.0038 = 2.4V = 1.0% — within 4% limit. ✓
