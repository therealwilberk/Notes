---
tags: [eee, bms, controls, wiring-diagrams, electrical-schematics]
aliases: ["BMS Panel Training", "Reading Electrical Diagrams"]
parent: "[[MOC-AutoCAD-Schneider]]"
created: 2026-05-30
status: in-progress
video: "https://www.youtube.com/watch?v=XzoVXOIvzVs"
progress: "0:00 - 20:24"
---

# Reading Electrical Schematics — BMS Controls Training

> [!info] Source
> 6-hour training from a real-world BMS control and automation project. Originally a paid 5-day course. Instructor walks through actual schematics from an electrical contractor.

> [!tip] Download the schematics
> Link in the video description. You need them in front of you while watching.

---

## Key Takeaway (so far)

> [!quote] RTFM — Read The Manual
> "People think controls people are wizards. We're not. We just read the manual." Everything has a manual. If you want to progress into controls, read the manual for every piece of equipment. You can't design around something you don't understand.

---

## 1. Panel Layout Basics

- **Horizontal line on every page** = divider between what's **inside** the panel and what's **outside** (field equipment)
- Not all schematics are drawn the same way. Designer preferences, software differences, etc.
- What matters isn't the layout — it's understanding **how it works**

> [!warning] Schematic ≠ Physical wiring
> How things are drawn in the schematic isn't necessarily how they're wired physically. A panel builder can wire it differently as long as it does the same thing.

---

## 2. Power Supply & Distribution (230V Side)

### Supply
- **Single phase, 50Hz, 230V**
- Comes into panel → hits the **isolator switch** (the handle on the outside of the panel, shaft goes into the disconnector switch inside)

### Distribution
- From isolator → **busbar** (same principle as a consumer unit)
- 10mm cable from main isolator to busbar + first MCB
- Power distributed across all MCBs via the busbar
- Neutral via a **neutral block**

### MCB Assignments
| MCB | Type | Load |
|-----|------|------|
| MCB 2 | D-type, 6A | Primary side of transformer |
| MCB 3 | — | Laptop socket |
| MCB 4 | — | Gas detection system (constant 230V feed) |

- All field equipment should have a **local isolator** as well
- MCB 4 feeds terminal block 1, then out to field equipment

---

## 3. Transformer & Controls (24V Side)

### Why step down?
- **Safety.** 230V on the panel door (switches, lights, indicators) is dangerous
- Touch voltage threshold = 50V → that's why we use 24V AC for controls
- Most BMS systems use a transformer (not a DC power supply), though either works

### 0V Distribution
- From transformer secondary → 0V rail
- Distributed via **Wago terminal blocks** with a push-in busbar
- NOT daisy-chained in series (one fault takes out everything)
- Multiple terminal blocks provide **redundancy** and easier fault-finding

### 24V AC Distribution
- From transformer → **MCB or fuse** first (protection)
- Then distributed to control circuits

---

## 4. Circuit Numbering System

This is the key to reading any schematic:

> [!important] The numbering rule
> Circuits are numbered based on what MCB they come from. The number **changes** every time the circuit passes through a device (switch, relay contact, light, push button).

- **100 circuit** = everything directly from the MCB, before any device
- Once it passes through a device → becomes a new circuit number (e.g., **400**, **200**)
- Example: 24V from MCB → through lamp test push button → now it's the **400 circuit**

### The Lamp Test Circuit
- **Normally open push button** (black, on panel front)
- When pressed: sends power to ALL indicator lamps simultaneously
- Purpose: quick visual check that all lamps work
- If one doesn't light → there's a problem that might have gone unnoticed
- Modern panels should also have **PLC inputs** doubling up the lamp indicators (for HMI/email/app alerts)

---

## 5. Relay Basics (How They're Drawn)

### Coil Side
- Drawn as a **box** with **A1** (positive) and **A2** (negative)
- A1/A2 + box = tells you it's the coil side
- **Match the coil voltage to your control voltage** (24V AC coil for 24V AC system)

### Contact Side
- **Normally Open (NO):** gap in the line — circuit is broken until relay energizes
- **Normally Closed (NC):** no gap — circuit is complete until relay energizes
- Each relay can have multiple **poles** (e.g., R1/2 = relay 1, 2 poles)

---

## 6. Gas Detection System — Safety Circuit

### The Run-Enable / Safety Circuit
All these are in **series** (one breaks → whole circuit fails):

1. **Power supply** from gas detection system (likely DC, ~24V or lower)
2. **Emergency stop button** (NC) — in plant room
3. **Thermal links** on boilers (NC) — fuse at high temp, both boilers in series
4. **Fire alarm signal** (if integrated)

### How It Works (Healthy State)
1. All devices closed → circuit complete → signal returns to gas detection system
2. Energizes an **internal relay** in the gas detection system
3. Internal relay closes a contact → **opens the gas valve** (allows gas into system)
4. Also drives relay outputs:
   - **R1** = generic fault relay (pole 1: safety circuit, pole 2: PLC input)
   - When healthy: R1 energized → contact switches from NC to NO → safety circuit enabled

### How It Works (Unhealthy State)
1. Panic button hit OR thermal link blown → circuit broken
2. Internal relay de-energizes
3. Gas valve closes (no gas into system)
4. R1 de-energized → contact stays on NC side → **"Safety Circuit Failed" light** comes on

> [!note] Thermal links in series
> Both boilers' thermal links are in series. If one blows, you won't know *which* boiler — but it doesn't matter. The thermal links trigger from heat/fire, so the priority is cutting gas, not identifying which boiler.

### Relay Logic Summary
| State | R1 Coil | R1 Contact | Result |
|-------|---------|------------|--------|
| All healthy | Energized | NO side (safety circuit) | Gas valve open, system runs |
| Fault (E-stop, thermal link, gas detected) | De-energized | NC side (failed light) | Gas valve closed, "Safety Circuit Failed" lit |

---

## 7. Design Reality Check

> [!warning] NO vs NC on site
> Sometimes you don't know if a contact should be NO or NC until you're physically on site. The designer picks what seems right, and the installer may need to invert it. **Red pen the drawing** to mark what actually got installed.

- Thermal links in parallel vs series: parallel lets you identify which boiler, but series is simpler and the priority is cutting the gas solenoid anyway
- Boiler fault outputs exist separately for individual diagnostics

---

## What's Next (after 20:24)

The video continues into:
- Carbon monoxide / gas sensor details
- More relay circuits on page 2
- Boiler control circuits
- PLC integration

> [!todo] Continue watching
> - [ ] 20:24 - 40:00
> - [ ] 40:00 - 1:00:00
> - [ ] Continue building notes as you go
