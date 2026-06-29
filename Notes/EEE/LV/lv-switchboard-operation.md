---
tags: [lv, switchboard, power-distribution, protection, operation]
aliases: ["Switchboard Operation", "How a Switchboard Works", "LV Switchboard Operation", "UL 891 Switchboard"]
parent: "[[Notes/EEE/LV/lv-switchgear]]"
created: 2026-06-27
status: complete
---

# How a Switchboard Operates

## The Distribution Hierarchy

Power moves through a building in stages. The switchboard sits at the top of the LV distribution chain, immediately downstream of the transformer:

```
Utility Transformer (MV/LV)
       │
       ▼
  ┌─────────────┐
  │ Switchboard  │  ← Main LV distribution point (UL 891)
  │ (MDB)        │
  └──────┬──────┘
         │
    Feeder circuits
         │
         ▼
  ┌─────────────┐
  │ Panelboards  │  ← Branch circuit distribution (UL 67)
  │ (SMDBs)      │
  └──────┬──────┘
         │
    Branch circuits
         │
         ▼
       Loads
```

In a small facility, the switchboard may be fed directly from the utility transformer and act as service entrance equipment. In a large facility, the switchboard receives power from an upstream LV switchgear assembly via feeder breakers.

## Physical Construction

A switchboard is a dead-front, free-standing assembly. "Dead-front" means no energized parts are exposed on the operating face — operators interact only with breaker handles, meters, and dead-front covers. This is the defining safety feature of a UL 891 switchboard.

### Sections

A switchboard lineup consists of one or more vertical steel sections bolted together:

**Service (Main) Section** — receives incoming power. Contains the main disconnect (circuit breaker or fused switch), utility metering provisions (CTs and PTs), and neutral-to-ground bonding for service entrance applications.

**Distribution Sections** — receive power from the service section and divide it into feeder circuits. Contain group-mounted or individually mounted feeder breakers.

**Pull Section** — an empty section used to route incoming cables from underground or overhead to the main device. Eliminates the need to bend large conductors inside the service section.

### Internal Compartments

Unlike switchgear (UL 1558) which mandates full compartmentalization between breaker, bus, and cable, a UL 891 switchboard uses a dead-front, open-chassis design:

- The front face is dead — covers, doors, and breaker faces
- Behind the dead-front, busbars and conductor connections are accessible when covers are removed
- Internal barriers are optional (not required by UL 891 as they are by UL 1558)
- Side barriers between sections are provided for arc containment

This open-chassis design makes switchboards more compact and less expensive than switchgear, at the cost of not isolating compartments from each other.

### Bus System

The bus is the backbone. Two levels exist:

**Horizontal (Through) Bus** — runs the full length of the lineup, connecting all sections. Mounted at the top, middle, or bottom of the enclosure depending on the design. Made of copper or aluminum bars (tin-plated or silver-plated), sized for continuous current from 800 A to 6000 A. Braced to withstand short-circuit forces up to the full interrupting rating (typically 100 kA at 480 V).

**Vertical (Riser) Bus** — taps off the horizontal bus within each distribution section. Runs vertically to feed group-mounted breaker positions. Rated up to 2250 A typically. Breakers connect via copper straps. Vertical bus mounting slots allow breakers to be positioned at any location along the bus.

Bus support uses polyester standoff insulators on steel brackets. Insulation is optional — UL 891 permits smaller clearances and non-insulated busbars (unlike UL 1558). When clearances are insufficient, tape wrap or insulating sleeve is applied.

The neutral bus runs the full lineup length. The ground bus is a continuous bar bolted to the frame at the bottom of the cable compartment.

## Power Flow: Normal Operation

### Step 1: Incoming Power Enters

Power enters through incoming cables (top or bottom entry, overhead or underground). In a service entrance switchboard, these cables connect directly to the main breaker lugs or to a pull section that transitions to the main bus.

### Step 2: Main Device

The main overcurrent protective device (OCPD) — typically a UL 1066 power circuit breaker or a large UL 489 molded case circuit breaker — receives power first. In service entrance applications, this device serves as the single-point disconnect for the entire facility (per NEC Article 230.71, no more than six disconnects are allowed for the service).

When the main breaker is closed, power passes through to the horizontal bus. When open, the entire downstream system is de-energized (except for utility-side metering in hot-sequence configurations).

### Step 3: Horizontal Bus Distribution

The horizontal (through) bus carries the full rated current laterally across all sections. Each distribution section taps into this bus.

### Step 4: Vertical Bus Risers

Within each distribution section, vertical riser bus connects to the horizontal bus. These vertical busbars carry current vertically to feed individual breaker positions.

### Step 5: Feeder Breakers

Feeder breakers (typically UL 489 molded case circuit breakers or insulated case circuit breakers) are connected to the vertical bus. Each protects a downstream circuit. The breakers are group-mounted — multiple breakers share the same bus within a section without individual compartmentalization.

### Step 6: Outgoing Circuits

From the load side of each feeder breaker, power travels via:
- **Bus straps** — for larger breakers, directly connecting to outgoing bus extensions
- **Cables** — from breaker load terminals to cable lugs in the cable termination space
- **Busway connections** — for high-current feeds to downstream switchboards or MCCs

Outgoing cables exit through top or bottom of the enclosure.

## Power Flow During a Fault

When a fault occurs downstream of a feeder breaker:

1. The fault current flows from the utility transformer, through the main breaker, horizontal bus, vertical bus, and feeder breaker towards the fault
2. The feeder breaker's trip unit detects the overcurrent condition
3. The molded case breaker trips instantaneously (within 3-4 cycles) or after a programmed delay
4. The main breaker does not trip — it withstood the fault current because its trip settings are coordinated to allow downstream devices to clear first

In a properly coordinated system, only the device closest to the fault opens. The rest of the switchboard continues supplying unfaulted loads.

**Limitation:** Because switchboards use MCCBs that trip instantaneously above their instantaneous setting (3-cycle withstand), true selective coordination at high fault currents is not achievable. Only switchgear with LV-PCBs (30-cycle short-time withstand) can provide full selective coordination.

## Service Entrance Operation

When a switchboard serves as service entrance equipment:

1. Incoming utility cables enter the service section
2. Power passes through utility metering current transformers (CTs) — either on the line side (hot sequence) or load side (cold sequence) of the main disconnect
3. The neutral conductor is bonded to ground via a neutral-to-ground link
4. The ground bus is connected to the switchboard frame and to the system earth electrode
5. The main disconnect provides the service disconnecting means

**Hot sequence metering:** CTs on the line side — the meter remains energized even when the main breaker is off (utility can read the meter without the building being powered). Most common configuration.

**Cold sequence metering:** CTs on the load side — the meter de-energizes when the main breaker is opened. Used when local codes require it.

## Multiple Source Configurations

Switchboards can be configured with dual or triple supplies:

### Dual Supply, No Coupler

```
Transformer A ─── Main A ─── Bus Section A ─── Loads A
Transformer B ─── Main B ─── Bus Section B ─── Loads B
```

Each transformer feeds its own section. No connection between sections. If Transformer A fails, Loads A are lost. Simple but no redundancy.

### Dual Supply with Bus Coupler

```
Transformer A ─── Main A ─── Bus Section A
                              │
                          [Coupler CB]
                              │
Transformer B ─── Main B ─── Bus Section B
```

Normal operation: Main A and Main B closed, Coupler open. Each transformer feeds its half.

On loss of Transformer A:
1. Open Main A
2. Close the bus coupler
3. Transformer B now feeds both sections

The coupler can be manual or automatic (with transfer logic). Automatic schemes use break-before-make logic — the failed incomer is verified open before closing the coupler.

### Utility + Generator

```
Utility ─── Main CB ─── Bus
                         │
Generator ─── Gen CB ───┘
```

The generator breaker and utility main breaker are mechanically or electrically interlocked to prevent paralleling. Only one source is active at a time. On utility loss, the generator starts, the main breaker opens, and the generator breaker closes.

## Metering and Instrumentation

Current transformers (CTs) are mounted on the line or load side of the main breaker — one per phase. They step down the primary current to 5 A (or 1 A) for meters, relays, and trip units.

Voltage transformers (PTs) step down voltage for metering (typically 480 V to 120 V).

Typical instruments: ammeter, voltmeter with phase selector, wattmeter, power factor meter, energy meter (kWh). Digital multifunction meters are now standard.

Instrument compartments at the top of sections house PTs, control power transformers, terminal blocks, and relays.

## Control Wiring

Control wiring is kept separate from power conductors. Vertical wireways run the height of each section. Terminal blocks are mounted above or below each breaker position for secondary connections.

Standard control wire: #14 AWG SIS (stranded, insulated, synthetic) — 600 V rated, extra flexible. CT wiring uses #14 AWG or #10 AWG depending on the burden.

For draw-out breakers, finger-safe secondary connections (typically 54-72 connections per breaker) allow control wiring without removing the breaker from its compartment. When the breaker is racked out, secondary disconnects automatically separate.

## Switchboard Operator Actions

**Normal switching:**
1. Verify load conditions on downstream equipment
2. Open the feeder breaker by moving its handle to OFF
3. Tag and lockout per procedure

**De-energizing a section:**
1. Trip the main breaker (or individual feeder breakers if only partial isolation is needed)
2. Verify zero energy with a voltage tester
3. The dead-front design means no exposed energized parts when the doors are closed, but once covers are removed, busbars are exposed

**Restoring power:**
1. Close the feeder breaker
2. Verify voltage and load on instrumentation

See [[Notes/EEE/LV/lv-switchgear-ratings]] for how these parameters appear on nameplates and how they connect to thermal and fault-current design limits.

## Comparison: Switchboard vs Switchgear Operation

| Aspect | Switchboard (UL 891) | Switchgear (UL 1558) |
|--------|---------------------|---------------------|
| Internal access | Bus and cables exposed when covers removed | Compartmentalized — each compartment isolated |
| Breaker replacement | Must de-energize section for fixed-mount breakers | Draw-out breakers removable while bus is energized |
| Fault coordination | Limited — MCCBs trip in 3 cycles | Full — LV-PCBs withstand 30 cycles for coordination |
| Arc flash exposure | Higher — longer clearing time + open chassis | Lower — compartmentalization + arc-resistant options |
| Service continuity | Section must be de-energized to service breakers | Individual breaker drawn out, rest of section stays live |
| Installation | Front-accessible, wall-mountable | Requires rear access |
| Footprint | Smaller | Larger |

## References

- UL 891. *Switchboards.*
- ANSI/NEMA PB 2. *Deadfront Distribution Switchboards.*
- NEC Article 230. *Services.*
- NEC Article 240. *Overcurrent Protection.*
- IEEE C37.20.1. *Metal-Enclosed Low-Voltage Power Circuit Breaker Switchgear.* (comparison reference)
- Eaton. *Switchboard fundamentals.* (technical content only; vendor-specific content discarded)
- Siemens. *Basics of Switchboards.* (technical reference)
- ABB. *MaxSB Low Voltage Switchboard.* (technical reference)
