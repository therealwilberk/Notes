---
tags: [eee, earthing, grounding, protection, safety, fundamentals]
aliases: ["Ground vs Neutral", "Earthing Fundamentals", "Why Earth", "Neutral Earth Distinction", "PE Conductor"]
parent: "[[Notes/EEE/LV/lv-switchgear]]"
created: 2026-06-27
status: complete
---

# Earthing Fundamentals

## The Core Idea

Two separate jobs exist in every electrical system:

1. **Current needs a path back to its source** — this is the job of the neutral conductor, part of the normal load circuit
2. **Fault current needs a path away from people** — this is the job of the protective earth conductor and the earth electrode

These are different jobs with different conductors. Confusion starts when they are discussed without separating the two.

## Where the Neutral Comes From

A star-connected transformer secondary winding has a center point called the neutral point:

```
L1 ───── ┐
         ├── ● (neutral point)
L2 ───── ┘
L3 ─────
```

When that center point is brought out as a conductor, it becomes the neutral conductor (N). Neutral is part of the normal power circuit — it carries current whenever single-phase loads are connected between a phase and neutral. Completing the load circuit is its only intended function.

A lamp supplied between phase and neutral:

```
Phase ───── Switch ───── Lamp ───── Neutral
```

Current flows from the transformer winding through the phase conductor, through the lamp, and returns to the transformer winding through the neutral conductor. No neutral means no return path means no current.

## What Earth Is

Earth (or ground) is a deliberate connection between the electrical system and the general mass of earth via an electrode — a copper-clad rod driven into the soil, a buried grid, or a plate. This connection establishes a common zero-voltage reference point for the entire system.

Earth is **not** part of the normal load circuit. It carries current only during abnormal conditions — faults, lightning surges, or switching transients.

## Neutral vs Earth

| Neutral | Protective Earth (PE) |
|---------|----------------------|
| Carries current during normal operation | Carries current only during faults |
| Part of the load circuit | Safety conductor |
| Connected to transformer star point | Connected to exposed metal parts (enclosures, frames, trays) |
| Required for single-phase loads to function | Required for protection against indirect contact |

## Why Connect Neutral to Earth?

At the transformer, the neutral point is intentionally bonded to earth:

```
Transformer neutral ● ─── Earth electrode ─── Soil
```

Two reasons:

### 1. Voltage Reference Stabilization

Without earthing, the transformer secondary floats. Its voltage relative to the earth around it is undefined. Capacitive coupling, leakage currents, and atmospheric effects cause unpredictable voltage drift. Earthing fixes the neutral at approximately 0 V relative to the surrounding earth, so the phase voltages are known and stable relative to ground.

A 230/400 V system with earthed neutral:

```
L1, L2, L3  ≈ 230 V to earth each
Neutral      ≈ 0 V to earth
L1-L2        ≈ 400 V phase-to-phase
```

### 2. Fault Current Return Path

If a phase conductor contacts a metal enclosure, the fault current path must return to the transformer neutral to operate the overcurrent protection. The earth connection at the neutral provides that path — through the earth electrode, the soil, the PE conductor, and back through the transformer neutral-to-earth bond.

## Does Fault Current Flow Through the Soil?

This is the most common misconception. The earth is not an infinite current sink. Current must always form a complete loop back to its source (the transformer winding).

In a TN system (the most common), the fault return path is almost entirely metallic:

```
Transformer winding
  → Phase conductor
  → Fault point
  → Metal enclosure
  → PE conductor
  → Neutral-to-earth bond
  → Back to transformer winding
```

The soil is hardly involved — the impedance is dominated by the copper conductors. This is why TN fault currents are high (hundreds to thousands of amps) and can trip conventional overcurrent devices.

In a TT system (where the consumer has a local earth electrode independent of the supply), the fault current does pass through the soil between the consumer's electrode and the supply's electrode. The soil resistance (typically 10-200 Ω) limits the fault current to tens of amps at most — too low to trip a standard breaker. This is why TT systems require RCDs.

## Protective Earth (PE) Conductor

The green/yellow conductor in every cable is the Protective Earth. It connects:
- Motor frames
- Switchboard enclosures
- Cable tray sections
- Transformer tanks
- Any metallic part that a person might touch

If a live conductor contacts any of these, the PE provides a low-impedance path for fault current to return to the source, enabling the protective device to trip.

## The Five IEC Conductor Types

IEC 60364-5-54 distinguishes five distinct elements that all involve the word "earth." Each has a specific definition and a different job. Confusion arises when they are used interchangeably.

```
                    🌍 Earth (the planet)
                       │
                 Earth Electrode
                       │
                 Earthing Conductor
                       │
              Main Earthing Terminal (MET)
               │           │            │
               │           │            │
              PE         Bonding      Neutral
          Conductors    Conductors    Connection*
               │           │
               │           │
         Equipment      Pipes, Steel,
         Enclosures     Building Frame
```

*Neutral connection depends on the earthing system (TN, TT, IT) — see [[Notes/EEE/Earthing/earthing-systems]]

### 1. Earth

Not a conductor. The planet itself. IEC 60050 defines it as the conductive mass of the Earth whose potential is conventionally taken as zero. Every other element in the earthing system ultimately references this.

### 2. Earth Electrode

The physical interface buried in the soil — a copper-clad steel rod, a buried copper strip, a plate, or a concrete-embedded foundation loop. Its job is to provide electrical contact between the installation and the earth mass. See [[Notes/EEE/Earthing/earthing-electrodes]].

During normal operation, the earth electrode carries essentially no current. Its role is passive — voltage reference, surge dissipation, and fault current return path for TT systems.

### 3. Earthing Conductor

The wire connecting the Main Earthing Terminal (MET) to the earth electrode. Nothing else. This is a narrow, specific definition in IEC. Many people call every green/yellow wire an "earthing conductor" — this is incorrect. The earthing conductor is only the single conductor (or set of conductors in parallel) that links the MET to the electrode.

Minimum cross-section per IEC 60364-5-54: 6 mm² copper or 50 mm² steel.

### 4. Protective Conductor (PE)

The green/yellow conductors running throughout the installation. PE conductors connect all exposed-conductive-parts (motor frames, switchboard enclosures, cable trays, transformer tanks) back to the MET.

PE conductors do not necessarily go directly to the earth electrode. The path is:

```
Equipment enclosure
  → PE conductor
  → MET
  → Earthing conductor (if fault current needs to reach earth)
  → Earth electrode
```

Or in a TN system:

```
Equipment enclosure
  → PE conductor
  → MET
  → Supply neutral-to-earth bond
  → Transformer winding
```

The MET is the junction where PE and the earthing conductor meet.

### 5. Bonding Conductor

A protective conductor provided for equipotential bonding. Bonding conductors connect extraneous-conductive-parts (water pipes, gas pipes, building steel, structural reinforcement) to the MET.

The purpose is not primarily fault current — it is maintaining all metal parts in a zone at the same potential, so that a person touching two different metal objects simultaneously experiences no dangerous voltage difference.

Minimum cross-section per IEC 60364-5-54: half of the largest PE conductor, minimum 6 mm² copper, maximum 25 mm² (may be relaxed in some national standards).

## Exposed-Conductive-Part vs Extraneous-Conductive-Part

These two terms are often confused but have distinct IEC definitions:

### Exposed-Conductive-Part

A conductive part of electrical equipment that can be touched and is not normally live, but can become live when basic insulation fails.

Examples:
- Motor frame
- Switchboard door and enclosure
- Transformer tank
- Metal enclosure of a washing machine
- Cable armor and metallic sheathing

These parts are connected to the PE conductor.

### Extraneous-Conductive-Part

A conductive part not forming part of the electrical installation that is liable to introduce a potential, generally the potential of a local earth.

Examples:
- Metallic water supply pipe entering the building
- Gas pipe
- Building structural steelwork
- Reinforcing steel in concrete
- Metal heating ducts
- Metallic compressed air lines

These parts are connected to the MET via bonding conductors.

The distinction matters because bonding an extraneous-conductive-part prevents it from introducing a dangerous potential difference relative to the installation's equipotential zone. PE conductors, on the other hand, ensure fault current has a low-impedance path back to the source.

## The Main Earthing Terminal (MET)

The MET is the central hub of the entire earthing system. Every conductor converges here:

```
                Earth Electrode
                     │
                Earthing Conductor
                     │
                     ▼
           Main Earthing Terminal
          │       │        │
          │       │        │
        PE    Bonding    Neutral
     Conductors  Conductors  Connection*
          │       │        │
          │       │        │
     Equipment  Pipes,   Transformer
     Enclosures  Steel   Star Point*
```

*Neutral connection at the MET depends on the earthing system. In a TN-C-S installation, the PEN is bonded to the MET at the service entrance. In a TT installation, there is no neutral connection at the MET — only PE, bonding, and earthing conductors meet here.

IEC 60364-5-54 requires the following to be connected to the MET:
- Protective bonding conductors
- Earthing conductors
- Protective conductors (PE)
- Functional earthing conductors, if any

## The Removable Link

The connection between the MET and the earthing conductor (or between the MET and the neutral) often includes a removable link or bolted connection. This link serves a specific testing purpose.

To measure the earth electrode resistance, the installation must be isolated from the electrode. If the building remains connected during testing, the test current sees multiple parallel return paths — building steel, bonded pipes, cable armoring, and other earth electrodes. The measured resistance is artificially low and meaningless.

Opening the removable link forces the test current through only the earthing conductor and the earth electrode, giving the true electrode-to-soil resistance.

Not all installations have a visible removable link — some use a bolted connection designed to be undone with a tool. The principle is the same: the MET-to-electrode connection must be separable for testing.

## Two Overlapping Systems

The entire earthing system can be understood as two separate systems that coexist in the same installation:

### Normal Power System

```
Transformer → Phase → Load → Neutral → Transformer
```

Current flows through this loop continuously during normal operation. The conductors are sized for the load current. The neutral provides the return path.

### Protective System

```
Earth Electrode → Earthing Conductor → MET → PE → Equipment Cases
MET → Bonding Conductors → Pipes, Steel, Building Frame
```

Under normal conditions, almost no current flows in the protective system. It sits idle — a static safety net. Only when insulation fails does the protective system become part of the fault current loop, providing a low-impedance path so protective devices operate quickly (TN) or enabling an RCD to detect the imbalance (TT).

The mental model:

| System | Conductors | Carries current | Purpose |
|--------|-----------|----------------|---------|
| Normal power | L1, L2, L3, N | Continuously | Deliver energy to loads |
| Protective | PE, bonding, earthing conductor, earth electrode | Only during faults | Safety — prevent shock, clear faults |

The earthing conductor, MET, PE, and bonding conductors carry fault current only — never load current (unless the neutral-earth bond is downstream of the MET in a TN-C system, which has its own constraints).

## The Source-Loop Principle

Every earth fault forms a complete loop:

```
                    ┌──────────────────────┐
                    │   Transformer        |
                    │   Secondary Winding  |
                    └──┬────────────────┬──┘
                       │                │
                  Phase conductor    Neutral-to-earth bond
                       │                │
                       ▼                ▼
                   Fault point ─── PE conductor 
                       │
                   Metal enclosure
```

The impedance of this entire loop is the **earth fault loop impedance** (Zs). The fault current is:

```
Ifault = U0 / Zs
```

Where U0 is the nominal phase-to-earth voltage (230 V) and Zs is the total loop impedance from source through phase conductor, fault, PE conductor, and back to source.

For the protective device to trip within the required time, Ifault must exceed the device's trip threshold. This means Zs must be low enough — which is why the PE conductor must be sized appropriately and the earth fault loop impedance must be verified during commissioning.

## References

- IEC 60364-1. *Low-voltage electrical installations — Fundamental principles.*
- IEC 60364-4-41. *Protection for safety — Protection against electric shock.*
- IEC 60364-5-54:2011+A1:2021. *Selection and erection of electrical equipment — Earthing arrangements and protective conductors.*
- IEC 60050-826. *International Electrotechnical Vocabulary — Electrical installations.*
- Schneider Electric. *Electrical Installation Guide.* Chapter E: Earthing schemes. [[source]](https://www.electrical-installation.org/enwiki/Earthing_connections)
- ABB. *Technical Application Papers No. 3: Distribution systems and protection against indirect contact and earth fault.*
- BS 7671. *Requirements for Electrical Installations (IET Wiring Regulations).*
