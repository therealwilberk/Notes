---
tags: [power-electronics, inverters, dc-ac]
aliases: ["PE M5", "DC-AC Inverters"]
parent: "[[Power Electronics -- Map of Content]]"
created: 2026-06-17
status: complete
---

# M5: DC-AC Inverters

## Voltage Source Inverter (VSI)

Most common inverter type. DC input voltage is fixed; the inverter synthesizes an AC voltage of variable magnitude and frequency. Requires a stiff DC bus (low impedance).

**Single-phase half-bridge**: two switches, output swings between +V_dc/2 and -V_dc/2. The DC bus requires a center tap — two capacitors in series provide the midpoint.

**Single-phase full-bridge (H-bridge)**: four switches. Output swings between +V_dc and -V_dc — double the voltage swing of the half-bridge for the same DC bus.

**Three-phase VSI**: six switches (three legs). Each leg produces a square wave 120° apart. The line-to-line voltage is √3 × the phase voltage.

## Current Source Inverter (CSI)

Input is a stiff DC current source (large inductor). Output current is switched between phases. Less common than VSI — requires a large DC link inductor, and the switches must block reverse voltage (series diode with each switch).

**Use**: high-power motor drives where the DC bus is already current-fed, superconducting magnetic energy storage, some grid-tie applications.

## Multilevel Inverters

Generate output voltage with three or more levels — reduces harmonic content and voltage stress on switches.

### Neutral Point Clamped (NPC)

Also called diode-clamped. A 3-level NPC uses two series capacitors (creating a neutral point) and clamping diodes to limit switch voltage stress to V_dc/2.

| Level count | Switches | Clamping diodes | Capacitors |
|------------|----------|-----------------|------------|
| 3-level | 4 | 2 | 2 |
| 5-level | 8 | 12 | 4 |

**Challenge**: neutral point voltage balancing — the midpoint voltage drifts if the upper and lower capacitors are not equally charged. Space vector modulation with redundant switching states can balance the NPC.

### Flying Capacitor (FC) Inverter

Also called capacitor-clamped. Uses floating capacitors instead of clamping diodes. The capacitors are charged to intermediate voltage levels — more flexible than NPC but requires capacitor pre-charging and balancing.

**Advantage**: phase redundancy — multiple switch states produce the same output voltage, enabling capacitor balancing.

**Disadvantage**: the number of capacitors grows rapidly with level count. Startup pre-charge is required.

### Cascaded H-Bridge (CHB)

Each phase is built from multiple H-bridge cells with isolated DC sources. Most modular of the multilevel topologies — each cell is identical.

**Use**: STATCOM, medium-voltage drives, battery storage systems (each cell is a separate battery pack). The most practical for high-level counts (>7 levels).

**Trap**: Each H-bridge needs its own isolated DC source. This is straightforward for battery systems and solar (each panel has its own DC source) but requires a multi-winding transformer with separate rectifiers for general use.

## Modulation (Overview — see [[pe-m7-pwm-modulation]] for detail)

| Scheme | THD | DC utilization | Complexity |
|--------|-----|----------------|------------|
| Square wave | 30-45% | Highest (no loss) | Simplest |
| Sinusoidal PWM (SPWM) | ~5% | 78.5% (V_out/V_dc = m/2) | Simple |
| Third harmonic injection | ~4% | 90.7% (V_out/V_dc = m/√3) | Moderate |
| Space vector PWM (SVPWM) | ~4% | 90.7% (same as 3rd harmonic) | Moderate |
| Selective harmonic elimination (SHE) | Very low | Depends on N | Complex |

## Trap: Deadtime and Distortion

Deadtime is required between complementary switch turn-on/turn-off to prevent shoot-through. During deadtime, neither switch conducts — the output voltage depends on the direction of the load current (freewheeling through body diodes). This causes:

- Voltage distortion (deadtime effect)
- Low-frequency harmonics
- Reduced fundamental voltage

Compensation: measure current polarity and adjust the PWM timing to compensate for the deadtime voltage error. Most modern motor drive controllers include deadtime compensation.

## References

- Mohan, Undeland & Robbins. *Power Electronics*. 3rd ed. Ch 8, 15-16.
- Rashid, M.H. *Power Electronics: Circuits, Devices, and Applications*. 4th ed. Ch 8-9.
- Franquelo, L.G. et al. "The Age of Multilevel Converters Arrives." IEEE Industrial Electronics Magazine, 2008.
- MDPL Energies. "A Comprehensive Review on Space Vector Based-PWM Techniques for CMV Mitigation in PV Multi-Level Inverters." 2024.
