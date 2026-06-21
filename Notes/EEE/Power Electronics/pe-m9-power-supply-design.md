---
tags: [power-electronics, power-supply, smps, design]
aliases: ["PE M9", "Power Supply Design"]
parent: "[[Power Electronics -- Map of Content]]"
created: 2026-06-17
status: complete
---

# M9: Power Supply Design

## Design Specification Flow

A systematic power supply design proceeds through these stages:

1. **Requirements capture**: V_in range, V_out, I_out, ripple, transient response, isolation, efficiency target, form factor, cooling, standards compliance
2. **Architecture selection**: single-stage vs two-stage, isolated vs non-isolated, topology selection
3. **Power stage design**: switching frequency, semiconductor selection, magnetics, capacitors
4. **Control loop design**: compensation type, crossover, phase margin
5. **Protection design**: OCP, OVP, UVLO, OTP, soft-start, inrush
6. **Layout and thermal**: PCB stackup, component placement, heatsinks
7. **Verification**: Bode plot measurement, load transient, efficiency, thermal, EMI

## Topology Selection Dependencies

| Input V | Output | Power | Typical topology selection |
|---------|--------|-------|--------------------------|
| 5 V | 1-3.3 V | <30 W | Buck (point-of-load VRM) |
| 12 V | 5 V | <50 W | Buck |
| 12 V | Isolated 5 V | <25 W | Flyback |
| 48 V | 12 V | <200 W | Buck, half-bridge |
| 90-265 V AC | 12-48 V | <75 W | Flyback (single-stage) |
| 90-265 V AC | 12-48 V | 75-600 W | PFC boost + LLC or forward |
| 90-265 V AC | 12-48 V | >600 W | PFC + PSFB or LLC |
| 380 V DC (PFC bus) | 48-54 V | >1 kW | LLC or PSFB |
| 200-400 V DC | 12-48 V | >2 kW | Full-bridge or DAB |

## Component Stress Analysis

### Switch Stress

For each topology, calculate:
- **Voltage stress**: V_DS(max) = V_in(max) + V_spike (leakage inductance + ringing). Include a derating factor of 0.7-0.8 for silicon, 0.8-0.85 for SiC/GaN.
- **Current stress**: I_D(rms) and I_D(pk) — determine conduction loss (I²R) and ensure within SOA.
- **Thermal stress**: $P_{loss} = P_{cond} + P_{sw}$. The junction temperature $T_j = T_{amb} + R_{\theta JA} P_{loss}$ must be $< T_{j(max)}$.

### Capacitor Stress

- **Voltage derating**: electrolytic caps at <80% of rated V; ceramic caps lose capacitance with DC bias (some lose 60-80% at rated V) — always check the DC bias curves
- **Ripple current**: electrolytic caps have ESR-limited ripple current ratings. Exceeding this overheats and dries out the capacitor. Use multiple caps in parallel.
- **Lifetime**: aluminum electrolytic lifetime halves for every 10°C rise (Arrhenius). For 105°C rated caps: $L(T) = L_0 \cdot 2^{(T_0 - T)/10}$ where $T_0$ is the rated temperature and $L_0$ is the rated lifetime.

**Trap: ceramic DC bias derating** — ceramic capacitors (X5R, X7R) lose 60-80% of their nominal capacitance when operated near their rated DC voltage. Always derate by using a higher voltage rating (e.g., use 100 V rated ceramic for a 48 V bus) and check the DC bias curves in the datasheet.

### Inductor / Transformer Stress

- **Flux density**: ensure B_max < B_sat across all operating conditions — especially during inrush and transient overload
- **Winding loss**: I²R_ac dominates at high frequency. See [[pe-m8-magnetic-design]] for skin/proximity effect mitigation.

## Protection Circuits

### Overcurrent Protection (OCP)

- **Cycle-by-cycle current limit**: the controller turns off the switch when the sensed current exceeds a threshold. Reset each cycle.
- **Hiccup mode**: after a sustained overcurrent, the controller enters a "try, wait, try" cycle (e.g., 32 cycles on, 2 seconds off). Reduces average power during fault.
- **Fuse**: last-resort protection. Coordinate with the electronic protection to ensure the fuse does not trip during normal OCP events.

### Overvoltage Protection (OVP)

- **Output OVP**: a comparator monitors the output voltage and latches off the converter if exceeded. The latch is reset by recycling input power.
- **Input OVP**: required for PFC stages. The controller stops switching if the input voltage exceeds a safe threshold.

### Overtemperature Protection (OTP)

Use an NTC thermistor near the hottest component (typically the transformer or heatsink). The controller reduces power or shuts down at a threshold. Hysteresis prevents oscillation at the threshold boundary.

### Soft-Start

The output voltage ramps up gradually (typically 1-10 ms) to prevent inrush current and overshoot. Implemented by:
- Clamping the error amplifier output during startup
- Digitally ramping the reference voltage (in digital controllers)
- Switched capacitor soft-start (analog controllers)

**Trap: pre-bias output** — if the converter starts into an output that already has voltage (pre-bias from a parallel supply), the soft-start ramp must start from the pre-bias voltage, not from zero. Otherwise, the output capacitor discharges through the synchronous rectifier, causing reverse current and an OCP trip. Most digital controllers have a pre-bias startup mode that reads the output voltage before starting.

### Inrush Current Limiting

Without limiting, the input bulk capacitor draws a large current at power-on, tripping upstream breakers. Methods:

| Method | Loss | Cost | Reusable? |
|--------|------|------|-----------|
| NTC thermistor | Low after heating | Low | No (must cool to reset) |
| Resistor + relay bypass | Only in resistor during startup | Medium | Yes |
| Active FET soft-start | Very low | High | Yes |
| Step-start with pre-charge | Low | Medium | Yes |

## Layout Considerations

Power stage layout, gate drive loop design, current sensing, thermal vias, and grounding practices are covered in detail in [[pe-m11-thermal-emc-layout]]. The same principles apply to PSU design — refer to that module for specific layout guidance including commutation loop minimization, Kelvin sensing, and ground plane separation.

## Hold-Up Time

The minimum time the output stays in regulation after input power is removed. Required for:
- Server PSU: 10-20 ms hold-up at full load
- Industrial PSU: 10-20 ms
- Telecom: 5-20 ms

Bulk capacitor requirement: $C_{bulk} = \frac{2 P_{out} t_{hold}}{V_{in(min)}^2 - V_{in(toff)}^2}$

For a PFC stage with 400 V DC bus and 300 V turn-off: $C_{bulk} = \frac{2 P_{out} t_{hold}}{400^2 - 300^2} = \frac{2 P_{out} t_{hold}}{70000}$.

## References

- Pressman, A.I. et al. *Switching Power Supply Design*. 3rd ed. McGraw-Hill.
- Maniktala, S. *Switching Power Supplies A-Z*. 2nd ed. Newnes.
- Basso, C. *Switch-Mode Power Supplies: SPICE Simulations and Practical Designs*. 2nd ed.
- Erickson & Maksimovic. *Fundamentals of Power Electronics*. 3rd ed. Ch 6, 20.
- Analog Devices. *AN-149: Modeling and Loop Compensation Design of Switching Mode Power Supplies*.
