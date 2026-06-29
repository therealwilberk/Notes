---
tags: [harmonics, triplen, neutral, transformer, propagation]
aliases: ["Triplen Harmonics", "Zero-Sequence Harmonics", "Neutral Current Harmonics"]
parent: "[[Harmonics -- Map of Content]]"
created: 2026-06-27
status: complete
---

# M3: Triplen Harmonics & Propagation

## What Triplens Are

Triplen harmonics are odd multiples of the third harmonic: 3rd, 9th, 15th, 21st, 27th... (orders $3n$).

They behave as zero-sequence quantities in a three-phase system. In a balanced three-phase system, zero-sequence components are equal in magnitude and phase on all three phases. For the fundamental, this only happens during a ground fault. For triplen harmonics, this happens continuously when single-phase nonlinear loads are present.

This zero-sequence behavior is the root cause of most harmonic-related field problems.

## Why Triplens Sum in the Neutral

In a balanced three-phase system with a shared neutral, fundamental currents on each phase are 120 degrees apart and cancel in the neutral:

$$
I_N = I_A + I_B + I_C = 0
$$

For a triplen harmonic (e.g., 3rd), the phase shift is $3 \times 120^\circ = 360^\circ = 0^\circ$. All three phases are in phase at the triplen frequency. They do not cancel — they add arithmetically:

$$
I_{N,3rd} = 3 \times I_{phase,3rd}
$$

A common scenario: each phase carries 100 A fundamental + 30 A 3rd harmonic. The neutral carries 90 A of 3rd harmonic — nearly as much as a single phase current. With 40% 3rd harmonic distortion, the neutral current exceeds the phase current.

**Trap:** The 9th and 15th harmonics also sum in phase. Though typically smaller in magnitude than the 3rd, their contribution can push the neutral current higher.

## The Shared Neutral Problem

In 208/120 V or 400/230 V wye systems, a single neutral conductor serves three phase conductors. This was safe for linear loads because neutral current was small. With triplen harmonics, the neutral becomes the most heavily loaded conductor.

**Physical effects:**
- Neutral conductor overheats — can exceed 180°C in severe cases
- Insulation degrades — PVC rated for 70-90°C fails rapidly
- Connections oxidize and loosen — increased resistance creates a thermal runaway
- A lost neutral causes voltage imbalance — line-to-neutral voltages swing wildly, damaging connected equipment

**Trap:** Many older designs used a reduced-size neutral (50% of phase conductor). These installations are dangerous with modern loads. Neutral should be at least the same size as phase conductors; often 150-200% in harmonic-rich environments.

## Transformer Winding Connections and Triplen Flow

Transformer winding configuration determines whether triplen harmonics propagate upstream.

### Delta-Wye (Delta primary, Wye secondary)

This is the most common LV distribution transformer configuration. Triplen harmonic currents on the wye secondary can flow due to the neutral return path. In the delta primary, these triplen currents circulate within the delta winding but do **not** appear in the line currents on the primary side.

**Implications:**
- Triplen harmonics are "trapped" in the delta — they do not pollute the upstream MV network
- But they still circulate in the transformer windings, causing additional heating
- A delta-wye transformer can run hot even when loaded below nameplate, due to triplen circulating currents

### Wye-Wye (both windings wye-connected)

Triplen harmonics flow freely from secondary to primary. The upstream network sees the triplen harmonics. This configuration provides no isolation.

### Wye-Delta (Wye primary, Delta secondary)

The wye primary can carry triplen harmonics from the upstream network. The delta secondary blocks them from reaching the load. Rarely used for distribution.

### Delta-Delta

No neutral path exists on either side. Triplen harmonics cannot flow in the line currents. However, triplen harmonics can still be present if the load produces them — they circulate within the delta windings.

### Zigzag Transformers

A zigzag winding provides a low-impedance path for zero-sequence (triplen) currents. Installed in shunt (parallel) with the load, it diverts triplen harmonics from the neutral back to the phase conductors, reducing neutral current.

## Propagation Rule Summary

| Configuration | Triplen on Secondary Side | Triplen on Primary Lines | Triplen Circulating in Windings |
|---------------|--------------------------|-------------------------|-------------------------------|
| Delta-Wye | Yes (via neutral) | No (trapped in delta) | Yes |
| Wye-Wye (both grounded) | Yes | Yes | Yes |
| Delta-Delta | No (requires neutral path) | No | Depends on load |
| Wye-Delta | Depends on primary neutral | Depends on upstream | Yes |
| Zigzag (shunt) | Diverts from neutral | N/A | N/A |

## Balanced vs Unbalanced Loading

The zero-sequence model for triplens assumes balanced loading. In reality, phases are never perfectly balanced. Unbalance causes some fundamental zero-sequence current and allows non-triplen harmonics to appear in the neutral as well.

**Trap:** A three-legged core transformer behaves as if it has a "phantom" delta tertiary winding. Even with a wye-wye transformer where only one neutral is grounded, triplen harmonics can still flow due to this built-in zero-sequence path. The phantom delta also provides a path for triplen circulating currents.

## System Resonance

Harmonic propagation is not purely resistive — it involves L and C. A power factor correction capacitor bank combined with transformer leakage inductance forms an LC tank circuit. If the resonant frequency coincides with a harmonic present in the system:

$$
f_{res} = \frac{1}{2\pi \sqrt{LC}}
$$

The harmonic current at that frequency is amplified — sometimes by a factor of 5-10x. This is **parallel resonance** (high impedance at the resonant frequency). It causes high voltage distortion and can damage capacitor banks.

**Series resonance** occurs where a capacitor and inductor form a low-impedance path at the resonant frequency. Harmonic current is drawn into the resonant path, causing overheating of the capacitor bank.

**Practical implication:** Installing PFC capacitors without a harmonic study is risky. A bank tuned for 50 Hz with 5th harmonic resonance can fail catastrophically. Detuning reactors (7% or 14% impedance) shift the resonant frequency below the first significant harmonic.

## References

- Schonek, J. *The Singularities of the Third Harmonic.* Schneider Electric Cahier Technique, 2002.
- IEEE 519-2022. *Harmonic Control in Electric Power Systems.*
- Csanyi, E. *What are Triplen Harmonics and Where Do They Happen?* EEP, 2018.
- ECalPro. *Worked Example: Harmonic Analysis & Neutral Conductor Sizing for a 2 MW Data Center.*
