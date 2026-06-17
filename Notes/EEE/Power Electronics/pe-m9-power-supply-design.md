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
- **Thermal stress**: P_loss = P_cond + P_sw. The junction temperature T_j = T_amb + R_θJA × P_loss must be < T_j(max).

### Capacitor Stress

- **Voltage derating**: electrolytic caps at <80% of rated V; ceramic caps lose capacitance with DC bias (some lose 60-80% at rated V) — always check the DC bias curves
- **Ripple current**: electrolytic caps have ESR-limited ripple current ratings. Exceeding this overheats and dries out the capacitor. Use multiple caps in parallel.
- **Lifetime**: aluminum electrolytic lifetime halves for every 10°C rise (Arrhenius). For 105°C rated caps: L = L_rated × 2^((T_rated - T_actual)/10).

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

### Inrush Current Limiting

Without limiting, the input bulk capacitor draws a large current at power-on, tripping upstream breakers. Methods:

| Method | Loss | Cost | Reusable? |
|--------|------|------|-----------|
| NTC thermistor | Low after heating | Low | No (must cool to reset) |
| Resistor + relay bypass | Only in resistor during startup | Medium | Yes |
| Active FET soft-start | Very low | High | Yes |
| Step-start with pre-charge | Low | Medium | Yes |

## Layout Considerations

### Power Stage Layout

- **Power loop area**: minimize the commutation loop (input cap → switch → output inductor → output cap → return). Each commutation loop generates magnetic field that couples into the control circuitry. Rule: loop inductance < 1 nH per 1 mm of loop perimeter.

- **Gate drive loop**: the gate driver → gate resistor → MOSFET gate → Kelvin source → return to driver must be as small as possible. Long gate loops pick up noise and cause ringing — can destroy the MOSFET gate oxide.

- **Current sense path**: use a Kelvin connection for shunt resistors. The sense traces should route directly to the shunt terminals, not through power plane copper.

- **Thermal via arrays**: place arrays of vias under power components (MOSFETs, diodes) to conduct heat to internal copper planes. Via pitch: 1.0-1.2 mm, via diameter: 0.3-0.5 mm, barrel plating: 1 oz minimum.

### Grounding

- **Power ground / signal ground separation**: the high di/dt return current from the switch must not share a path with the control circuitry's ground reference. Route power ground and signal ground as separate planes, connected at a single point (typically the input capacitor negative terminal).

**Trap**: A common mistake is routing the gate driver return current through the power ground plane. The voltage drop across the power ground impedance creates a voltage spike on the gate driver's ground reference — this differential voltage can exceed the gate-source rating. Always use a separate gate drive return trace to the source of the MOSFET.

## Hold-Up Time

The minimum time the output stays in regulation after input power is removed. Required for:
- Server PSU: 10-20 ms hold-up at full load
- Industrial PSU: 10-20 ms
- Telecom: 5-20 ms

Bulk capacitor requirement: C_bulk = 2 × P_out × t_hold / (V_in(min)² - V_in(turn-off)²)

For a PFC stage with 400 V DC bus and 300 V turn-off: C_bulk = 2 × P_out × t_hold / (400² - 300²) = 2 × P_out × t_hold / 70000.

## References

- Pressman, A.I. et al. *Switching Power Supply Design*. 3rd ed. McGraw-Hill.
- Maniktala, S. *Switching Power Supplies A-Z*. 2nd ed. Newnes.
- Basso, C. *Switch-Mode Power Supplies: SPICE Simulations and Practical Designs*. 2nd ed.
- Erickson & Maksimovic. *Fundamentals of Power Electronics*. 3rd ed. Ch 6, 20.
- Analog Devices. *AN-149: Modeling and Loop Compensation Design of Switching Mode Power Supplies*.
