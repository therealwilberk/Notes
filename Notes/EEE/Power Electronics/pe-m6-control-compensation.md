---
tags: [power-electronics, control, compensation, small-signal]
aliases: ["PE M6", "Control & Loop Compensation"]
parent: "[[Power Electronics -- Map of Content]]"
created: 2026-06-17
status: complete
---

# M6: Control Theory & Loop Compensation

## Averaged Switch Model

The fundamental tool for analyzing converter dynamics. Replace the switch and diode with an average model that preserves the low-frequency behavior but removes the switching ripple.

**State-space averaging**: write the state equations for both switch-on and switch-off intervals, then average them over one switching period weighted by D and D'.

The result: a continuous-time nonlinear model that captures the *average* behavior of the converter. This is then linearized around a quiescent operating point to get a small-signal linear model.

## Canonical Model

Erickson & Maksimovic's canonical circuit model represents any PWM DC-DC converter as:

- An ideal DC transformer (turns ratio M(D))
- An effective low-pass filter (LC network)
- Controlled sources for duty cycle modulation (e(s) × d, j(s) × d)

The PWM switch model (Vorpérian) further simplifies this — the three-terminal PWM switch (active, passive, common) captures the switching cell behavior. Insert it into the converter circuit, replace the switch and diode with the averaged model, and analyze.

## Small-Signal Transfer Functions

### Control-to-Output: G_vd(s) = v_out(s) / d(s)

| Topology | Low-frequency gain | Pole structure | RHPZ? |
|----------|-------------------|----------------|-------|
| Buck | V_in | Two poles (LC) | No |
| Boost | V_in/(1-D)² | Two poles (LC) | Yes — f_z = R(1-D)²/(2πL) |
| Buck-boost | -V_in D/(1-D)² | Two poles (LC) | Yes |
| Flyback (CCM) | V_in D/(1-D)² × N | Two poles | Yes |
| Forward (CCM) | V_in × N × D | Two poles | No |

In all CCM topologies, the output filter creates a double pole at f_0 = 1/(2π√(LC)). The ESR of the output capacitor adds a zero at f_ESR = 1/(2π × C × R_ESR).

**Trap**: In DCM, the control-to-output transfer function reduces to a single pole (the inductor pole disappears) — no RHPZ. This is why DCM converters are easier to stabilize than CCM converters, but the trade-off is higher ripple and lower efficiency.

### Line-to-Output: G_vg(s) = v_out(s) / v_in(s)

Audio susceptibility — how well the output rejects input voltage disturbances. The crossover frequency determines the rejection bandwidth. Below crossover, feedback attenuates line variations. Above crossover, the open-loop line-to-output response determines the rejection.

## Compensation Design

### Type I Compensator (Integral only)

Single pole at origin. Low bandwidth. Rarely used alone — insufficient phase margin for most converters.

G_c(s) = ω_p / s

### Type II Compensator (PI + one pole)

Good for current-mode control (where the plant has a single dominant pole). Provides:

- One pole at origin (high DC gain → zero steady-state error)
- One pole at some frequency (reduce high-frequency gain)
- One zero (phase boost to counteract the pole)

G_c(s) = G_c0 × (1 + s/ω_z) / (s × (1 + s/ω_p))

Typical phase boost: up to 90°.

### Type III Compensator (Two poles, two zeros)

Required for voltage-mode control of CCM converters (double pole at LC resonance). Provides:

- One pole at origin
- Two zeros (placed near or below f_LC to cancel the double pole)
- Two poles (one at f_ESR, one at f_sw/2 to roll off noise)

G_c(s) = G_c0 × (1 + s/ω_z1)(1 + s/ω_z2) / (s × (1 + s/ω_p1)(1 + s/ω_p2))

Phase boost: up to 180°.

### Design Procedure

1. Measure or model the plant G_vd(s) (use frequency response analysis or the averaged model)
2. Choose crossover frequency f_c: typically f_sw/20 to f_sw/5
3. For voltage-mode CCM: place zeros near f_LC to cancel the double pole
4. Adjust compensator gain so that |T(f_c)| = 1 (where T = G_c × G_vd × H_fb)
5. Check phase margin: target >45°, ideally 60-90°
6. If phase margin is insufficient: move zeros lower, reduce f_c, or add a third zero

**Trap**: Phase margin measured at crossover assumes a single-pole roll-off. If the plant has a RHPZ (boost, buck-boost), the phase drops further above f_RHPZ. The crossover MUST be well below f_RHPZ — otherwise, sufficient phase margin is impossible. Rule of thumb: f_c < f_RHPZ / 3.

## Current-Mode Control

Peak current-mode control (PCMC) replaces the output inductor's dynamics with a current loop. The inner current loop senses the switch or inductor current and modulates the duty cycle to follow a current reference from the voltage loop.

**Advantages**:
- Reduces the plant to a single pole (current loop eliminates the inductor pole)
- Inherent overcurrent protection (cycle-by-cycle current limit)
- Improves line rejection (the current loop compensates input voltage variations immediately)
- Simplifies compensation (Type II is usually sufficient)

**Slope compensation is required for D > 50%**: Without slope compensation, the current loop is unstable above 50% duty cycle — subharmonic oscillation at f_sw/2. Add an external ramp to the current sense signal.

The required compensation slope: m_c = m_2 / (1 + D/2) — but commonly set to m_c = m_2/2 (half the inductor current down-slope) for stability across all duty cycles.

**Trap**: Subharmonic oscillation manifests as alternating pulse widths — the current waveform shows every-other-pulse widening. On the output, this appears as increased ripple at f_sw/2. The fix is proper slope compensation.

## Digital Control

### Sampling and Aliasing

The ADC sampling frequency must be high enough to avoid aliasing. The PWM carrier generates sidebands at multiples of f_sw — an anti-aliasing filter (or synchronous sampling) is required.

**Synchronous sampling**: sample the output voltage and current at the valley of the PWM carrier (when the switch is on for buck, or at the switching valley for boost). This avoids sampling the switching ripple and eliminates the need for anti-aliasing filtering.

### Discrete-Time Model

The plant must be discretized for digital control. Use the Z-transform with the appropriate hold equivalent:

- **Zero-order hold (ZOH)**: the DAC holds the control value constant between updates. This is the standard model for digital PWM controllers.
- **Tustin (bilinear)**: better for high-frequency poles, maps the jω axis to the unit circle — no frequency warping at low frequencies.
- **Matched pole-zero**: maps s-plane poles and zeros to z-plane using z = e^(sT).

### Digital PID

P(z) = K_p + K_i × T_s / (z-1) + K_d × (z-1) / (T_s × z)

Implement in difference equation form:

u[k] = u[k-1] + K_p × (e[k] - e[k-1]) + K_i × T_s × e[k] + K_d / T_s × (e[k] - 2e[k-1] + e[k-2])

**Required**: output clamping (anti-windup), integrator clamping, and initialization handling at startup.

### Deadbeat Control

One-step-ahead control: the controller is designed to drive the error to zero in one sample period (theoretically). Requires an accurate plant model. Very fast transient response but sensitive to parameter variation.

### Implementation Platforms

| Platform | Best for | Clock | ADC | PWM resolution |
|----------|----------|-------|-----|----------------|
| MCU (C2000, STM32G4) | Mid-complexity control | 200 MHz | 12-bit, 3 MSPS | 150 ps HRPWM |
| FPGA | Ultra-high speed / multi-phase | >200 MHz | External | ~100 ps |
| Digital power controller (UCD31xx) | Offline SMPS | 100 MHz | 12-bit | 250 ps |

**Trap**: Digital control introduces a computation delay (ADC → compute → PWM update). This delay adds phase lag in the loop — approximately 1-2 switching cycles. At high f_c/f_sw ratios, this delay can significantly reduce the phase margin. Use single-cycle update (update the PWM within the same switching period as the ADC sample) to minimize delay.

## References

- Erickson & Maksimovic. *Fundamentals of Power Electronics*. 3rd ed. Ch 7-11.
- Basso, C. *Transfer Functions of Switching Converters*. 2024.
- Analog Devices. *AN-149: Modeling and Loop Compensation Design of Switching Mode Power Supplies*.
- Texas Instruments. *Switch-Mode Power Converter Compensation Made Easy*. Application Note.
- Venable, D. "The K Factor: A New Mathematical Tool for Stability Analysis." Venable Industries, 1983.
- Monolithic Power Systems. "Digital Control of Power Electronic Systems." MPScholar.
