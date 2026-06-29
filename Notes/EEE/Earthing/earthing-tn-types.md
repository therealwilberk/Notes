---
tags: [eee, earthing, grounding, tn-system, tn-s, tn-c, tn-c-s, pen-conductor]
aliases: ["TN-S System", "TN-C System", "TN-C-S System", "PEN Conductor", "PME", "Protective Multiple Earthing"]
parent: "[[Notes/EEE/Earthing/earthing-systems]]"
created: 2026-06-27
status: complete
---

# TN Subtypes — TN-S, TN-C, TN-C-S

Within the TN system classification (supply neutral earthed, exposed parts connected to the neutral), three subtypes define how the neutral (N) and protective earth (PE) conductors are arranged along the distribution path.

## TN-S (Separate N and PE Throughout)

The neutral and protective earth are separate conductors from the transformer to every load.

```
Transformer              Building
══════════               ════════════
  L1 ─────────────────── L1
  L2 ─────────────────── L2
  L3 ─────────────────── L3
  N  ─────────────────── N
  PE ─────────────────── PE ─── Metal enclosures
   │
Earth electrode
```

**Conductors in the cable:** Five — L1, L2, L3, N, PE.

**Fault current path.** Phase → fault → enclosure → PE conductor → transformer neutral point. Entirely metallic, no involvement of the soil.

**Typical Ze.** 0.20-0.80 Ω depending on transformer size and cable distance. The lowest and most predictable of the TN subtypes (after TN-C-S with a utility PEN).

**Advantages:**
- No risk of the neutral current flowing through the PE conductor under normal conditions
- No risk of the PE conductor being energized by a broken neutral
- Clean separation of functions — N carries load current, PE carries only fault current
- Best electromagnetic compatibility — no neutral current in the protective conductor means no stray magnetic fields in data or instrumentation circuits

**Disadvantages:**
- Requires five conductors from the transformer — more copper than TN-C
- Higher installation cost than TN-C

**Applications:**
- Data centers and telecommunications (EMC requirements)
- Healthcare facilities
- Laboratory installations
- Commercial buildings with sensitive electronics
- Installations where the supply authority provides a separate PE conductor

**In switchboards.** The neutral bar and earth bar are kept separate. Main bonding connects the earth bar to the incoming metallic services (water, gas, structural steel) at one point — the main earthing terminal. The neutral bar is bonded to earth only at the transformer and (in some national regulations) at the service entrance via the neutral-to-earth link.

## TN-C (Combined N and PE — PEN)

The neutral and protective earth are combined into a single conductor called PEN (Protective Earth and Neutral) throughout the entire system.

```
Transformer              Building
══════════               ════════════
  L1 ─────────────────── L1
  L2 ─────────────────── L2
  L3 ─────────────────── L3
  PEN ────────────────── PEN ─── Metal enclosures
   │
Earth electrode
```

**Conductors in the cable:** Four — L1, L2, L3, PEN.

**Fault current path.** Phase → fault → enclosure → PEN conductor → transformer neutral point. Metallic, but the same conductor carries both neutral current and fault current.

**Typical Ze.** 0.05-0.35 Ω. The lowest of all subtypes because the PEN conductor is typically a large cross-section (often equal to the phase conductors).

**Critical constraint — PEN break danger.** If the PEN conductor opens upstream, the return path for load current is lost. The neutral point of the installation floats, and the load current seeks an alternative return path — typically through the earth electrode or through bonded services. The voltage at the neutral point can rise to several hundred volts relative to earth. All exposed metalwork bonded to the PEN rises to this voltage simultaneously.

This is the primary reason TN-C is restricted or prohibited in many jurisdictions.

**Constraints per IEC 60364:**
- The PEN conductor must have a minimum cross-section of 10 mm² copper or 16 mm² aluminum
- TN-C is not permitted for circuits supplying portable equipment (flexible cables cannot provide the required mechanical protection for a combined conductor)
- TN-C is not permitted in hazardous areas (explosive atmospheres)
- The PEN conductor must be insulated or otherwise protected against mechanical damage to the same standard as phase conductors
- TN-C is prohibited for installations with sensitive electronic equipment (the neutral current in the PEN creates voltage drops that appear on the enclosure reference)

**Applications:**
- Overhead distribution networks (rural and suburban)
- Industrial installations with large fixed equipment
- Situations where conductor economy is the overriding concern

**In switchboards.** With a PEN incoming supply, the neutral bar and earth bar are bonded together at the service entrance. Downstream within the installation, separate N and PE bars must be established (converting to TN-S internally). The PEN conductor is connected to the PE bar, and the N bar is linked to it.

## TN-C-S (Combined PEN Upstream, Separate N and PE Downstream)

The neutral and protective earth are combined in a single PEN conductor for the supply distribution network, then separated into distinct N and PE conductors at the service entrance.

```
Utility Network          Service Entrance         Installation
══════════════           ════════════════         ════════════
  L1 ─────────────────── L1 ───────────────────── L1
  L2 ─────────────────── L2 ───────────────────── L2
  L3 ─────────────────── L3 ───────────────────── L3
  PEN ────────────────── ● ── N ───────────────── N
                          └── PE ──────────────── PE ─── Enclosures
   │
Earth electrode
```

This is also known as **Protective Multiple Earthing (PME)** in the UK, or as the neutral being earthed at multiple points along the distribution.

**Conductors in the supply cable:** Four — L1, L2, L3, PEN.

**Conductors in the installation:** Five — L1, L2, L3, N, PE.

**Separation point.** At the service entrance (main switchboard, main distribution board), the incoming PEN is connected to the main earthing terminal. From there, separate N and PE bars distribute to downstream circuits. The neutral bar and earth bar are bonded together at this single point — and only at this point — via the main earthing link.

**Typical Ze.** 0.05-0.35 Ω. The lowest Ze of any system because the PEN conductor in the supply network is heavily bonded to earth at multiple points (hence PME), effectively paralleling many earth return paths.

**Fault current path.** Phase → fault → enclosure → PE conductor (within installation) → main earthing terminal → PEN conductor (supply) → transformer neutral. The multiple earth connections along the PEN provide additional parallel return paths through the soil, further reducing the impedance.

**PEN break behavior.** If the PEN conductor opens upstream, the installation's N and PE are still bonded together at the service entrance. The multiple earth electrodes on the supply side (and the consumer's own electrode) provide an alternative return path. The voltage rise is less severe than in a pure TN-C system, but still significant. For this reason, the supply authority typically limits PME to areas where the combined earth electrode resistance is low enough.

**Advantages:**
- Economical — the supply utility saves one conductor over the distribution distance
- Lowest Ze values — excellent for overcurrent device operation
- Widely understood standard — installed globally

**Disadvantages:**
- Requires clear labeling of the separation point
- If PEN and N are confused downstream, the PE conductor carries neutral current under normal conditions (a common installation error)
- Not permitted for temporary supplies (caravan parks, construction sites) in some jurisdictions
- Electromagnetic compatibility concerns in installations with high neutral currents

**Applications:**
- The dominant system in the UK (PME), Germany, and most countries with underground residential distribution
- Standard arrangement for new commercial and residential buildings served by a utility network

**In switchboards.** The incoming PEN connects to the earth bar. The neutral bar is connected to the earth bar via a removable link at the service entrance. Downstream, all circuits have separate N and PE conductors. The earth bar is bonded to the building's main earthing conductor and to all incoming metallic services.

## Summary Comparison

| Property | TN-S | TN-C | TN-C-S (PME) |
|----------|------|------|-------------|
| Supply conductors | 5 (L1, L2, L3, N, PE) | 4 (L1, L2, L3, PEN) | 4 (L1, L2, L3, PEN) |
| Installation conductors | 5 (N + PE separate) | 4 (PEN continues) | 5 (separated at origin) |
| Typical Ze | 0.20-0.80 Ω | 0.05-0.35 Ω | 0.05-0.35 Ω |
| PEN break danger | N/A (separate conductors) | Severe — enclosure energized | Moderate — multiple earth paths |
| Permitted for portable equipment | Yes | No | Yes (downstream of separation) |
| Permitted in hazardous areas | Yes | No | Yes (downstream of separation) |
| EMC performance | Best — no N current in PE | Worst — N current in PE | Good — no N current in PE downstream |
| Installation cost | Highest | Lowest | Moderate |
| Dominant use case | Data centers, hospitals | Overhead distribution | Urban residential/commercial |

## Converting Between Subtypes

The separation point in TN-C-S is where the transition from combined to separate occurs. The rules at this point:

1. The PEN is connected to the main earthing terminal (MET)
2. The PE bar is connected to the MET
3. The N bar is connected to the PE bar via a link — this link is the neutral-to-earth bond
4. Beyond this point, N and PE must never be reconnected — no downstream neutral-to-earth bonds are permitted
5. The PEN conductor must not be switched (no switch or breaker in the PEN)
6. A PEN terminal must be provided upstream of any main switch

## References

- IEC 60364-1. *Low-voltage electrical installations — Fundamental principles.*
- IEC 60364-4-41. *Protection against electric shock.*
- IEC 60364-5-54. *Earring arrangements and protective conductors.*
- BS 7671. *Requirements for Electrical Installations. Section 8: Earthing Arrangements.*
- UK Electricity Safety, Quality and Continuity Regulations (ESQCR) 2002.
- ABB. *Technical Application Papers No. 3: Distribution systems and protection against indirect contact and earth fault.*
