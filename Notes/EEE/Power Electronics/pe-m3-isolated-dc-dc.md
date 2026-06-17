---
tags: [power-electronics, dc-dc, isolated-converters]
aliases: ["PE M3", "Isolated DC-DC"]
parent: "[[Power Electronics -- Map of Content]]"
created: 2026-06-17
status: complete
---

# M3: Isolated DC-DC Converters

Galvanic isolation between input and output through a transformer. The transformer also enables voltage step-up/step-down ratios beyond what non-isolated topologies can practically achieve.

## Flyback Converter

Lowest component count among isolated topologies. The transformer operates as a coupled inductor — it stores energy during the switch-on interval and releases it during the switch-off interval.

V_out = V_in × D / (1-D) × (N_s / N_p) — depends on the transformer turns ratio.

**Operating modes**:
- **CCM**: lower peak currents, smaller filter cap, but introduces a RHPZ (like the boost)
- **DCM**: simpler control (no RHPZ), higher peak currents, larger output ripple

**Transformer design is critical**:
- Must store energy — requires an air gap (unlike a standard transformer)
- Gap stores energy in the magnetic field: E = ½ × L_m × I_pk²
- Magnetizing inductance L_m determines the ripple current
- Leakage inductance creates a voltage spike at switch turn-off — requires snubber (RCD clamp or active clamp)

**Trap**: The leakage inductance spike can exceed the MOSFET rating. Always include a snubber. An RCD clamp across the primary winding absorbs leakage energy — the clamp voltage should be 1.5× the reflected output voltage to minimize loss without excessive voltage stress.

**Multiple outputs**: possible by adding secondary windings. Cross-regulation depends on leakage inductance between windings. Tight coupling with interleaved winding construction improves cross-regulation.

## Forward Converter

Unlike the flyback, the forward converter *transfers* energy during the switch-on interval (transformer does not store energy — an output inductor stores it).

V_out = V_in × D × (N_s / N_p)

**Transformer reset is required**: since the transformer is driven unidirectionally, the core must be reset each cycle to avoid saturation. Three reset methods:

| Method | Components | Duty limit | Efficiency |
|--------|------------|------------|------------|
| Tertiary winding reset | Third winding + diode | D < 50% | Good — energy returned to input |
| RCD reset | Resistor + cap + diode | D can exceed 50% | Poor — energy dissipated in R |
| Active clamp | Small MOSFET + cap | D up to ~70% | Best — ZVS, energy recycled |

**Trap**: In a single-switch forward converter with tertiary reset, D is limited to <50%. Exceeding this saturates the core. Two-switch forward converters eliminate this limit and recycle magnetizing energy through the input.

## Push-Pull Converter

Two primary switches drive the transformer alternately. Full-wave rectification on secondary.

V_out = 2 × V_in × D × (N_s / N_p)

**Problem**: flux imbalance. If the volt-second product applied by the two switches differs (due to controller mismatch or component tolerances), the core walks into saturation. The imbalance builds up over multiple cycles.

**Solution**: current-mode control (inherently balances flux), or DC-blocking capacitor in series with the primary, or careful component matching.

**Trap**: Push-pull converters can self-destruct from transformer saturation within tens of cycles if flux imbalance goes unchecked. Always use current-mode control or a DC-blocking capacitor.

## Half-Bridge Converter

Two switches drive the transformer through a DC-blocking capacitor. The capacitor prevents flux imbalance — it automatically blocks any DC component.

V_out = V_in × D × (N_s / N_p) (with capacitive divider providing V_in/2 at the switch node)

**Advantages**: no flux imbalance, switches see V_in (not 2×V_in as in push-pull), DC-blocking capacitor provides inherent protection.

**Disadvantages**: capacitive divider draws current, main switch utilization is lower than full-bridge.

## Full-Bridge Converter

Four switches, full utilization of the input voltage. The transformer primary is driven by two diagonally opposed switch pairs.

V_out = 2 × V_in × D × (N_s / N_p)

**Used for**: high-power applications (>500 W). The switches see V_in, and the transformer utilization is the best among bridge converters.

**Phase-shifted full-bridge (PSFB)**: a variant where all four switches operate at fixed 50% duty, but the phase shift between the two legs controls the output. Enables ZVS across all four switches with suitable inductance.

## LLC Resonant Converter

A resonant tank (L_r, C_r, L_m) provides a sinusoidal-like current waveform. Soft switching (ZVS on primary, ZCS on secondary) enables high efficiency at high frequencies — up to 1 MHz.

**Operating principle**:
- Two resonant frequencies: f_r1 = 1/(2π√(L_r × C_r)) and f_r2 = 1/(2π√((L_r + L_m) × C_r))
- Above f_r1: ZVS for primary switches, but secondary current is discontinuous (higher conduction loss)
- At f_r1: optimal operating point — ZVS for primary, ZCS for secondary, highest efficiency
- Between f_r1 and f_r2: ZVS for primary, ZCS for secondary — good for high input voltage
- Below f_r2: avoid — switches lose ZVS (ZCS region for primary), higher switching loss

**Control**: pulse frequency modulation (PFM) — increase frequency to reduce gain (for lower V_in, decrease frequency to increase gain).

**Gain curve**: capacitive region (ZCS, avoid) | ZVS region | inductive region (ZVS, operate here). The gain is >1 below f_r1, =1 at f_r1, and <1 above f_r1.

**Design parameters to select**:
- Q (quality factor) = √(L_r/C_r) / R_ac — lower Q gives higher peak gain but reduces operating range
- L_n = L_m / L_r — typically 3-7. Higher L_n reduces peak gain but improves ZVS range

**Trap**: The LLC converter is difficult to regulate under light load — the gain curve becomes very flat. At no load, the output voltage may drift to the peak of the gain curve. Always specify a minimum load or use burst mode control at light load.

## Dual Active Bridge (DAB)

Bidirectional isolated DC-DC. Two full bridges (primary and secondary) coupled through a transformer. Power flow is controlled by the phase shift between the two bridges — similar to PSFB but with active bridges on both sides.

**Advantages**: bidirectionality, high power density, inherent ZVS over a wide range, simple control.

**Disadvantages**: high circulating current at light load (ZVS is lost), current-mode control needed for transients.

## Topology Selection by Power Level

| Power | Typical Topology | Comments |
|-------|-----------------|----------|
| <50 W | Flyback | Lowest cost, multi-output, DCM avoids RHPZ |
| 50-200 W | Forward (single-switch) | Better efficiency than flyback, D < 50% |
| 200-500 W | Forward (two-switch) / Half-bridge | Two-switch forward: no duty limit, good efficiency |
| 500 W - 2 kW | Full-bridge / LLC | LLC resonant for high efficiency, PSFB for lower cost |
| 2 kW+ | Full-bridge / DAB | DAB for bidirectional, PSFB for unidirectional |

## References

- Erickson & Maksimovic. *Fundamentals of Power Electronics*. 3rd ed. Ch 6-8, 19.
- Mohan, Undeland & Robbins. *Power Electronics*. 3rd ed. Ch 9-11.
- Frenetic / Passive Components Blog. "Transformer Topologies in Power Converters." 2026.
- Monolithic Power Systems. "LLC Resonant Converter Design and Calculation."
