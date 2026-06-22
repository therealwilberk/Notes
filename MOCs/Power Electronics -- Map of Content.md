---
type: moc
tags: [moc, power-electronics, eee]
aliases: ["Power Electronics Notes", "PE MOC", "Power Electronics -- Map of Content"]
created: 2026-06-17
status: complete
---

# Power Electronics — Map of Content

Comprehensive refresher on power electronics: switching devices, converter topologies, control theory, magnetics, power supply design, motor drives, and system integration. Assumes prior EE knowledge. Compressed for revision, deep where it matters.

Reference textbooks: Mohan, Undeland & Robbins — *Power Electronics: Converters, Applications, and Design* (3rd ed); Erickson & Maksimovic — *Fundamentals of Power Electronics* (3rd ed); Rashid — *Power Electronics: Circuits, Devices, and Applications*.

## Core Modules

| # | Module | Description | Status |
|---|--------|-------------|--------|
| M1 | [[Notes/EEE/Power Electronics/pe-m1-switching-devices\|Switching Devices]] | Diodes, MOSFET, IGBT, SiC, GaN — physics, gate drive, switching loss | Complete |
| M2 | [[Notes/EEE/Power Electronics/pe-m2-non-isolated-dc-dc\|Non-Isolated DC-DC Converters]] | Buck, boost, SEPIC, Cuk, Zeta — CCM/DCM, component stress | Complete |
| M3 | [[Notes/EEE/Power Electronics/pe-m3-isolated-dc-dc\|Isolated DC-DC Converters]] | Flyback, forward, bridge, LLC, DAB — isolation, resonant, soft-switching | Complete |
| M4 | [[Notes/EEE/Power Electronics/pe-m4-ac-dc-pfc\|AC-DC Converters & PFC]] | Rectifiers, boost/bridgeless PFC, Vienna, harmonics standards | Complete |
| M5 | [[Notes/EEE/Power Electronics/pe-m5-dc-ac-inverters\|DC-AC Inverters]] | VSI, CSI, multilevel (NPC/FC/CHB), inverter PWM overview | Complete |
| M6 | [[Notes/EEE/Power Electronics/pe-m6-control-compensation\|Control & Loop Compensation]] | Averaged modeling, small-signal, Type II/III, digital control | Complete |
| M7 | [[Notes/EEE/Power Electronics/pe-m7-pwm-modulation\|PWM & Modulation Techniques]] | Carrier-based, SVPWM, SHE, DPWM, interleaving, spread spectrum | Complete |
| M8 | [[Notes/EEE/Power Electronics/pe-m8-magnetic-design\|Magnetic Design]] | Inductor/transformer design, core materials, skin/proximity, planar | Complete |
| M9 | [[Notes/EEE/Power Electronics/pe-m9-power-supply-design\|Power Supply Design]] | Topology selection, protection, hold-up, soft-start, pre-bias | Complete |
| M10 | [[Notes/EEE/Power Electronics/pe-m10-motor-drives\|Motor Drives]] | BLDC six-step, PMSM FOC, IM DTC, sensorless, traction inverters | Complete |
| M11 | [[Notes/EEE/Power Electronics/pe-m11-thermal-emc-layout\|Thermal, EMC & Layout]] | Loss calc, heatsinks, EMI filtering, PCB layout, panel/AutoCAD | Complete |

## Bonus Modules

| # | Module | Description | Status |
|---|--------|-------------|--------|
| M12 | [[Notes/EEE/Power Electronics/pe-m12-wide-bandgap\|Wide Bandgap Deep Dive]] | SiC/GaN structure, gate drive, packaging, reliability | Complete |
| M13 | [[Notes/EEE/Power Electronics/pe-m13-grid-renewables\|Grid Integration & Renewables]] | PV inverters, MPPT, PLL, anti-islanding, wind, storage, microgrids | Complete |

## Supplementary References

| Note | Description |
|------|-------------|
| [[Schematic Components -- Map of Content\|Schematic Components]] | Modular reference on relays, contactors, solenoids, breakers, fuses, signal transformers, switches, indicators, terminals — each with thinking patterns, mermaid diagrams, and traps |
