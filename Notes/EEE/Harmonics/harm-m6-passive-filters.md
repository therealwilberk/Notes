---
tags: [harmonics, passive-filters, line-reactors, mitigation]
aliases: ["Passive Harmonic Filters", "Tuned Filters", "Line Reactors"]
parent: "[[Harmonics -- Map of Content]]"
created: 2026-06-27
status: complete
---

# M6: Passive Filters & Line Reactors

## Line Reactors (AC/DC)

The simplest and most cost-effective harmonic mitigation device. A line reactor is an inductor placed in series with the nonlinear load.

**How it works:** The reactor's inductive reactance increases with frequency ($X_L = 2\pi f L$). At harmonic frequencies, the reactor presents higher impedance, smoothing the current pulses from the rectifier.

**Standard sizes:**

| Reactor | % Impedance (at fundamental) | Effect on THD_I (6-pulse) |
|---------|------------------------------|---------------------------|
| None | 0% | ~30-40% |
| AC line reactor (3%) | 3% | ~25-33% |
| AC line reactor (5%) | 5% | ~22-28% |
| DC link reactor | Equivalent to ~1.5-2% AC | ~28-35% |
| AC + DC reactor | ~3% AC + DC | ~20-25% |

**Trap:** Adding a reactor reduces harmonic current but also reduces the DC bus voltage slightly (voltage drop across the reactor). The VFD may not reach full output voltage on a marginal supply.

### Mounting Options

| Location | Advantages | Disadvantages |
|----------|------------|---------------|
| AC line side (before rectifier) | Protects rectifier from line transients, reduces line notching | Larger, 3-phase component |
| DC link (between rectifier and DC bus) | Smaller, lower cost, single component | Does not reduce line notching |

**Practical rule:** For VFDs, always use at least a 3% AC line reactor. Many VFD manufacturers include a DC link reactor internally. Adding an external AC reactor further reduces THD and provides additional protection.

## Tuned Passive Filters

An LC circuit tuned to resonate at a specific harmonic frequency. At resonance, the filter presents a low-impedance shunt path that diverts harmonic current away from the supply.

**Resonant frequency:**

$$
f_{res} = \frac{1}{2\pi \sqrt{LC}}
$$

### Single-Tuned Filter

The most common type. A series LC branch tuned to one harmonic (e.g., 5th at 250 Hz).

```
Supply ──── Load
            │
            ├─ L5 ── C5 ── (5th harmonic trap)
            │
```

Designed with a quality factor $Q$ (typically 30-100). Higher $Q$ = narrower bandwidth = more effective at the tuned frequency but less forgiving of component drift or frequency variation.

**Trap:** A filter tuned precisely to 250 Hz on a 50 Hz system has minimal impedance at 250 Hz. But if the system frequency drifts to 50.5 Hz, the 5th harmonic is now at 252.5 Hz, and the filter impedance rises. Standard design assumes +/- 1-2% frequency tolerance.

### Double-Tuned Filter

A single branch that provides low impedance at two adjacent harmonics (e.g., 5th and 7th). More compact than two single-tuned branches but more complex to design.

### High-Pass (Damped) Filter

Instead of a sharp notch, a high-pass filter uses a resistor in parallel with the tuning inductor to provide broadband attenuation above a corner frequency.

**Second-order high-pass:**

```
Supply ──── Load
            │
            ├─ R ── C
            │    │
            └──── L
```

Effective for suppressing multiple high-order harmonics simultaneously. Used when harmonic spectrum is broad or variable.

**C-type filter:** A variant where a capacitor is placed in series with the inductor, and the resistor is in parallel with the inductor. Provides very low loss at fundamental (the C and L are tuned to 50 Hz) while damping high-order harmonics. Common for arc furnace installations.

## Passive Filter Design Considerations

### Reactive Power Compensation

At the fundamental frequency, a passive filter (especially the capacitor) supplies reactive power. This is often beneficial — the filter displaces some PFC requirement. But it also means the filter must be rated for fundamental voltage and current, not just harmonic content.

### Detuning Uncertainty

Component tolerances (+/- 5-10% for inductors, +/- 5% for capacitors), temperature drift, and aging shift the resonant frequency. Standard practice:

- Design the filter to resonate at 3-5% below the target harmonic (e.g., 237 Hz for 5th harmonic on 50 Hz). The filter then covers the target even with component drift.
- Include a detuning reactor (7% or 14%) on PFC capacitor banks to prevent resonance with system inductance.

### Resonance with System Impedance

The filter capacitor forms a parallel resonant circuit with the upstream system inductance. The **parallel resonance** frequency must not coincide with any significant harmonic in the system.

```
     Z_sys (L_sys)
        │
        ├──── Load
        │
     Filter (L_f, C_f)
```

The parallel resonance frequency:

$$
f_{res,parallel} = \frac{1}{2\pi} \sqrt{\frac{1}{L_{sys} C_{filter}}}
$$

If this coincides with, say, the 7th harmonic, and the system has significant 7th harmonic content, the voltage distortion at 350 Hz can be amplified.

**Rule:** Always perform a system impedance scan (frequency response) when adding passive filters to an existing installation.

## Passive Filter Comparison

| Filter Type | Harmonics Targeted | THD_I Reduction | Cost | Risk |
|-------------|-------------------|-----------------|------|------|
| Line reactor (3%) | Broad, moderate | 25-30% reduction | Low | None |
| Line reactor (5%) | Broad, moderate | 30-40% reduction | Low | Voltage drop |
| Single-tuned (5th) | 5th only | 50-60% if 5th dominates | Medium | Resonance with system |
| Single-tuned (5th + 7th) | 5th, 7th | 60-70% | Medium | Resonance |
| Double-tuned (5/7) | 5th, 7th | 60-70% | Medium | Complex tuning |
| High-pass (2nd order) | All above corner | 40-50% | Medium | Higher loss |
| C-type | Broad + specific | 50-70% | Medium-High | Component count |

## When Passive Filters Are the Right Choice

- Dominant harmonics are low-order and stable (5th, 7th from 6-pulse drives)
- Load is constant or varies slowly
- Reactive power compensation is also needed
- Budget is limited — passive filters cost 1/3 to 1/2 of equivalent active filters
- Installation has clean (low-distortion) supply — passive filters work best when the background voltage is already sinusoidal

## When Passive Filters Are the Wrong Choice

- Load varies rapidly (active filter tracks better)
- Harmonic spectrum is broad or contains many orders
- System impedance varies (genset vs utility, multiple generators in parallel)
- Multiple filter stages would be needed (space, cost, resonance risk)
- The load includes significant interharmonics or subharmonics

## References

- IEEE 519-2022. *Harmonic Control in Electric Power Systems.*
- Comsys. *Comparing Harmonics Mitigation Techniques.* IEEE.
- Transcoil. *Hybrid Power Quality Solutions using Line Reactors, Active and Passive Filters.*
- Energies 17(11), 2024. *Design and Performance Evaluation of a Hybrid Active Power Filter Controller.*
- Siemens. *Whitepaper: Harmonics in Power Systems.*
