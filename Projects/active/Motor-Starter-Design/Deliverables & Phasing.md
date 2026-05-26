---
tags:
  - project
  - motor-starter
  - deliverables
parent: "[[MOCs/Motor Starter Design — Map of Content.md]]"
created: 2026-05-21
---

# Deliverables & Phasing

## Tool Setup — draw.io

1. Go to `diagrams.net` (no account required)
2. New diagram → select **Blank**
3. Open shape libraries: View → Shapes → tick **Electrical** (IEC symbols) and **Floorplan** (for title block elements)
4. Set page size: A3 landscape for each drawing

### Layout Per Page

- Left half: power circuit (vertical, top to bottom — supply → devices → motor)
- Right half: control circuit (ladder diagram — two vertical rails, rungs left to right)
- Bottom strip: title block (drawing number, revision, date, title, scale)

### Symbol Conventions

- Power conductors: 2px line weight, black
- Control conductors: 1px line weight, red
- Earth/PE conductors: green
- All devices labelled with reference (K1, KT, OL, MCCB)
- Terminal numbers on all connections (T1, T2, T3 for motor; L1, L2, L3 for supply)
- IEC contact symbols: NO = open gap with line, NC = diagonal line through gap

### Title Block

```
| Project: Motor Starter Design Comparison | Drawing: 1/4 |
| Motor: 7.5kW, 400V, 15.9A FLC           | Rev: A       |
| Configuration: DOL Starter               | Date: [date] |
| Drawn by: [your name]                    | Scale: NTS   |
```

## Phasing (Weekend)

**Day 1 (~3–4 hours):**
- Set up draw.io, build the IEC symbol library
- Drawing 1: DOL power + control circuits
- Drawing 2: Star-delta power circuit

**Day 2 (~3–4 hours):**
- Drawing 2 continued: star-delta control circuit (timer, interlocks)
- Drawing 3: VFD circuit
- Drawing 4: device and cable schedule page
- Export all 4 pages, clean up layout

## LinkedIn Output

Export each drawing as **PNG at 150–200 DPI** from draw.io. Create a simple carousel or collage showing all four pages.

### Suggested Caption

> "Motor Starter Design Comparison — DOL, Star-Delta, and VFD-fed circuits for a 7.5kW pump motor. Each configuration drawn to IEC conventions with device selection and cable sizing. Part of a structured electrical installation study covering protection coordination, control circuit logic, and starting method selection."

### What Makes It Stand Out

Most LinkedIn "motor starter" posts are screenshots of textbook diagrams. A clean, original draw.io schematic with your own device schedule and cable sizing calculation is differentiated content — it shows you've applied the knowledge, not just read it.

## What This Tests

| Concept | Reference |
|---|---|
| Self-latching control logic | Module 3, section 3.7 |
| Star-delta contactor interlock | Module 3, section 3.8 |
| Star contactor current rating (FLC/√3) | Module 2, section 2.3 |
| Overload relay setting = FLC | Module 3, section 3.3 |
| VFD bypass contactor purpose | Module 2, section 2.5 |
| Screened cable for VFD output | Module 8, section 8.7 |
| Cable sizing methodology | Module 7, section 7.11 |
| Phase-to-earth PE conductor | Pre-commissioning tests |
