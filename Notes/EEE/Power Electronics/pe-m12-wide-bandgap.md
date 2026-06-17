---
tags: [power-electronics, wide-bandgap, sic, gan]
aliases: ["PE M12", "Wide Bandgap Deep Dive"]
parent: "[[Power Electronics -- Map of Content]]"
created: 2026-06-17
status: complete
---

# M12: Wide Bandgap Deep Dive

## Material Properties Comparison

| Property | Si | SiC (4H) | GaN |
|----------|-----|----------|------|
| Bandgap (eV) | 1.12 | 3.26 | 3.44 |
| Critical field (MV/cm) | 0.3 | 2.5-3.0 | 3.0-3.3 |
| Electron mobility (cm²/V·s) | 1500 | 900 | 2000 (2DEG) |
| Thermal conductivity (W/cm·K) | 1.5 | 4.9 | 1.3-2.0 (on Si substrate) |
| Max T_j (°C) | 150-175 | 200-250 | 150-175 (limited by packaging) |
| Baliga's FOM (rel. to Si) | 1 | 500-600 | >1000 |

The critical field advantage is the most important: a 600 V SiC MOSFET requires a drift region that is 10× thinner than a Si MOSFET with the same voltage rating → R_DS(on) is dramatically lower for the same die area.

## SiC MOSFET Deep Dive

### Structure

Vertical DMOS structure (similar to Si MOSFET). The drift region is epitaxial SiC. The gate oxide is the same SiO₂ (this limits the maximum gate voltage to 20-25 V, similar to Si).

**Channel mobility**: SiC MOSFETs have lower channel mobility than Si (~30 cm²/V·s vs 300+ for Si). This creates a "channel resistance" component that dominates at low voltage ratings. At high voltage (>1 kV), the drift resistance dominates and SiC's advantage is clear.

### Gate Drive Requirements

| Parameter | SiC MOSFET | Si MOSFET |
|-----------|------------|-----------|
| V_GS(on) | +15 V to +20 V | +10 V to +15 V |
| V_GS(off) | -5 V to -2 V | 0 V |
| V_GS(max) | -8 V to +25 V (check datasheet) | ±20 V |
| V_GS(th) | 2-4 V (positive TC) | 2-4 V |

**Trap**: SiC MOSFET gate oxide is more sensitive than Si — exceeding V_GS(max) even briefly can cause permanent degradation. The gate driver must have tight voltage regulation (±2% recommended). Paralleling SiC MOSFETs requires careful gate loop layout — one device's ringing can propagate to others.

### dV/dt and Cross-Talk

SiC MOSFETs switch at 10-50 V/ns. In a half-bridge configuration:

When the low-side switch turns off, the high-side switch's gate sees a current through C_GD: I_Miller = C_GD × dV/dt.

This current flows through the high-side gate loop impedance — if R_g(high-side) is high, the induced V_GS can exceed V_GS(th), turning on the high-side MOSFET and causing shoot-through.

**Mitigation**:
- Use a low-impedance gate drive with a dedicated Kelvin-source connection
- Apply a negative V_GS(off) (-5 V typical) to increase the headroom
- Add a gate-source capacitor (C_GS extra) to absorb the Miller current (but slows switching)
- Use a Miller clamp circuit that shorts the gate to source when V_GS drops below a threshold

### Paralleling

SiC MOSFETs have a positive temperature coefficient of R_DS(on) — they parallel naturally for DC. But switching behavior depends on device capacitance and gate threshold, which vary between devices.

**Parallel design rules**:
- Use MOSFETs from the same lot (matched V_GS(th) within 100 mV)
- Each device must have its own gate resistor (stops ringing between paralleled devices)
- Gate traces must be symmetric to the driver
- The power layout must be symmetric — asymmetric layout causes unequal current sharing during switching

## GaN HEMT Deep Dive

### Structure

Lateral device grown on a silicon (or SiC) substrate. The 2DEG channel forms at the AlGaN/GaN interface — no doping required. The gate is a Schottky contact in depletion-mode devices, or a p-GaN layer in enhancement-mode (e-mode) devices.

**E-mode vs D-mode**:

| | E-mode (p-GaN gate) | D-mode (HEMT) | Cascode (D-mode + Si LV FET) |
|---|---|---|---|
| Normally off? | Yes | No | Yes |
| V_GS(th) | 1.2-1.8 V | -10 to -20 V | 2-3 V (Si FET) |
| Gate drive | 0 to 6 V | -10 to +2 V | 0 to 12 V (Si FET) |
| Simplicity | Drop-in Si MOSFET replacement | Requires negative supply | Acts like Si MOSFET |

### Unique Characteristics

**No body diode**: GaN conducts reverse current through the 2DEG channel with V_SD(forward) ≈ 1.5-2.0 V. This is higher than a Si body diode (~0.7 V) but has zero reverse recovery (Q_rr = 0). In hard-switching half-bridges, the GaN HEMT's reverse conduction losses during deadtime can exceed the switching loss savings.

**Dynamic R_DS(on) — "current collapse"**: Under high-voltage stress, electrons can be trapped in the buffer layer, causing temporary R_DS(on) increase. Modern p-GaN gate structures and carbon-doped buffers have largely eliminated this, but it remains a consideration for reliability testing.

**Gate sensitivity**: Maximum V_GS for e-mode GaN is typically 6-7 V. The threshold is ~1.5 V — very low. The gate driver must have tight voltage regulation and low noise.

### Layout for GaN

The gate loop inductance must be <1 nH — any inductance on the gate path creates ringing that can exceed V_GS(max).

**Guidelines**:
- Place the gate driver within 2-3 mm of the GaN FET
- Use a solid ground plane on the layer below the gate loop
- Minimize the gate drive loop area: driver output → gate resistor → GaN gate → source → return to driver
- Use a via fence alongside the gate trace to provide a controlled impedance

Monolithic integration (driver + GaN FET in one package) solves the gate loop problem — this is the approach from Navitas (GaNFast), TI (LMG series), and others.

## Application Sweet Spots

| Application | Si | SiC | GaN |
|-------------|-----|-----|------|
| PFC (>1 kW) | — | Best | Good |
| PFC (<500 W) | — | Good | Best (totem-pole) |
| LLC (>1 kW) | — | Best | Good |
| LLC (<500 W) | — | Good | Best (high freq) |
| Traction inverter (400 V) | IGBT | Best (SiC MOSFET) | — |
| Traction inverter (800 V) | — | Best | — |
| OBC (3.3-22 kW) | — | Best (hard-switch) | Good (soft-switch) |
| Data center PSU | — | Good | Best (density) |
| Wireless power | — | — | Best |
| LED driver | — | — | Best (low power) |

## Reliability Considerations

| Failure mode | Si | SiC | GaN |
|-------------|-----|-----|------|
| Gate oxide TDDB | Well understood | Known (weaker oxide) | N/A (p-GaN) |
| Cosmic ray (SEB) | Well characterized | Better than Si | Not applicable (lateral) |
| HTRB (high temp reverse bias) | Mature | Good (>1000 hrs) | Good |
| Power cycling | Mature | Better (higher T_j) | Limited by packaging |
| dV/dt-induced failure | Rare | Occasional | Critical (low threshold) |

**Trap**: SiC MOSFET reliability at high dV/dt under repetitive pulsed conditions is an active research area. Gate oxide degradation accelerates with electric field (E_ox > 4 MV/cm). Ensure the gate drive voltage is within the datasheet recommended range at all times — including during transients.

## References
- Baliga, B.J. *Fundamentals of Power Semiconductor Devices*. Springer, 2008.
- EPC. *AN002: Fundamentals of Gallium Nitride Power Transistors*.
- Renesas. "Wide Bandgap Power Switches for Hard- and Soft-Switching Applications." CS MANTECH, 2025.
- Navitas Semiconductor. "Systematic Approach to GaN Power IC Reliability." APEC 2019.
- SemiEngineering. "GaN Power Devices Power Up." 2026.
- Fraunhofer IZM. "Power Module Design for GaN Transistors Enabling High Performance." 2025.
