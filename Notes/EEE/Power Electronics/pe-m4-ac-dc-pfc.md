---
tags: [power-electronics, ac-dc, pfc, rectifiers]
aliases: ["PE M4", "AC-DC Converters & PFC"]
parent: "[[Power Electronics -- Map of Content]]"
created: 2026-06-17
status: complete
---

# M4: AC-DC Converters & Power Factor Correction

## Diode Rectifiers

### Single-Phase Bridge Rectifier

Four diodes in a full-bridge configuration. Output voltage: V_dc = (2√2/π) × V_ac ≈ 0.9 × V_ac (unfiltered).

With a capacitor filter: the output rises to peak (√2 × V_ac) minus diode drops. The diodes conduct only near the voltage peak — pulsed input current causes high THD and low power factor (PF ~0.5-0.6).

### Three-Phase Bridge Rectifier

Six diodes. Output voltage: V_dc = (3√2/π) × V_L-L ≈ 1.35 × V_L-L.

Lower output ripple than single-phase. The pulsed current is less severe but still causes significant THD (~30%).

## Thyristor (SCR) Rectifiers

Controlled rectification. The firing angle α controls the average output voltage:

Single-phase: V_dc = (√2 × V_ac / π) × (1 + cos α)

Three-phase: V_dc = (3√2 × V_L-L / π) × cos α

**Trap**: At low firing angles, the power factor is poor due to the phase lag between voltage and current fundamental. Six-pulse rectifiers generate 5th, 7th, 11th, 13th... harmonics (6n±1). Use multipulse (12/24 pulse) configurations with phase-shifting transformers to cancel low-order harmonics.

## Power Factor Correction (PFC)

### Why PFC is Required

Without PFC, the input current is highly distorted (pulsed). This causes:
- Excessive neutral current in three-phase systems (3rd harmonic currents sum in the neutral)
- Transformer and conductor heating from harmonics
- Reduced real power capability from the utility
- IEC 61000-3-2 (Class A-D) limits harmonic current emissions for equipment >75 W

### Boost PFC (Single-Phase)

The most common active PFC topology. A boost converter between the bridge rectifier and the bulk capacitor shapes the input current to follow the input voltage.

**Control**: the boost converter operates with two cascaded loops:
1. **Outer voltage loop**: regulates the DC bus voltage (typically 380-400 V DC)
2. **Inner current loop**: shapes the input current to follow a sinusoidal reference (multiplied by the voltage loop output)

The current reference is: I_ref(t) = V_rectified(t) × V_error / V_rms²

### Operating Modes

| Mode | Inductor current | Characteristics |
|------|-----------------|-----------------|
| CCM | Continuous | Lower peak current, larger inductor, good for >300 W |
| DCM / BCM | Returns to zero each cycle | Simple control, smaller inductor, higher peak current, good for <300 W |
| CrCM (Critical) | Boundary between CCM/DCM | Variable frequency, ZVS at switch turn-on, good for 200-400 W |

**Trap**: CCM boost PFC requires a fast recovery diode (or SiC Schottky) in the boost stage — the reverse recovery of a standard diode causes excessive loss and EMI at the switching transition. The boost diode conducts during MOSFET turn-on — snap recovery spikes the switching node.

### Bridgeless PFC

Removes the input diode bridge — the MOSFET body diodes or additional low-frequency diodes handle rectification. Eliminates three diode drops from the conduction path — improves efficiency by ~1-2%.

**Topologies**: totem-pole (most common), bidirectional switch, dual-boost. Totem-pole with GaN FETs achieves >98% efficiency at 1 MHz switching.

**Trap**: Totem-pole PFC cannot operate in CCM with standard MOSFETs (body diode reverse recovery causes shoot-through). GaN HEMTs (no body diode) or SiC MOSFETs (fast recovery) are required.

### Vienna Rectifier (Three-Phase)

Three-level, three-phase PFC. Uses a single switch per phase with a bidirectional switching cell. Inherently limits the switch voltage stress to half the output voltage — enables the use of 600 V devices in a 400 V AC system.

**Advantages**:
- Low THD, high PF
- Three-level output reduces filter size
- No neutral point connection required

**Disadvantages**:
- Unidirectional (cannot regenerate)
- Complex control
- Requires a split DC bus with midpoint balancing

### Interleaved PFC

Two or more boost stages operating in parallel with phase-shifted clocks. Reduces input current ripple without increasing per-phase inductor size. Improves thermal distribution.

## Harmonics Standards

| Standard | Scope | Key Limits |
|----------|-------|------------|
| IEC 61000-3-2 | Equipment <16 A per phase | Class A-D limits by harmonic order |
| IEC 61000-3-12 | Equipment 16-75 A per phase | THD <48%, individual harmonics per order |
| IEEE 519 | Utility interconnection | Voltage THD <5%, current THD per TDD at PCC |

**Trap**: Meeting IEC 61000-3-2 Class C (lighting) requires both PF >0.9 and a 3rd harmonic current limit (<0.3× fundamental). Standard boost PFC on an LED driver needs additional filtering or an active wave-shaping circuit.

## Two-Stage vs Single-Stage

**Two-stage**: PFC + downstream DC-DC. Higher efficiency, larger, more expensive. Used for >75 W applications.

**Single-stage**: integrates PFC and DC-DC into one converter (e.g., flyback with valley switching). Used for <75 W applications where IEC 61000-3-2 may not apply (some exceptions). Lower efficiency but lower cost.

## References
- Mohan, Undeland & Robbins. *Power Electronics*. 3rd ed. Ch 5-6, 18.
- Erickson & Maksimovic. *Fundamentals of Power Electronics*. 3rd ed. Ch 17-18.
- ON Semiconductor. "Demystifying Three-Phase PFC Topologies." H2PToday, 2021.
- IEC 61000-3-2:2018, Electromagnetic compatibility (EMC) — Limits for harmonic current emissions.
- ScienceDirect. "Recent advancement of AC-DC SEPIC Converter: A State-of-the-Art Review." 2025.
