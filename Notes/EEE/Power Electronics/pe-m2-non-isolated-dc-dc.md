---
tags: [power-electronics, dc-dc, converters]
aliases: ["PE M2", "Non-Isolated DC-DC"]
parent: "[[Power Electronics -- Map of Content]]"
created: 2026-06-17
status: complete
---

# M2: Non-Isolated DC-DC Converters

## Buck Converter (Step-Down)

Steady-state: $V_{out} = D \cdot V_{in}$ (CCM, ideal)

Three states — on-state (switch closed), off-state (switch open, diode conducts), and boundary conditions determine component selection. See [[pe-m1-switching-devices]] for switch characteristics and [[pe-m8-magnetic-design]] for inductor design.

### CCM vs DCM

**CCM** (Continuous Conduction Mode): inductor current never reaches zero during the switching period. Well-defined transfer function, lower ripple, but the right-half-plane zero (boost/buck-boost only) complicates compensation.

**DCM** (Discontinuous Conduction Mode): inductor current hits zero before the next switching cycle. Occurs at light load. Transfer function changes to single-pole — easier compensation but higher ripple and lower efficiency due to increased peak current.

Boundary inductance: $L_{crit} = \frac{(1-D)R_{load}}{2 f_{sw}}$, where $R_{load} = V_{out} / I_{out}$.

Below $L_{crit}$, the converter enters DCM for that load condition.

### Output voltage ripple

$V_{ripple} = \frac{\Delta I_L t_{off}}{8 C_{out}} + \Delta I_L \cdot ESR_C$

At high switching frequencies, $ESR$ (and $ESL$) dominate ripple. Ceramic capacitors with low $ESR$ minimize ripple but can cause instability with some control loops due to low damping.

**Trap**: Using only ceramic output caps (very low $ESR$) may cause loop instability with Type III compensation. Add a small electrolytic or use a specific "ceramic-capable" controller. Check the $ESR$ zero frequency relative to crossover.

## Boost Converter (Step-Up)

$V_{out} = \frac{V_{in}}{1-D}$ (CCM, ideal)

**Right-half-plane zero**: a unique feature of boost and buck-boost topologies. When the load increases, the inductor current must first increase (temporarily reducing $V_{out}$) before the output capacitor recharges. This creates a zero in the RHP — it adds negative phase shift (like a pole) while increasing gain (like a zero). This limits the achievable crossover frequency.

Control implication: the crossover frequency must be well below the RHP zero frequency, typically $f_c < f_{RHPZ}/3$ to $f_{RHPZ}/5$.

$f_{RHPZ} = \frac{R_{load} (1-D)^2}{2\pi L}$

Higher $L$ pushes the RHPZ lower — there is a trade-off between ripple reduction and control bandwidth.

**Trap**: In boost converters, the output is disconnected from the input during normal operation, but there is a direct path from input to output through the inductor and diode. If the switch is shorted, $V_{in}$ appears at the output. If the switch stays on continuously, the inductor saturates and the output collapses. Always include a loss-of-load protection and consider a buck-boost if short-circuit behavior matters.

## Buck-Boost Converter

$V_{out} = -V_{in} \frac{D}{1-D}$

Inverting output. The switch, inductor, and diode form a topology where the inductor is connected to ground through the diode during off-time.

**Trap**: The output is inverted relative to input ground. The control circuitry must reference the correct ground. Isolated gate drive or level shifting is needed if the controller is on the input side.

## SEPIC (Single-Ended Primary-Inductor Converter)

$V_{out} = V_{in} \frac{D}{1-D}$ — same gain as buck-boost, but non-inverting.

Uses two inductors (or a coupled inductor) and a series capacitor.

**Advantages**: non-inverting, continuous input current (good for PFC and battery applications), inherent short-circuit protection (series capacitor blocks DC).

**Disadvantages**: two inductors (higher cost/volume), series capacitor must handle high ripple current, RHPZ similar to boost.

## Cuk Converter

$V_{out} = -V_{in} \frac{D}{1-D}$ — inverting, like buck-boost.

Continuous input AND output current — lowest ripple among the basic non-isolated topologies. Uses a series capacitor for energy transfer.

Series capacitor must carry full input current — high ripple rating required. Efficiency is generally lower than SEPIC due to higher conduction losses.

## Zeta Converter

Non-inverting version of Cuk. Same gain as SEPIC ($V_{out} = V_{in} \frac{D}{1-D}$) but with discontinuous input current and continuous output current. Uses a coupled inductor or two inductors with a series capacitor. Less common than SEPIC because the input current is pulsed.

## Topology Selection Guide

| Requirement | Best Fit | Why |
|-------------|----------|-----|
| V_out < V_in | Buck | Simplest, highest efficiency, no RHPZ |
| V_out > V_in | Boost | Needs care with RHPZ and compensation |
| V_out in/out range | SEPIC | Non-inverting, good for battery apps |
| V_out < 0 (negative rail) | Buck-boost or Cuk | Cuk has lower ripple |
| Continuous output current, pulsed input current | Zeta | Non-inverting, coupled inductor needed |
| High step-up ratio (>5×) | Boost + coupled inductor | Avoid extreme $D$ ratios |
| Bidirectional | Buck-boost (sync) | Use two switches with synchronous rectification |

## Steady-State Analysis Procedure (Any Topology)

1. Draw the circuit for switch-on and switch-off states
2. Apply inductor volt-second balance: ∫ v_L dt over one period = 0
3. Apply capacitor charge balance: ∫ i_C dt over one period = 0
4. Solve for V_out/V_in, I_L, ΔI_L, V_ripple
5. Determine CCM/DCM boundary using L_crit formulas

## Trap: Duty Cycle Limits

Real switches have minimum on-time and minimum off-time. At very high switching frequencies, these limits cap the achievable conversion ratio. A controller with 100 ns minimum on-time at 2 MHz cannot achieve $D < 0.2$.

## References
- Erickson & Maksimovic. *Fundamentals of Power Electronics*. 3rd ed. Ch 1-6.
- Mohan, Undeland & Robbins. *Power Electronics*. 3rd ed. Ch 7.
- Hart, D.W. *Power Electronics*. Ch 6-7.
