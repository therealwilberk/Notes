---
tags: [power-electronics, motor-drives, foc, bldc, pmsm]
aliases: ["PE M10", "Motor Drives"]
parent: "[[Power Electronics -- Map of Content]]"
created: 2026-06-17
status: complete
---

# M10: Motor Drives

## DC Motor Drives

Simplest motor control — torque is proportional to armature current, speed is proportional to armature voltage minus IR drop.

- **Single-quadrant drive**: one H-bridge leg + flyback diode — forward motoring only
- **Two-quadrant drive**: regenerative braking possible (power flows back when back-EMF > armature voltage)
- **Four-quadrant drive**: full H-bridge with regeneration — forward/reverse motoring and braking

## Brushless DC (BLDC) Motor — Six-Step Commutation

BLDC motors have permanent magnets on the rotor and concentrated windings on the stator. The trapezoidal back-EMF enables six-step commutation.

**Commutation sequence**: energize two of three phases at a time. Every 60 electrical degrees, the active phases switch. Hall effect sensors (or sensorless back-EMF detection) provide the rotor position.

**Limitations**:
- Torque ripple at each commutation event (every 60°)
- Non-optimal current waveform — the phase current is rectangular, not sinusoidal
- No torque control at low speed for sensorless operation (back-EMF is proportional to speed — at zero speed, back-EMF = 0)

## PMSM — Field-Oriented Control (FOC)

PMSMs have sinusoidal back-EMF and distributed windings. FOC provides smooth torque with zero low-frequency ripple.

### Clarke and Park Transforms

**Clarke transform**: convert three-phase currents (a, b, c) to a stationary two-axis system (α, β):

```
i_α = i_a
i_β = (i_a + 2×i_b) / √3
```

**Park transform**: rotate the stationary frame to align with the rotor flux:

```
i_d = i_α × cos(θ) + i_β × sin(θ)
i_q = -i_α × sin(θ) + i_β × cos(θ)
```

Result: i_q (quadrature) controls torque, i_d (direct) controls flux. For surface-mount PMSM (SPMSM), i_d is set to 0 for maximum torque per ampere (MTPA). For interior PMSM (IPMSM), injecting negative i_d exploits reluctance torque.

### Control Structure

1. **Outermost loop (speed/position)**: PI controller generates the torque (i_q) reference
2. **Current loop (i_d, i_q)**: two PI controllers regulate i_d and i_q — typically much faster bandwidth than the speed loop
3. **Inverse Park + Clarke**: convert V_d, V_q back to three-phase voltage commands
4. **PWM**: SVPWM or SPWM generates the inverter gate signals (see [[pe-m7-pwm-modulation]])

### PI Tuning for Current Loops

Plant: the motor winding is an RL circuit (L_s, R_s). In the dq-frame, the electrical time constant τ_e = L_s / R_s.

Tune the PI gains for a desired current loop bandwidth f_c (typically f_sw/20):

K_p = 2π × f_c × L_s
K_i = K_p × R_s / L_s (zero at -R_s/L_s cancels the plant pole)

### Sensorless FOC

Eliminates the position sensor — reduces cost and improves reliability. Methods:

| Method | Low-speed | Medium/high-speed | Requires |
|--------|-----------|-------------------|----------|
| Back-EMF observer | Fails near zero | Good | Motor model + speed estimation |
| Sliding mode observer | Poor | Good | Robust, chattering |
| Flux observer | Poor | Good | Accurate flux model |
| INFORM / HF injection | Good | Not needed | Salient pole motor (IPMSM) |
| Luenberger observer | Fair | Good | Model + speed adaptation |

**Trap**: Sensorless FOC fails at very low or zero speed because the back-EMF goes to zero. If the application must produce torque at zero speed (e.g., crane, elevator), a sensor is required. Hybrid methods (HF injection at low speed, back-EMF at high speed) bridge the gap.

## Induction Motor Drives

Induction motors (IMs) are simpler and cheaper than PMSM but more complex to control.

### Scalar Control (V/f)

Keep the V/f ratio constant to maintain constant flux. Simple, open-loop, adequate for fans and pumps. Poor dynamic response — cannot control torque directly.

### Field-Oriented Control for IM

**Rotor flux orientation (RFO-FOC)**: align the d-axis with the rotor flux vector. The slip frequency is injected to maintain rotor flux orientation:

ω_slip = R_r × i_q / (L_r × i_d)

Slower than PMSM FOC (the rotor flux has a time constant τ_r = L_r / R_r). Flux estimation requires a model of the rotor circuit.

### Direct Torque Control (DTC)

Instead of PWM + PI current loops, DTC directly selects the inverter switching state using hysteresis comparators for torque and flux:

- Torque and flux are estimated from the stator voltages and currents
- A hysteresis comparator selects the appropriate voltage vector from a lookup table
- Fast torque response (limited only by the inverter switching speed)

| Aspect | FOC | DTC |
|--------|-----|-----|
| Torque response | Fast (limited by PI bandwidth) | Very fast (hysteresis-based) |
| Steady-state ripple | Low | Higher (torque ripple at switching harmonics) |
| Parameter sensitivity | Moderate | Low |
| Switching frequency | Fixed | Variable (hysteresis) |
| Implementation complexity | Moderate | Simple |
| Low-speed performance | Good | Poor (higher ripple) |

## Regenerative Braking

When the motor speed exceeds the commanded speed (or during braking), kinetic energy is returned to the DC bus. The bus voltage rises. In a motor drive, the excess energy must be dissipated (braking resistor) or returned to the grid (regenerative drive).

**Braking chopper**: a switch and resistor across the DC bus. When the bus voltage exceeds a threshold (typically 10% above nominal), the chopper dissipates the regen energy as heat.

**Active front end (AFE)**: replaces the diode rectifier with an active PWM rectifier that can return energy to the grid. Enables four-quadrant operation and also provides PFC on the input.

## Traction Inverters

Automotive traction drives (EV/HEV) have specific requirements:

- **DC bus**: 400 V (current gen) or 800 V (next gen — lower I²R losses, faster charging)
- **Power**: 50-400 kW peak
- **Switching devices**: IGBT modules (400 V bus) or SiC MOSFET modules (800 V bus)
- **Current handling**: 200-600 A RMS per phase
- **Thermal**: liquid cooling, junction temperature up to 175°C for Si, 200°C+ for SiC
- **Safety**: ASIL-D functional safety (ISO 26262), galvanic isolation, redundant sensors

**Trap**: 800 V bus traction inverters require careful consideration of partial discharge and clearance/creepage distances in the motor windings. Standard insulation systems designed for 400 V may fail at 800 V. Motor rewinding or custom insulation is required.

## References
- Mohan, N. *Advanced Electric Drives: Analysis, Control, and Modeling Using MATLAB/Simulink*. Wiley, 2014.
- Mohan, N. *Electric Machines and Drives: A First Course*. Wiley, 2012.
- Krishnan, R. *Permanent Magnet Synchronous and Brushless DC Motor Drives*. CRC Press.
- Buja, G.S. & Kazmierkowski, M.P. "Direct Torque Control of PWM Inverter-Fed AC Motors — A Survey." *IEEE Trans. Ind. Elec.*, 2004.
- Novotny, D.W. & Lipo, T.A. *Vector Control and Dynamics of AC Drives*. Oxford, 1996.
