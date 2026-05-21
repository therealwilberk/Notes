# Mini-Project — Motor Starter Design Comparison
## draw.io | IEC symbols | Weekend deliverable

---

## The Brief

Design and draw the complete electrical schematics — power circuit and control circuit — for three motor starter configurations applied to the same motor. Produce a device and cable schedule to support the drawings. The output is a four-page draw.io document, exportable to PNG/PDF for LinkedIn.

This is not a theoretical exercise. Every device rating, cable size, and protection setting must be calculated and justified. The drawings must be correct enough that a site electrician could wire from them.

---

## The Motor (Case Study)

Use the established motor from Module 1. You already know this machine.

| Parameter | Value |
|---|---|
| Power | 7.5 kW |
| Voltage | 230Δ / 400Y |
| Full load current (FLC) | 15.9A (star, 400V supply) |
| Supply | 3-phase, 400V / 230V, 50Hz, TN-S |
| Speed | 1455 RPM (4-pole) |
| Insulation class | F |
| Duty | S1 continuous |
| Application | Centrifugal pump (low starting torque — suits star-delta) |

---

## The Three Configurations

### Drawing 1 — DOL Starter

**Power circuit:**
Supply (L1/L2/L3) → MCCB → Contactor K1 → Thermal overload relay → Motor terminals (U1/V1/W1)
Earth conductor from motor frame to MET shown.

**Control circuit (ladder diagram):**
- Rung 1: Stop (NC) → Start (NO) → OL relay NC contact → K1 coil
- Rung 2: K1 auxiliary NO contact in parallel with Start (self-latch)
- Rung 3: Run indicator lamp (H1) via K1 NO auxiliary

**What you're demonstrating:** the simplest protection hierarchy, self-latching control logic, fail-safe stop design.

---

### Drawing 2 — Star-Delta Starter

**Power circuit:**
Supply → MCCB → K1 (main/line contactor) → Motor terminals (U1/V1/W1)
K2 (star contactor) → short circuits U2/V2/W2
K3 (delta contactor) → connects U2-V1, V2-W1, W2-U1
Both K2 and K3 connected to motor terminals (U2/V2/W2).

**Control circuit:**
- Start/Stop rungs (same Stop NC / OL NC logic as DOL)
- K1 + K2 energise simultaneously on start
- Timer relay KT starts when K1 energises
- On KT timeout: K2 coil de-energised → K3 coil energises
- Electrical interlock: K2 NC auxiliary in series with K3 coil; K3 NC auxiliary in series with K2 coil
- Mechanical interlock notation shown on drawing

**What you're demonstrating:** 3-contactor architecture, timer logic, interlock design, open-transition switching.

---

### Drawing 3 — VFD-Fed Motor Circuit

**Power circuit:**
Supply → MCCB (supply-side protection) → VFD input terminals (L1/L2/L3)
VFD output terminals (U/V/W) → Motor terminals (U1/V1/W1)
Bypass contactor KB shown in parallel with VFD output (closed after motor at full speed)
Screened motor cable notation shown. Earth continuity from motor frame to VFD earth terminal to MET.

**Control interface (simplified):**
- VFD enable via digital input DI1 (from remote start/stop PB circuit, 24V DC)
- Run/fault signal via digital output DO1 to indicator lamp
- VFD parameter table as drawing note: motor FLC setting, acceleration time, deceleration time, overload protection set internally

**What you're demonstrating:** VFD circuit architecture differs from contactor-based starters; bypass contactor purpose; screened cable requirement; earth continuity path specific to VFD installations.

---

### Drawing 4 — Device & Cable Schedule

A single structured table covering all three configurations:

**Device schedule:**

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

**Cable schedule:**

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

**Cable sizing note (brief rationale on drawing):**
Motor FLC = 15.9A. Selected 4mm² Cu cable (current-carrying capacity 27A clipped to surface per IEC 60364-5-52, Table B.52.4). No derating factors applied — short run, single cable, ambient ≤40°C. Voltage drop at 15.9A over estimated 20m run: ΔV = 2 × 15.9 × 20 × 0.0038 = 2.4V = 1.0% — within 4% limit. ✓

---

## Tool Setup — draw.io

**Getting started:**
1. Go to `diagrams.net` (no account required)
2. New diagram → select **Blank**
3. Open shape libraries: View → Shapes → tick **Electrical** (IEC symbols) and **Floorplan** (for title block elements)
4. Set page size: A3 landscape for each drawing (gives room for both power and control circuits side by side)

**Recommended layout per page:**
- Left half: power circuit (vertical, top to bottom — supply → devices → motor)
- Right half: control circuit (ladder diagram — two vertical rails, rungs left to right)
- Bottom strip: title block (drawing number, revision, date, title, scale)

**Symbol conventions to follow:**
- Power conductors: 2px line weight, black
- Control conductors: 1px line weight, red
- Earth/PE conductors: green
- All devices labelled with their reference (K1, KT, OL, MCCB)
- Terminal numbers on all connections (T1, T2, T3 for motor; L1, L2, L3 for supply)
- IEC contact symbols: NO = open gap with line, NC = diagonal line through gap

**Title block (bottom of each page):**
```
| Project: Motor Starter Design Comparison | Drawing: 1/4 |
| Motor: 7.5kW, 400V, 15.9A FLC           | Rev: A       |
| Configuration: DOL Starter               | Date: [date] |
| Drawn by: [your name]                    | Scale: NTS   |
```

---

## Phasing (Weekend)

**Day 1 (~3–4 hours):**
- Set up draw.io, build the IEC symbol library (save commonly used symbols as custom shapes once drawn)
- Drawing 1: DOL power + control circuits
- Drawing 2: Star-delta power circuit (the complex one — 3 contactors, 6 motor terminals)

**Day 2 (~3–4 hours):**
- Drawing 2 continued: star-delta control circuit (timer, interlocks)
- Drawing 3: VFD circuit (simpler than star-delta control, different topology)
- Drawing 4: device and cable schedule page
- Export all 4 pages, clean up layout

---

## LinkedIn Output

Export each drawing as **PNG at 150–200 DPI** from draw.io (File → Export → PNG, set resolution). Create a simple carousel or collage showing all four pages. Suggested caption structure:

> "Motor Starter Design Comparison — DOL, Star-Delta, and VFD-fed circuits for a 7.5kW pump motor. Each configuration drawn to IEC conventions with device selection and cable sizing. Part of a structured electrical installation study covering protection coordination, control circuit logic, and starting method selection."

**What makes it stand out:** most LinkedIn "motor starter" posts are screenshots of textbook diagrams. A clean, original draw.io schematic with your own device schedule and cable sizing calculation is differentiated content — it shows you've applied the knowledge, not just read it.

---

## What This Tests

| Concept | Where it comes from |
|---|---|
| Self-latching control logic | Module 3, section 3.7 |
| Star-delta contactor interlock | Module 3, section 3.8 |
| Star contactor current rating (FLC/√3) | Module 2, section 2.3 |
| Overload relay setting = FLC | Module 3, section 3.3 |
| VFD bypass contactor purpose | Module 2, section 2.5 quirks |
| Screened cable for VFD output | Module 8, section 8.7 |
| Cable sizing methodology | Module 7, section 7.11 |
| Phase-to-earth PE conductor | Pre-commissioning tests document |
