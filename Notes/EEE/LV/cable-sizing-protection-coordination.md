---
tags: [eee, lv, cables, protection, coordination, overload]
aliases: ["IB In Iz I₂", "Protection Coordination", "Overload Protection", "Cable Protection Coordination", "Conventional Tripping Current"]
parent: "[[Notes/EEE/LV/lv-switchgear]]"
created: 2026-06-29
status: complete
---

# Cable Sizing — Protection Coordination (IB, In, Iz, I₂)

Every circuit designer must coordinate four currents: the load current, the protective device rating, the cable capacity, and the guaranteed trip threshold.

## The Four Currents

```
Load ───── Cable ───── Breaker
           ↑           ↑
          Iz           In
           ^
     carries IB
```

### IB — Design (Load) Current

The current the equipment draws during normal operation. Determined from the load, not the cable.

Examples: LED lighting circuit → 3 A, socket circuit → 18 A, motor → 42 A.

### In — Rated Current of the Protective Device

The breaker or fuse nameplate rating. Selected from standard values (6 A, 10 A, 16 A, 20 A, 25 A, 32 A, 40 A, 50 A, 63 A, etc.).

Must be at least IB, otherwise the device trips during normal operation:

```
IB ≤ In
```

Example: load = 17 A → 16 A breaker is inadequate, 20 A breaker is acceptable.

### Iz — Current-Carrying Capacity of the Cable (Installed)

The maximum continuous current the installed cable can carry without exceeding its temperature limit. Depends on the cable material and construction, but also heavily on installation method, ambient temperature, grouping, and thermal insulation.

The same 4 mm² copper PVC cable has different Iz depending on where and how it is installed: clipped to a wall (~37 A), buried in insulation (~25 A), grouped with other cables (lower still). The copper is identical — its ability to lose heat is not.

### I₂ — Conventional Tripping Current

The current at which the protective device is guaranteed to trip within the conventional time defined by the standard (typically 1 hour for breakers, variable for fuses). Not the fault current.

For a 20 A breaker:
- 20 A → may never trip
- 23 A → may trip eventually
- 29 A → guaranteed to trip (this is I₂)

For most circuit breakers, I₂ ≈ 1.45 × In. For fuses, I₂ ranges from approximately 1.6 to 1.9 × In, which is why a correction factor k₃ is needed when fuses are used.

## Condition 1: IB ≤ In ≤ Iz

Read left to right:

The load current must be less than the breaker rating, and the breaker rating must not exceed the cable's installed capacity.

Example:
- IB = 18 A
- In = 20 A (breaker)
- Iz = 27 A (cable installed)

```
18 ≤ 20 ≤ 27 ✓
```

All three values are satisfied.

## Condition 2: I₂ ≤ 1.45 × Iz

This ensures the cable does not overheat before the protective device trips during an overload.

Example:
- Iz = 20 A
- 1.45 × Iz = 29 A
- Breaker I₂ = 28 A

```
28 ≤ 29 ✓
```

The cable is protected.

If the device only guaranteed tripping at 35 A:

```
35 > 29 ✗
```

The cable could overheat before the device opened. A larger cable or a different protective device is needed.

## Why the 1.45 Factor

The factor comes from the typical overload behaviour of cables. A cable can carry a moderate overload (up to 1.45 × Iz) for the conventional time without suffering damage. The protective device must clear the overload within that time, so its guaranteed trip current I₂ must be at or below 1.45 × Iz.

## Fuse Correction Factor (k₃)

Fuses have a higher I₂ relative to In than circuit breakers. To use a fuse where a breaker would be rated at In, the cable Iz must be sized to accommodate the fuse's higher trip threshold. This is handled by applying a factor k₃ during selection.

## References

- IEC 60364-4-43. *Protection against overcurrent.*
- IEC 60947-2. *Low-voltage switchgear and controlgear — Circuit-breakers.*
- IEC 60269. *Low-voltage fuses.*
- Schneider Electric. *Electrical Installation Guide.* Chapter G: Sizing and protection of conductors. [[source]](https://www.electrical-installation.org/enwiki/Overcurrent_protection_principles)
- Schneider Electric. *Practical values for a protective scheme.* [[source]](https://www.electrical-installation.org/enwiki/Practical_values_for_a_protective_scheme)
