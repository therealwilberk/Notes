---
tags: [harmonics, power-quality, fundamentals]
aliases: ["Harmonics Fundamentals", "THD", "Harmonic Order"]
parent: "[[Harmonics -- Map of Content]]"
created: 2026-06-27
status: complete
---

# M1: Harmonics Fundamentals

## What a Harmonic Is

A harmonic is a sinusoidal component whose frequency is an integer multiple of the fundamental frequency. In a 50 Hz system, the 3rd harmonic is 150 Hz, the 5th is 250 Hz, and so on.

Any periodic, non-sinusoidal waveform can be decomposed into a sum of sinusoids at integer multiples of the fundamental frequency — this is the Fourier series:

$$
v(t) = V_0 + \sum_{h=1}^{\infty} V_h \sin(h \omega_0 t + \phi_h)
$$

Where:
- $h$ = harmonic order
- $V_0$ = DC component
- $V_h$ = magnitude of the $h$th harmonic
- $\omega_0$ = fundamental angular frequency ($2\pi f_0$)

A purely sinusoidal waveform has only the fundamental ($h = 1$). Any deviation from a sine wave means harmonics exist.

## Harmonic Order Classification

| Group | Orders | Characteristic |
|-------|--------|----------------|
| Odd non-triplen | 5th, 7th, 11th, 13th... | Produced by 6-pulse rectifiers ($6n \pm 1$) |
| Triplen | 3rd, 9th, 15th, 21st... | Odd multiples of 3 — zero-sequence behavior |
| Even | 2nd, 4th, 6th... | Indicate asymmetry, half-wave rectification, or DC offset |
| Interharmonics | Non-integer multiples | Produced by cycloconverters, arc furnaces, some VFDs |

Odd harmonics dominate in practice because most nonlinear loads are symmetrical — they produce the same waveform in both half-cycles, which eliminates even harmonics by symmetry.

## Key Metrics

### Total Harmonic Distortion (THD)

The ratio of harmonic energy to fundamental energy, expressed as a percentage:

$$
THD_V = \frac{\sqrt{\sum_{h=2}^{\infty} V_h^2}}{V_1} \times 100\%
$$

$$
THD_I = \frac{\sqrt{\sum_{h=2}^{\infty} I_h^2}}{I_1} \times 100\%
$$

THD is the most common power quality metric. A THD of 0% means a pure sine wave.

### Total Demand Distortion (TDD)

Current THD normalized to the maximum demand load current ($I_L$) rather than the fundamental of the measured current:

$$
TDD = \frac{\sqrt{\sum_{h=2}^{\infty} I_h^2}}{I_L} \times 100\%
$$

TDD is preferred over THD for compliance (IEEE 519) because it prevents gaming — a lightly loaded system with high THD but low absolute harmonic current still passes if TDD is within limits.

### Harmonic Spectrum

A bar chart of $I_h$ (or $V_h$) vs harmonic order $h$. More informative than a single THD number because specific orders matter for resonance, transformer heating, and filter design.

### Power Factor and Harmonics

True power factor has two components:

$$
PF_{true} = PF_{displacement} \times PF_{distortion}
$$

$$
PF_{distortion} = \frac{I_1}{I_{RMS}} = \frac{1}{\sqrt{1 + THD_I^2}}
$$

A load with perfect displacement PF (no phase shift) but heavy harmonics still has poor true PF. This is why PFC circuits address both phase shift and current shaping.

## Relationship Between Voltage and Current Harmonics

Harmonic currents are drawn by the load. These currents produce harmonic voltage drops across the system impedance:

$$
V_h = I_h \times Z_{sys}(h)
$$

where $Z_{sys}(h)$ is the system impedance at harmonic order $h$, including transformer leakage reactance, cable impedance, and source impedance.

Three implications:

- **Voltage distortion follows current distortion.** The same load produces worse voltage THD on a weak (high-impedance) system than on a stiff (low-impedance) system.
- **Parallel resonance.** If a capacitive bank resonates with system inductance at a harmonic frequency, $Z_{sys}(h)$ peaks and voltage distortion spikes.
- **Series resonance.** A low-impedance path at a harmonic frequency can trap harmonic current, causing large circulating currents.

## Why Harmonics Are a Growing Problem

Three long-term trends drive harmonic proliferation:

| Trend | Mechanism |
|-------|-----------|
| Power electronics proliferation | VFDs, SMPS, LED drivers, EV chargers, PV inverters — all nonlinear |
| Efficiency-driven design | Lower conduction angles mean higher peak currents and more distortion |
| Weaker grids at connection points | Distributed generation and longer feeders increase supply impedance |

## References

- IEEE 519-2022. *IEEE Standard for Harmonic Control in Electric Power Systems.*
- IEC 61000-2-4:2024. *Electromagnetic compatibility (EMC) — Compatibility levels in industrial plants.*
- Mohan, Undeland & Robbins. *Power Electronics.* 3rd ed. Ch 5-6.
- Arrillaga, J. & Watson, N.R. *Power System Harmonics.* 2nd ed. Wiley, 2003.
