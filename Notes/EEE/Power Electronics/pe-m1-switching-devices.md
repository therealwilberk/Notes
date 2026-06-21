---
tags: [power-electronics, switching-devices, semiconductors]
aliases: ["PE M1", "Switching Devices"]
parent: "[[Power Electronics -- Map of Content]]"
created: 2026-06-17
status: complete
---

# M1: Switching Devices

## Power Diodes

Three main types distinguished by reverse recovery behavior:

| Type | Recovery | trr | Use |
|------|----------|-----|-----|
| Standard (PN) | Slow, snap-off | >1 µs | 50/60 Hz rectification |
| Fast recovery | Soft recovery | 50-500 ns | High-frequency rectifiers, snubbers |
| Schottky | Majority carrier, no stored charge | ~0 (no trr) | Low-voltage (<200 V), high-frequency |

**Reverse recovery**: stored charge in the depletion region must be removed before the diode blocks reverse voltage. In hard-switching converters, reverse recovery current causes additional loss and EMI. Schottky diodes eliminate this — no minority carriers.

**Trap**: Snappy recovery diodes cause voltage ringing. Always specify soft recovery for snubber and boost diodes in hard-switching topologies.

## Power MOSFET

Voltage-controlled device. Enhancement-mode N-channel is the standard power switch.

**Key static parameters:**
- $R_{DS(on)}$: on-resistance, increases with temperature (positive TC — good for paralleling)
- $V_{GS(th)}$: gate threshold, typically 2-4 V
- $B_{VDS}$: breakdown voltage
- $C_{iss}$, $C_{rss}$, $C_{oss}$: input, reverse transfer (Miller), output capacitances

**Switching behavior:**
- Turn-on: $V_{GS}$ charges $C_{iss}$ to $V_{GS(th)}$ → $I_D$ rises → Miller plateau ($V_{GS}$ constant, $V_{DS}$ falls) → ohmic region
- Turn-off: Miller plateau in reverse, $C_{iss}$ discharges
- Switching loss: $E_{on} + E_{off} = \int v_{DS}(t) \, i_D(t) \, dt$ — see [[pe-m6-control-compensation]] for compensation implications

**Miller effect**: $C_{rss}$ ($C_{GD}$) creates feedback from drain to gate. During the Miller plateau, $V_{GS}$ is clamped while $V_{DS}$ changes. High $dV/dt$ at the drain injects current back into the gate circuit — can cause spurious turn-on. Mitigate with low-impedance gate drive and Kelvin-source connection.

**Trap**: MOSFETs can be turned on parasitically by high $dV/dt$ through $C_{GD}$. If the gate driver impedance is high, the induced gate voltage may exceed $V_{GS(th)}$. Use a gate-source resistor (10 kΩ typical) and/or a negative gate drive voltage for SiC.

**Body diode**: integral P-N diode in every power MOSFET. Slow recovery (typically), use external Schottky in parallel if body diode conducts in the topology (e.g., half-bridge). See [[pe-m5-dc-ac-inverters]] for inverter body diode considerations.

## Superjunction (CoolMOS) MOSFET

Superjunction (SJ) MOSFETs use alternating p-type and n-type columns in the drift region to achieve a 3D charge balance. This allows a higher doping concentration in the drift region for a given breakdown voltage, dramatically reducing $R_{DS(on)}$ compared to planar/standard MOSFETs.

**Key characteristics:**
- Typical voltage range: 600–900 V
- $R_{DS(on)}$ ~50–70% lower than planar for the same die size
- Higher $C_{rss}$ (Miller capacitance) — slower switching than WBG but better than standard MOSFET

**Applications:** PFC stages, LLC converters, and high-end power supplies.

**Key manufacturers:**
- Infineon — CoolMOS (C7, P7, CFx series)
- STMicroelectronics — MDmesh (M2, M5, K5 series)
- OnSemi — SuperFET (FRFET, Easy Drive series)

## IGBT

Voltage-controlled, minority carrier device. Combines MOSFET gate with BJT output.

| Characteristic | MOSFET | IGBT |
|---------------|--------|------|
| Conduction loss | $I^2 R_{DS(on)}$ — high at high $V_{BR}$ | $V_{CE(sat)} I$ — lower at high voltage |
| Switching speed | Fast (ns) | Slower — tail current |
| Tail current | None | Minority carriers must recombine at turn-off |
| Paralleling | Easy (positive TC) | Harder (positive TC only at high current) |
| Typical range | <600 V, high freq | >600 V, <50 kHz |

**Trap**: IGBTs have a latch-up region at high dV/dt. Never exceed the RBSOA (reverse bias safe operating area). At turn-off, the collector current "tails" — the longer the tail, the higher the turn-off loss. Use punch-through (PT) or field-stop (FS) IGBTs for lower tail current.

## SiC MOSFET

Wide bandgap (3.26 eV vs 1.12 eV for Si). See [[pe-m12-wide-bandgap]] for a detailed comparison of WBG materials. Key advantages over silicon MOSFET:

- Higher breakdown field (10×) → thinner drift region → lower $R_{DS(on)}$ for same $V_{BR}$
- Higher thermal conductivity (4.9 W/cm·K vs 1.5 W/cm·K)
- Higher junction temperature rating (200°C+)
- Lower switching losses — faster $dV/dt$ (up to 50 V/ns)

**Gate drive considerations:**
- $V_{GS}$ range: typically $-5$ V to $+20$ V (check datasheet — tighter than Si MOSFET)
- Recommended $V_{GS(on)}$: $+15$ V to $+20$ V
- Recommended $V_{GS(off)}$: $-5$ V to $-2$ V (to prevent $dV/dt$-induced turn-on)
- Gate loop inductance must be minimized — ringing on $V_{GS}$ can destroy the gate oxide

**Trap**: SiC MOSFETs switch very fast. High $dV/dt$ couples through $C_{GD}$ to the gate. Without negative gate drive, the Miller current can raise $V_{GS}$ above threshold and cause shoot-through in a half-bridge. Use a Kelvin-source connection or a dedicated source-sense pin.

## GaN HEMT

Wide bandgap (3.44 eV). See [[pe-m12-wide-bandgap]] for detailed GaN physics and device structure. Enhancement-mode (e-mode) GaN HEMTs are normally off, depletion-mode (d-mode) are normally on (require cascode with Si MOSFET).

**2DEG (2-dimensional electron gas):** forms at the AlGaN/GaN heterojunction interface. Electron mobility $>2000$ cm²/V·s — nearly 2× Si. No doping required.

**Key differences from Si MOSFET:**

| Property | Si MOSFET | SiC MOSFET | GaN HEMT |
|----------|-----------|------------|----------|
| Bandgap (eV) | 1.12 | 3.26 | 3.44 |
| Mobility (cm²/V·s) | 1500 | 900 | 2000+ |
| $V_{GS}$ range | $\pm 20$ V | $-5$ to $+25$ V | $-10$ to $+7$ V (e-mode) |
| $Q_g$ (typical 650 V, 30 A) | $\sim 60$ nC | $\sim 45$ nC | $\sim 6$ nC |
| Reverse recovery | Slow body diode | Fast body diode | No body diode |
| $dV/dt$ capability | $<10$ V/ns | $<50$ V/ns | $<150$ V/ns |

**No body diode**: GaN HEMTs conduct reverse current through the 2DEG channel when $V_{GS}$ is off — essentially a "reverse conduction" mode with $V_{SD}$ drop (~2 V). No reverse recovery charge. Deadtime power loss can be higher than Si because of the higher $V_{SD}$ drop.

**Gate drive is critical**:
- e-mode GaN: $V_{GS(max)}$ is typically 6-7 V. A ringing spike above this kills the device.
- Gate loop inductance must be $<1$ nH — monolithic integration of driver + GaN FET (e.g., Navitas GaNFast) solves this.
- Use a GaN-specific gate driver with tight voltage regulation.

**Trap**: e-mode GaN HEMTs have a normally off threshold of $\sim 1.5$ V. This is low — layout noise can cause false turn-on. Never leave the gate floating. Always use a pulldown resistor (10 kΩ or lower).

## References

- Mohan, Undeland & Robbins. *Power Electronics: Converters, Applications, and Design*. 3rd ed. Ch 1-6, 19-20.
- Baliga, B.J. *Fundamentals of Power Semiconductor Devices*. Springer, 2008.
- EPC Corporation. *AN002: Fundamentals of Gallium Nitride Power Transistors*. Application Note.
- Lidow, A. et al. *GaN Transistors for Efficient Power Conversion*. 3rd ed. Wiley, 2019.
- Renesas. "Wide Bandgap Power Switches for Hard- and Soft-Switching Applications." CS MANTECH, 2025.
