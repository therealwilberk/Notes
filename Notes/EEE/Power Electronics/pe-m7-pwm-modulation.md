---
tags: [power-electronics, pwm, modulation]
aliases: ["PE M7", "PWM & Modulation"]
parent: "[[Power Electronics -- Map of Content]]"
created: 2026-06-17
status: complete
---

# M7: PWM & Modulation Techniques

## Carrier-Based PWM

The output of the compensator (control voltage v_c) is compared to a fixed-frequency carrier (typically a triangle or sawtooth) to generate the gate signals.

### Leading-Edge / Trailing-Edge / Triangle Modulation

| Modulation | Switch turn-on | Switch turn-off | Used in |
|------------|---------------|-----------------|---------|
| Trailing-edge | Carrier valley | Compare match | Voltage-mode control |
| Leading-edge | Compare match | Carrier peak | Current-mode control (alt) |
| Triangle (center-aligned) | Both edges symmetric | Both edges symmetric | Voltage-mode, inverters |

**Trap**: The PWM resolution (number of clock cycles per switching period) limits the achievable minimum duty cycle. For a 2 MHz switching frequency and a 200 MHz MCU clock: 100 clock cycles per period → ~1% duty resolution. Use high-resolution PWM (HRPWM) for fine adjustment.

### Naturally Sampled vs Uniformly Sampled

**Naturally sampled**: analog comparison — the control voltage varies continuously. Produces lower harmonic distortion but requires analog implementation.

**Uniformly sampled**: the control voltage is sampled at the carrier peak (or valley) and held for the entire half-cycle. Used in digital controllers. Produces slightly higher harmonic distortion than naturally sampled — the difference is negligible for most applications.

### Third Harmonic Injection

Adds 1/6 of the third harmonic (at 3× fundamental) to a sinusoidal reference. Reduces the peak of the modulating waveform by ~15.5%, allowing a higher fundamental amplitude before overmodulation.

Result: the maximum modulation index increases from 1.0 (SPWM, 78.5% DC utilization) to 1.15 (90.7% DC utilization). Equivalent to SVPWM.

Implementation: v_inj = v_ref + 1/6 × sin(3 × θ). Or simpler: v_inj = v_ref + 1/4 × (v_a - v_c) × (v_c - v_b) — the min-max injection method.

## Space Vector PWM (SVPWM)

The three-phase voltage is represented as a single rotating vector in the αβ-plane (Clarke transform). The inverter has 2³ = 8 switching states: 6 active vectors and 2 zero vectors.

**Implementation**:
1. Determine the sector (1-6) containing the reference vector V_ref
2. Calculate dwell times for the two adjacent active vectors (T1, T2) and zero vectors (T0)
3. T1 = m × sin(60° - θ) × T_sw, T2 = m × sin(θ) × T_sw, T0 = T_sw - T1 - T2
4. Generate the switching sequence (symmetric: 0-1-2-7-2-1-0 for each sector)

**Advantages over SPWM**:
- 15% higher DC bus utilization (same as 3rd harmonic injection)
- Lower THD for the same switching frequency
- Well-suited to digital implementation

**Discontinuous PWM (DPWM)**: clamps one phase to the DC rail for 60° of each cycle, reducing switching losses by 33%. The clamped phase contributes no switching loss during that interval. Various DPWM variants (DPWM1, DPWM2, DPWM3, DPWMMAX, DPWMMIN) differ in which phase is clamped and when.

| Variant | Clamping duration | Best for |
|---------|------------------|----------|
| CPWM (continuous) | None | Lowest THD |
| DPWM1 | 60° at voltage peak | Unity PF applications |
| DPWM2 | 30° before/after zero cross | Lagging PF |
| DPWM3 | Split between peak/zero | General |

## Selective Harmonic Elimination (SHE-PWM)

Pre-calculates switching angles to eliminate specific low-order harmonics (5th, 7th, 11th, etc.) while controlling the fundamental amplitude. N switching angles can eliminate (N-1) harmonics.

**Advantages**: very low THD at low switching frequencies, suitable for high-power GTO/IGCT converters where switching frequency is limited to a few hundred Hz.

**Disadvantages**: requires offline calculation of switching angles (transcendental equations), lookup tables for different modulation indices, poor transient response.

## Multilevel PWM

### Phase-Shifted PWM (PS-PWM)

Each cell in a cascaded H-bridge or flying capacitor converter uses the same carrier frequency but shifted by 360°/N (where N is the number of cells). Creates effective switching frequency of N × f_sw at the output — lower filter requirement.

### Level-Shifted PWM (LS-PWM)

For diode-clamped (NPC) converters. Uses (N-1) carrier signals stacked vertically, each compared to the same reference. Variants:

- **PD (Phase Disposition)**: all carriers in phase — lowest line-to-line THD
- **POD (Phase Opposition Disposition)**: carriers above zero are 180° out of phase with those below zero
- **APOD (Alternative POD)**: each adjacent carrier is 180° out of phase

## Interleaving

Two or more converter phases operating in parallel with phase-shifted clocks. Applies to multiphase buck converters (voltage regulator modules — VRMs) and interleaved PFC.

**Benefits**: reduces net current ripple (ripple cancellation), spreads heat across phases, improves transient response.

Ripple cancellation factor: depends on the number of phases and duty cycle — for 2 phases, optimal at D=0.5; for 3 phases, optimal at D=0.33 and D=0.66.

## Spread Spectrum (Frequency Dithering)

Modulating the switching frequency reduces peak EMI at the fundamental switching frequency and its harmonics. The energy is spread across a wider band.

**Methods**: triangular modulation (linear sweep), random modulation, pseudo-random binary sequence (PRBS).

**Limitation**: frequency variation must stay within the bandwidth constraints of the control loop and magnetics design. Typical: ±5-10% of the nominal switching frequency.

## PWM Schemes Comparison

| Scheme | THD | DC util | Switching loss | Complexity | Digital cost |
|--------|-----|---------|---------------|------------|--------------|
| Square wave | High | Max | Low | None | None |
| SPWM | ~5% | 78.5% | Moderate | Low | Low |
| 3rd harmonic | ~4% | 90.7% | Moderate | Low | Low |
| SVPWM | ~4% | 90.7% | Moderate | Medium | Medium |
| DPWM | ~6% | 90.7% | Low (33% less) | Medium | Medium |
| SHE | Very low | Variable | Very low | High | Very high |

## References
- Mohan, Undeland & Robbins. *Power Electronics*. 3rd ed. Ch 8, 15.
- Erickson & Maksimovic. *Fundamentals of Power Electronics*. 3rd ed. Ch 15.
- Holmes, D.G. & Lipo, T.A. *Pulse Width Modulation for Power Converters: Principles and Practice*. Wiley, 2003.
- Hava, A.M. et al. "A High-Performance PWM Algorithm for Common-Mode Voltage Reduction in Three-Phase Voltage Source Inverters." *IEEE Trans. Power Elec.*, 2011.
- MDPL Mathematics. "Comparative Analysis of SVPWM Techniques to Minimize CMV and/or Switching Losses." 2024.
