---
tags: [eee, earthing, bonding, protection, equipotential, touch-voltage, rcd, fault-loop]
aliases: ["Equipotential Bonding", "Earth Fault Loop Impedance", "Zs Calculation", "Touch Voltage", "RCD Protection", "Automatic Disconnection"]
parent: "[[Notes/EEE/Earthing/earthing-fundamentals]]"
created: 2026-06-27
status: complete
---

# Bonding and Earth Fault Protection

## Bonding vs Earthing

Earthing connects the electrical system to the physical earth via an electrode. Bonding connects exposed metal parts to each other so they stay at the same potential.

Bonding does not rely on the earth electrode — it creates a local equipotential zone. Two objects bonded together will rise or fall in voltage together, so a person touching both simultaneously experiences no dangerous potential difference, even if the entire zone is at a high voltage relative to remote earth.

## Main Equipotential Bonding

Every LV installation must bond the following to the main earthing terminal:

- Water supply pipes (metallic)
- Gas supply pipes
- Other metallic service pipes (heating, oil, compressed air)
- Structural steelwork
- Lightning protection system (where present)
- Metallic cable sheaths and armoring
- Metallic ducting and cable trays

The main bonding conductors are sized per the supply neutral conductor cross-section (typically 6-16 mm² Cu). The bond is made at the service entrance, as close to the point of entry as possible.

Without main bonding, a fault in one part of the building could create a potential difference between a pipe and an enclosure — exacting a person who touches both.

## Supplementary Bonding

In rooms with conductive floors or wet conditions (bathrooms, swimming pools, industrial kitchens), supplementary bonding connects all exposed metal parts within the room — pipework, radiators, bath tubs, and the PE conductors of all circuits in the room. This ensures the equipotential zone is maintained within arm's reach.

## Earth Fault Loop Impedance (Zs)

When a phase conductor contacts an exposed metal part, the fault current flows through a complete loop back to the transformer winding:

```
Transformer secondary winding
  → Phase conductor (impedance Zphase)
  → Fault point (assumed zero impedance — bolted fault)
  → Enclosure
  → Protective conductor (CPC / PE) — impedance Zpe
  → Main earthing terminal
  → Neutral-to-earth bond
  → Transformer neutral point
  → Back to secondary winding
```

The total impedance of this loop is Zs:

```
Zs = Ze + (R1 + R2)
```

Where:

| Component | Meaning | Typical Range |
|-----------|---------|---------------|
| Ze | External loop impedance — from transformer to the installation origin (supply authority's responsibility) | 0.05-0.80 Ω (TN), 10-200 Ω (TT) |
| R1 | Resistance of the phase conductor from the origin to the fault point | Depends on length and cross-section |
| R2 | Resistance of the protective conductor from the fault point back to the origin | Depends on length and cross-section |

### Calculation Example

A 32 A final circuit in a TN-S system with Ze = 0.35 Ω, 30 m of 4 mm² copper phase conductor and 2.5 mm² copper CPC:

Copper resistivity at 70°C operating temperature: 0.0225 Ω·mm²/m (corrected from 20°C value of 0.0175 using temperature factor).

```
R1 = 0.0225 × 30 / 4.0 = 0.169 Ω
R2 = 0.0225 × 30 / 2.5 = 0.270 Ω
R1 + R2 = 0.439 Ω
Zs = 0.35 + 0.439 = 0.789 Ω
```

Prospective earth fault current:

```
Ifault = U0 / Zs = 230 / 0.789 = 292 A
```

For a 32 A Type B MCB (magnetic trip threshold = 5 × In = 160 A), the fault current of 292 A is well above the instantaneous trip threshold. The MCB will trip within 0.1 s.

Maximum permitted Zs for a 32 A Type B MCB per BS 7671 Table 41.3: 1.44 Ω. The calculated Zs of 0.789 Ω is within limits.

### Temperature Correction

Conductor resistance increases with temperature. During a fault, conductors heat rapidly from their ambient operating temperature (typically 70°C for PVC-insulated cables) toward the maximum short-circuit temperature (160°C for PVC, 250°C for XLPE). The worst-case Zs uses the conductor resistance at the maximum operating temperature before the fault, not the 20°C cold resistance:

```
Rt = R20 × (1 + α × (t - 20))
```

For copper (α = 0.00393 /°C), from 20°C to 70°C:

```
R70 = R20 × (1 + 0.00393 × 50) = R20 × 1.1965
```

## Automatic Disconnection Condition

The protective device must disconnect the supply within a specified time when an earth fault occurs.

### Required Disconnection Times (IEC 60364-4-41)

| Circuit Type | TN System | TT System |
|-------------|-----------|-----------|
| Final circuits ≤ 32 A (socket outlets, hand-held equipment) | 0.4 s | 0.2 s |
| Distribution circuits and final circuits > 32 A (fixed equipment) | 5 s | 1 s |

### Checking the Condition

The disconnection condition for each circuit is:

```
Zs × Ia ≤ U0
```

Where Ia is the current causing the protective device to operate within the required time. For an MCB, Ia is the current at which the magnetic trip operates (typically 5 × In for Type B, 10 × In for Type C, 20 × In for Type D).

Rearranged:

```
Zs ≤ U0 / Ia
```

If the calculated Zs exceeds this value, either the cable must be shortened, the cable cross-section increased, or a different protective device selected.

## Touch Voltage

When a fault occurs but before the protective device operates, the enclosure rises to a voltage relative to earth:

```
Utouch = Ifault × Rpe
```

Where Rpe is the resistance of the protective conductor from the fault point to the main earthing terminal. The touch voltage is highest at the furthest point from the main earthing terminal because the full PE resistance is in series.

IEC 60364-4-41 defines conventional touch voltage limits:

| Condition | Touch Voltage Limit |
|-----------|-------------------|
| Dry locations (normal) | 50 V AC |
| Wet locations (construction, agricultural) | 25 V AC |
| Medical locations | 25 V AC |

The design must ensure that if the touch voltage exceeds these limits, the disconnection time is reduced accordingly. The Zs × Ia ≤ U0 condition inherently limits the touch voltage to U0 = 230 V in TN systems, but the actual touch voltage at the fault point during the fault duration depends on the PE conductor impedance.

## RCD Protection

Residual Current Devices detect the difference between current flowing in the phase conductor(s) and the neutral conductor. Under normal conditions, these are equal (assuming no leakage). When a fault diverts current to earth, the phase and neutral currents are no longer equal — the difference is the residual current.

### Operating Principle

```
Phase ────────┬─────────── Load
              │
              │ ←  IΔn (residual current)
              │
Earth ────────┘
Neutral ──────┴─────────── Load
```

A current transformer around all live conductors (including neutral) senses the vector sum. Under normal conditions: sum = 0. Under a ground fault: sum = IΔn. When IΔn exceeds the RCD threshold, the device trips.

### Standard Ratings

| IΔn | Application |
|-----|-------------|
| 10 mA | Medical, wet areas, child protection |
| 30 mA | General socket outlets, hand-held equipment |
| 100 mA | Protection against fire (not personnel) |
| 300 mA | Fire protection only, main incomer in TT |
| 500 mA | Main incomer, discrimination with downstream RCDs |

### RCD in TT Systems

In TT systems, the disconnection condition uses the RCD:

```
RA × IΔn ≤ 50 V
```

RA is the sum of the earth electrode resistance and the PE conductor resistance. For a 30 mA RCD:

```
RA ≤ 50 / 0.03 = 1667 Ω
```

This is easily achieved with any practical earth electrode. For a 300 mA RCD on a main switch:

```
RA ≤ 50 / 0.30 = 167 Ω
```

This requires a verified low-resistance earth electrode.

### Type of RCD

| Type | Detects | Standard |
|------|---------|----------|
| AC | Sinusoidal AC residual currents only | Basic, legacy |
| A | AC + pulsating DC residual currents | Modern installations |
| B | AC + pulsating DC + smooth DC + high-frequency AC | VFDs, UPS, EV chargers |
| F | AC + high-frequency (mixed frequencies) | Frequency converters |

Type A is the minimum for modern installations. Type B is required where variable speed drives, UPS, or EV charging equipment is installed.

## Earth Fault Protection Summary by System

| System | First Fault Protection | Disconnection Condition | Mandatory Devices |
|--------|----------------------|------------------------|-------------------|
| TN | Overcurrent device (MCB, MCCB, fuse) | Zs × Ia ≤ U0 | None beyond standard protection |
| TT | RCD | RA × IΔn ≤ 50 V | RCD on all circuits |
| IT (1st fault) | IMD alarm only | No disconnection required | Insulation monitoring device |
| IT (2nd fault) | Overcurrent or RCD | Zs × Ia ≤ U0 (TN-like) or RA × IΔn ≤ 50 V (TT-like) | Depends on exposed parts interconnection |

## References

- IEC 60364-4-41. *Low-voltage electrical installations — Protection for safety — Protection against electric shock.*
- IEC 60364-5-54. *Earthing arrangements, protective conductors and protective bonding conductors.*
- BS 7671. *Requirements for Electrical Installations. Part 4: Protection for safety. Part 5: Selection and erection of equipment.*
- IEC 61008-1. *Residual current operated circuit-breakers without integral overcurrent protection for household and similar uses (RCCBs).*
- IEC 61009-1. *Residual current operated circuit-breakers with integral overcurrent protection for household and similar uses (RCBOs).*
- ABB. *Technical Application Papers No. 3: Distribution systems and protection against indirect contact and earth fault.*
