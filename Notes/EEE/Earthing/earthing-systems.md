---
tags: [eee, earthing, grounding, protection, safety, tn-system, tt-system, it-system]
aliases: ["TN System", "TT System", "IT System", "Earthing System Types", "IEC 60364 Earthing"]
parent: "[[Notes/EEE/Earthing/earthing-fundamentals]]"
created: 2026-06-27
status: complete
---

# Earthing Systems — TN, TT, IT

IEC 60364 classifies earthing systems by two letters. The first letter describes the supply-side (transformer) relationship to earth. The second letter describes the installation-side (consumer) relationship to earth.

## The Letter Code

| Position | Letter | Meaning |
|----------|--------|---------|
| First | T | One or more points of the supply (transformer) are directly connected to earth |
| First | I | The supply is isolated from earth or connected through a high impedance |
| Second | T | The installation's exposed conductive parts are connected directly to earth (independent of the supply earth) |
| Second | N | The installation's exposed conductive parts are connected to the supply neutral (which is itself earthed) |

Three combinations are possible: TN, TT, IT.

## TN System (Terre-Neutral)

The transformer neutral is directly earthed. The installation's exposed metalwork is connected to the same supply neutral. This creates a low-impedance metallic return path for earth faults.

```
Transformer              Installation
══════════               ════════════
                L1 ────
                L2 ────
                L3 ────
                N  ────
                PE ──── ─── Metal enclosures
   │
Earth electrode
```

**Fault behavior.** A phase-to-enclosure fault creates a high current limited only by the conductor impedances. Typically hundreds to thousands of amps. This is sufficient to trip conventional overcurrent protective devices (MCBs, MCCBs, fuses) within the required disconnection time.

**Protection condition.** The earth fault loop impedance Zs must satisfy:

```
Zs × Ia ≤ U0
```

Where Ia is the current causing automatic disconnection within the specified time and U0 is the nominal phase-to-earth voltage. Since Zs is low (typically 0.2-1.5 Ω), Ia can be high and standard overcurrent devices provide adequate protection.

**Application.** The dominant system in industrial, commercial, and urban residential installations worldwide. Preferred wherever low earth fault loop impedance can be guaranteed.

**TN subtypes.** Three subtypes define how neutral and protective earth are arranged along the distribution path — see [[earthing-tn-types]].

## TT System (Terre-Terre)

The transformer neutral is directly earthed (first T). The installation's exposed metalwork is connected to an independent local earth electrode (second T) — not to the supply neutral.

```
Transformer              Installation
══════════               ════════════
                L1 ────
                L2 ────
                L3 ────
                N  ────
                   ─ ─ ─ ─ (soil)
                         │
                    Local earth electrode
                         │
                    Metal enclosures
   │
Earth electrode
```

**Fault behavior.** A phase-to-enclosure fault must return through the soil between the consumer's earth electrode and the transformer's earth electrode. The total loop impedance includes two electrode resistances plus soil resistance, typically 20-200 Ω. The fault current is:

```
Ifault = U0 / (RA + RB + soil resistance)
```

For a 230 V system with 50 Ω loop impedance: Ifault = 4.6 A. This is too low to trip a standard 32 A MCB.

**Protection condition.** TT systems cannot rely on overcurrent devices for earth fault protection. Instead, RCDs are mandatory:

```
RA × IΔn ≤ 50 V
```

Where RA is the sum of the earth electrode resistance and PE conductor resistance, and IΔn is the rated residual operating current of the RCD. For a 30 mA RCD: RA ≤ 1667 Ω — easily achieved. For a 300 mA RCD: RA ≤ 167 Ω — achievable with a good electrode but requires verification.

**Applications:**
- Rural installations where the supply authority does not provide a PE conductor
- Temporary supplies (construction sites)
- Older overhead distribution networks
- Agricultural buildings
- Some residential areas in France, Spain, and parts of Africa

**Advantage:** No risk of the neutral conductor breaking and energizing exposed metalwork (a failure mode in TN-C systems). Each consumer has independent earthing.

**Disadvantage:** Mandatory RCDs for all circuits. High earth fault loop impedance means overcurrent devices alone cannot protect against earth faults.

## IT System (Isolé-Terre)

The transformer neutral is isolated from earth or connected through a high impedance (typically a 1500-2000 Ω resistor). The installation's exposed metalwork is connected to a local earth electrode.

```
Transformer              Installation
══════════               ════════════
                L1 ────
                L2 ────
                L3 ────
               (N) ──── (may not be distributed)
                    ─ ─ ─ ─
                    High impedance
                    or open
                    ─ ─ ─ ─
                    Earth electrode (supply side)
   │
Earth electrode
```

**Fault behavior — first fault.** A phase-to-enclosure fault produces a negligible current because no low-impedance return path exists. The current is limited by the system's leakage capacitance and the neutral-earthing impedance. Typical first-fault current: milliamps to a few amps. The system continues operating normally.

An insulation monitoring device (IMD) continuously measures the insulation resistance between the live conductors and earth and alarms when it falls below a set threshold (typically 50-100 kΩ for a 230/400 V system).

**Fault behavior — second fault.** If a second earth fault occurs on a different phase while the first fault remains uncleared, a phase-to-phase short circuit develops through the two fault paths and earth. The fault current is now high — limited only by the conductor impedances. The circuit must trip immediately. This second fault effectively converts the IT system into a TN or TT system depending on whether the exposed parts are interconnected.

**Protection condition.** For the first fault: detection by the IMD and an audible/visual alarm. For the second fault: automatic disconnection by overcurrent devices or RCDs must occur within the required time.

**Applications:**
- Hospital operating theatres (continuity of supply critical)
- Mines and quarries
- Continuous process industries (petrochemical, steel)
- Marine and offshore installations
- Data centers with stringent uptime requirements
- Electric propulsion systems on ships

**Advantage:** Supply continuity after the first earth fault. No arc flash risk during the first fault. Reduced maintenance shutdowns.

**Disadvantage:** Increased complexity (IMD required). A second fault is more dangerous than a first fault in a TN system because the phase-to-phase voltage across the fault loop is higher (400 V instead of 230 V). Requires trained personnel to locate and clear the first fault.

## Comparison

| Property | TN | TT | IT |
|----------|----|----|----|
| Transformer neutral earthing | Direct | Direct | Isolated or high impedance |
| Installation earthing | Via supply neutral | Independent electrode | Independent electrode |
| First fault current | High (kA) | Low (A to tens of A) | Negligible (mA) |
| Protection device for first fault | Overcurrent device (MCB, fuse) | RCD | IMD (alarm only) |
| Protection device for second fault | N/A (already tripped) | N/A (already tripped) | Overcurrent device or RCD |
| Typical Ze (external loop impedance) | 0.05-0.8 Ω | 10-200 Ω | N/A (system is not earthed) |
| RCD requirements | Not mandatory (but recommended) | Mandatory for all circuits | Not required for first fault |
| Supply continuity after first fault | Lost | Lost | Maintained |
| Complexity | Low | Medium | High |
| Dominant regions | UK, Germany, most industrial | France, Spain, rural areas | Hospitals, mines, ships |

## Selection Guidelines

Select TN when: the supply authority provides a low-impedance earth path and the installation has sufficient fault current to operate overcurrent devices.

Select TT when: the supply authority does not provide a PE conductor, the soil resistivity is low enough for a practical electrode, or the installation is temporary.

Select IT when: supply continuity during a first earth fault is essential, the installation is mobile or subject to frequent supply disconnection, the fault voltage must be minimized, or the installation operates in a hazardous environment where a single fault should not create an ignition source.

## References

- IEC 60364-1. *Low-voltage electrical installations — Fundamental principles, assessment of general characteristics.*
- IEC 60364-4-41. *Protection against electric shock.*
- IEC 60364-5-54. *Earthing arrangements and protective conductors.*
- IEC 60364-6. *Verification.*
- BS 7671. *Requirements for Electrical Installations. Part 4: Protection for safety.*
- ABB. *Technical Application Papers No. 3: Distribution systems and protection against indirect contact and earth fault.*
