---
tags: [harmonics, generation, nonlinear-loads, rectifiers]
aliases: ["Harmonic Sources", "Nonlinear Load Harmonics"]
parent: "[[Harmonics -- Map of Content]]"
created: 2026-06-27
status: complete
---

# M2: Harmonic Generation & Sources

## The Nonlinear Load

A linear load draws current proportional to voltage (Ohm's law applies). A nonlinear load draws current that is not proportional — the current waveform differs in shape from the voltage waveform.

The distinction is waveform shape, not magnitude. An induction motor is linear (current is sinusoidal at a lagging phase angle). A VFD input stage is nonlinear (current is pulsed even though the average power is similar).

### Why Nonlinearity Produces Harmonics

A sine wave through a linear impedance produces a sine wave. A sine wave through a nonlinear impedance (diode, thyristor, saturated core) produces a distorted wave. The Fourier decomposition of that distorted wave contains harmonics.

The same principle applies in reverse — a nonlinear load injecting harmonic currents causes harmonic voltage drops across every series impedance between the load and the source.

## Six-Pulse Diode Bridge Rectifier

The most common harmonic source in industry. A three-phase diode bridge conducts in 60-degree pulses — only two diodes conduct at any instant, and conduction switches every 60 degrees when a new pair of diodes becomes forward-biased.

The resulting DC-side voltage has 6 ripple pulses per cycle (hence "six-pulse"). The AC-side current is a stepped waveform.

**Characteristic harmonics:** $h = 6n \pm 1$ (5th, 7th, 11th, 13th, 17th, 19th...)

**Typical magnitudes** (relative to fundamental, ideal six-pulse):

| Order | $I_h / I_1$ |
|-------|-------------|
| 5th | ~20% |
| 7th | ~14% |
| 11th | ~9% |
| 13th | ~8% |

**THD:** ~30% without any input reactor.

**Trap:** The 5th harmonic rotates opposite to the fundamental (negative sequence). In a motor, the 5th harmonic produces a counter-rotating MMF that opposes the fundamental torque and causes additional heating.

## Twelve-Pulse Rectifier

Two six-pulse bridges fed from phase-shifted windings — one wye, one delta. The 30-degree phase shift between the two transformer secondaries causes 5th and 7th harmonic currents to cancel at the primary.

**Characteristic harmonics:** $h = 12n \pm 1$ (11th, 13th, 23rd, 25th...)

**THD:** ~10-15%

Higher pulse counts scale the same way — 18-pulse produces $18n \pm 1$, 24-pulse produces $24n \pm 1$. Each step eliminates the next lowest harmonic family.

**Trap:** Cancellation depends on equal load sharing between bridges and balanced supply voltages. Imbalance degrades cancellation — 5th and 7th harmonics reappear.

## Variable Frequency Drives (VFDs)

Most VFDs use a six-pulse diode front end followed by a DC link and IGBT inverter stage. The diode bridge is the harmonic source. The inverter stage switching frequency (2-16 kHz) produces high-frequency EMI, not power system harmonics (which are below 2.5 kHz for the 50th harmonic at 50 Hz).

VFD harmonic current depends on:
- DC link reactor (or lack thereof)
- AC line reactor (% impedance)
- Load on the motor
- Number of drives sharing a bus

**Trap:** A VFD on a backup generator produces worse voltage distortion than on a stiff utility feed because the generator has higher subtransient reactance — the same harmonic current produces a larger voltage drop. Generator sizing must account for this. IEEE 519-2022 clarifies that TDD limits for genset-backed drives are not required to meet the same 5% limits as utility-connected installations.

## Switch-Mode Power Supplies (SMPS)

Single-phase rectifier + capacitor filter. The diodes conduct only near the voltage peak — short, high-amplitude current pulses.

**Characteristic harmonics:** All odd harmonics, dominated by 3rd (triplen).

**THD:** 80-150% (uncorrected). A 100 W SMPS can have THD over 100% — the current waveform is closer to an impulse train than a sine wave.

Active PFC (boost PFC) shapes the input current to follow the voltage, reducing THD below 10%. Most modern power supplies over 75 W include PFC to comply with IEC 61000-3-2.

## LED Lighting

LED drivers are SMPS-derived. Low-cost drivers omit PFC, producing THD of 50-120%. High-quality drivers include active PFC with THD < 15%.

**Trap:** Large LED retrofits in commercial buildings can cause neutral overloads from accumulated 3rd harmonic current, even though each individual fixture is low power. The neutral current from hundreds of LED drivers can exceed phase current.

## Arc Furnaces

Extreme nonlinearity — the arc voltage-current characteristic has negative resistance. Current is highly distorted and varies cycle-to-cycle.

**Harmonic spectrum:** Broad, including interharmonics and even harmonics due to asymmetry in the arc. 2nd, 3rd, 4th, 5th all present at significant levels.

Arc furnaces require dedicated filtering (typically tuned passive banks + active filters) and often have their own transmission-level feed to isolate flicker and harmonics from other users.

## PV Inverters

Grid-tied inverters inject harmonic currents as a byproduct of PWM switching and grid synchronization.

**Characteristic harmonics:** Varies by topology. Two-level inverters produce switching-frequency sidebands. Multilevel inverters (NPC, CHB) produce lower harmonics at the AC side due to stepped voltage waveforms.

**Emerging issue:** PV inverters can amplify certain harmonics through interaction with grid impedance — especially the 15th, 21st, and other high-order harmonics. This is a growing concern as PV penetration increases in LV networks.

**Trap:** Anti-islanding detection circuits can misinterpret harmonic levels. Some inverter controls intentionally inject harmonic current for impedance measurement, which can conflict with other mitigation systems on the same network.

## EV Chargers

EV chargers use switch-mode rectification with power levels from 3.7 kW (single-phase AC) to 350 kW (DC fast charging).

Single-phase chargers produce 3rd harmonic (triplen). Three-phase chargers produce 5th, 7th, 11th, 13th. Fast DC chargers use active front ends (AFE) with THD < 5%. Lower-cost AC chargers may not.

**Evening peak coincidence:** Residential EV charging concentrates in the evening when lighting and entertainment loads are also active. Cumulative harmonic distortion at the distribution transformer can exceed limits during these windows.

## Summary by Source

| Source | Dominant Harmonics | Typical THD_I | Notes |
|--------|-------------------|---------------|-------|
| 6-pulse rectifier (no reactor) | 5th, 7th, 11th, 13th | 30-40% | Most common industrial source |
| 6-pulse + 3% line reactor | Same orders, reduced | 25-33% | Standard VFD configuration |
| 12-pulse rectifier | 11th, 13th | 10-15% | Requires phase-shifting transformer |
| Single-phase SMPS (no PFC) | 3rd, 5th, 7th | 80-150% | Computers, small electronics |
| SMPS with PFC | 3rd (residual) | <10% | Modern equipment >75 W |
| LED driver (low-cost) | 3rd, 5th, 7th | 50-120% | Retrofits, residential |
| LED driver (premium) | Residual high-order | <15% | Commercial spec-grade |
| Arc furnace | Broad (2nd-7th) | Highly variable | Dedicated feed required |
| PV inverter | 5th, 7th, 11th + sidebands | <5% (modern) | Interaction with grid impedance |
| EV charger (AC) | 3rd (single-phase) / 5th, 7th (3-phase) | 10-30% | Depends on charger class |

## References

- IEEE 519-2022. *Harmonic Control in Electric Power Systems.* Annex C (sources).
- Mohan, Undeland & Robbins. *Power Electronics.* 3rd ed. Ch 5-6.
- Hoevenaars, T. *Comparing Harmonics Mitigation Techniques.* Comsys/IEEE.
- Energies 14(12), 2021. *Impact of Harmonic Currents of Nonlinear Loads on Power Quality of a Low Voltage Network.*
