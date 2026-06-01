---
type: topic
tags: [eee, transformers, control-voltage, 24v]
created: 2026-06-01
status: building
parent: "[[MOC — Electrical Installation]]"
sources:
  - "[[BMS Controls Training — 6hr Video]]"
---

# Control Transformers & 24V Systems

## Why 24V?

**Safety.** The touch voltage threshold is 50V. Anything above that can be lethal under fault conditions. 230V on a panel door (switches, indicator lights, push buttons that an operator touches) is dangerous.

24V AC is the standard control voltage for BMS and most industrial control panels. Some systems use 24V DC (with a power supply instead of a transformer), but the principle is the same — step down from mains voltage to a safe level for control circuits.

## Transformer vs DC Power Supply

| | Transformer | DC Power Supply |
|--|-------------|-----------------|
| Output | AC | DC |
| Typical use | BMS panels, traditional controls | PLC-based systems, electronics |
| Simplicity | Fewer components, more robust | Needs rectification, filtering |
| BMS convention | More common | Either works |

Most BMS systems use a transformer. The secondary side is 24V AC.

## Secondary Distribution

### 0V Rail

From the transformer secondary, the 0V rail distributes via **Wago terminal blocks** with push-in busbar connections. Not daisy-chained in series — if one connection fails in a daisy chain, everything downstream dies. Multiple terminal blocks provide **redundancy** and make fault-finding easier.

### 24V Rail

From the transformer → **MCB or fuse** first (protection) → then distributed to control circuits. The fuse/MCB protects the transformer secondary from overloads.

## Key Point

The transformer is the boundary between the dangerous side (230V) and the safe side (24V). Everything on the secondary side is touch-safe. Everything on the primary side is not. This distinction drives how the panel is physically laid out — the 230V and 24V sections are typically separated within the enclosure.
