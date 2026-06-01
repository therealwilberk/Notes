---
type: source
tags: [eee, bms, controls, source-reference]
created: 2026-06-01
status: in-progress
video: "https://www.youtube.com/watch?v=XzoVXOIvzVs"
progress: "0:00 – 20:24"
---

# BMS Controls Training — 6hr Video

> [!info] Source
> 6-hour training from a real-world BMS control and automation project. Originally a paid 5-day course. Instructor walks through actual schematics from an electrical contractor.

> [!tip] Download the schematics
> Link in the video description. Needed while watching.

---

## Content Covered (0:00 – 20:24)

| Timestamp | Topic | Topic Note |
|-----------|-------|------------|
| 0:00 | Panel layout, inside vs outside line | [[Panel Layout & Structure]] |
| ~3:00 | Power supply, isolator, busbar, MCBs | [[Power Distribution]] |
| ~8:00 | Transformer, 24V control voltage, 0V/24V rails | [[Control Transformers & 24V Systems]] |
| ~12:00 | Circuit numbering (100, 200, 400 circuits) | [[Circuit Numbering & Wire Tags]] |
| ~14:00 | Relay coils (A1/A2), NO/NC contacts | [[Reading Relay Schematics]] |
| ~17:00 | Gas detection safety circuit, series interlocks | [[Safety Circuits & Interlocks]] |
| ~19:00 | Lamp test circuit | [[Circuit Numbering & Wire Tags]] |

## What's Next (20:24+)

- Carbon monoxide / gas sensor details
- More relay circuits on page 2
- Boiler control circuits
- PLC integration

---

## Raw Notes (for reference)

### Panel Layout Basics
- Horizontal line on every page = divider between inside panel and field equipment
- Not all schematics drawn the same way — designer preferences, software differences
- What matters isn't the layout — it's understanding how it works
- Schematic ≠ physical wiring — panel builder can wire differently as long as function is the same

### Power Supply & Distribution (230V)
- Single phase, 50Hz, 230V
- Supply → isolator switch (handle outside, shaft to disconnector inside) → busbar
- 10mm cable from main isolator to busbar + first MCB
- MCB 2: D-type, 6A → transformer primary
- MCB 3: laptop socket
- MCB 4: gas detection system (constant 230V feed)
- All field equipment should have local isolators
- MCB 4 feeds terminal block 1 → field equipment

### Transformer & Controls (24V)
- Safety: 230V on panel door is dangerous. Touch threshold = 50V → use 24V AC
- BMS convention: transformer (not DC power supply), though either works
- 0V distribution via Wago terminal blocks with push-in busbar
- NOT daisy-chained (one fault takes out everything) — multiple terminal blocks for redundancy
- 24V from transformer → MCB or fuse first → then distributed

### Circuit Numbering
- Circuits numbered by which MCB they come from
- Number changes every time circuit passes through a device
- 100 circuit = directly from MCB, before any device
- Example: 24V from MCB → through lamp test push button → 400 circuit

### Lamp Test Circuit
- Normally open push button (black, on panel front)
- When pressed: sends power to ALL indicator lamps simultaneously
- Purpose: quick visual check that all lamps work
- Modern panels should have PLC inputs doubling up the indicators

### Relays
- Coil: box with A1 (positive) and A2 (negative)
- Match coil voltage to control voltage (24V AC coil for 24V AC system)
- NO: gap in line, circuit broken until energized
- NC: no gap, circuit complete until energized
- Multiple poles per relay (R1/2 = relay 1, 2 poles)

### Gas Detection Safety Circuit
- Series chain: power supply → E-stop (NC) → thermal links (NC) → fire alarm signal
- Healthy: all closed → circuit complete → internal relay energizes → gas valve opens
- Fault: circuit broken → relay de-energizes → gas valve closes → "Safety Circuit Failed" light
- R1: fault relay. Pole 1 = safety circuit, Pole 2 = PLC input
- Thermal links in series: if one blows, whole chain breaks (can't tell which boiler — but priority is cutting gas)
- Sometimes NO vs NC not known until on site — red pen the drawing
