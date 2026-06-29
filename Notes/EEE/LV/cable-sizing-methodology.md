---
tags: [eee, lv, cables, sizing, methodology, ampacity, voltage-drop, installation-method]
aliases: ["Cable Sizing Methodology", "Conductor Sizing", "General Method for Cable Sizing", "Cable Selection", "Iz Tables"]
parent: "[[Notes/EEE/LV/lv-switchgear]]"
created: 2026-06-29
status: complete
---

# Cable Sizing — General Methodology

Cable sizing is a filtering process. No single table gives the answer. Each step eliminates options until one cross-section satisfies every requirement.

## The Sizing Workflow

```
Load
  │
  ▼
Calculate IB
  │
  ▼
Choose cable type
  │
  ▼
Determine installation method
  │
  ▼
Apply correction factors
  │
  ▼
Select cross-sectional area
  │
  ▼
Check voltage drop
  │
  ▼
Check short-circuit withstand
  │
  ▼
Select protective device
```

See [[Notes/EEE/LV/cable-sizing-protection-coordination]] for the four-circuit-current framework (IB, In, Iz, I₂) and coordination rules.

## Step 1 — Determine the Design Current (IB)

IB comes from the load. For a three-phase motor:

```
IB = P / (√3 × U × PF × η)
```

Example: 15 kW motor, 400 V, PF = 0.85, η = 0.9 → IB ≈ 30 A.

For single-phase loads:

```
IB = P / (U × PF)
```

## Step 2 — Choose the Cable Characteristics

Before consulting any ampacity tables, decide:

- Conductor material: copper or aluminium
- Insulation type: PVC (70 °C or 90 °C), XLPE (90 °C), EPR
- Number of loaded conductors
- Single-core or multicore cable

Each choice changes the allowable current. A 10 mm² XLPE cable can carry more than a 10 mm² PVC cable of the same construction because XLPE tolerates a higher operating temperature.

## Step 3 — Identify the Installation Method

Installation method is one of the largest influences on cable size. IEC 60364-5-52 groups methods into reference letters (A1, A2, B1, B2, C, D, E, F, G).

| Ref | Description | Example |
|-----|------------|---------|
| A1 | Insulated conductors in conduit in a thermally insulated wall | Buried in building insulation |
| A2 | Multicore cable in conduit in a thermally insulated wall | Same, but with multicore cable |
| B1 | Insulated conductors in conduit on a wall | Surface-mounted conduit |
| B2 | Multicore cable in conduit on a wall | Surface-mounted conduit, multicore |
| C | Clipped direct or on a wall — single-core or multicore | Cable clipped to a wall surface |
| D | Buried in the ground | Underground cable |
| E | On a perforated cable tray — single-core | Open cable tray, single cores |
| F | On a perforated cable tray — multicore | Open cable tray, multicore |
| G | Bare conductors on insulators | Open busbar or bare wires |

The same 10 mm² cable might carry ~42 A in method A1 and ~57 A in method C. The copper is identical — only the heat dissipation changed.

The cable must also be harmonised with the method: if the selected cross-section appears in the table for the chosen method, proceed. If not, a different cable construction or a different method should be used.

## Step 4 — Apply Correction Factors

Published Iz tables assume ideal conditions (30 °C air, 20 °C ground, single circuit, no thermal insulation). Real installations differ.

Common correction factors:

- **Ambient temperature (k₁):** Hotter environments reduce Iz. A 30 °C-rated cable in a 45 °C ambient might carry only 0.79 of its tabulated value.
- **Grouping (k₂):** Multiple cables in proximity reduce heat dissipation. For 5 circuits bunched, the factor might be 0.60–0.70.
- **Thermal insulation (k₃):** A cable buried in insulation has drastically reduced heat loss.
- **Burial depth and soil thermal resistivity (for buried cables).**

Example:
- Table Iz = 57 A (method C, 10 mm² copper PVC)
- Ambient factor = 0.91
- Grouping factor = 0.80
- Corrected Iz = 57 × 0.91 × 0.80 ≈ 41.5 A

The cable did not become smaller — it carries less safely under those conditions.

## Step 5 — Select the Smallest Cable Satisfying IB ≤ In ≤ Iz

With corrected Iz:

- Compare standard breaker ratings In against IB and Iz
- Select the smallest cable where the inequality holds

Example:
- IB = 30 A
- In = 32 A (standard breaker)
- 4 mm² corrected Iz = 28 A → fails (In > Iz)
- 6 mm² corrected Iz = 37 A → passes

Select 6 mm².

Cable sizing is iterative: start with a tentative cross-section, look up its Iz for the chosen installation method, apply correction factors, check the inequality, and move up a size if needed until all conditions are met.

## Step 6 — Check Voltage Drop

Ampacity compliance does not guarantee acceptable voltage at the load.

Permitted voltage drop (typical): 3 % for lighting circuits, 5 % for power circuits (values vary by national standard).

Voltage drop approximation for three-phase:

```
ΔU = √3 × IB × (R cos φ + X sin φ) × L
```

For a 6 mm² cable, 250 m long, 30 A load, the voltage drop may exceed limits even though the thermal rating is adequate. If it does, increase the cable size regardless of the thermal check.

## Step 7 — Check Short-Circuit Withstand (Adiabatic)

Verify that the cable can survive the worst-case fault until the protective device clears it (see [[Notes/EEE/LV/cable-sizing-adiabatic]]):

```
I²t ≤ k²S²
```

A cable may carry 30 A continuously and have acceptable voltage drop but still fail a 5 kA fault lasting 0.8 s. Remedies:

- Increase the cable cross-section S
- Choose a faster protective device (lower t)
- Use a current-limiting device

## Interpreting the Current-Carrying Tables

The large ampacity tables (IEC 60364-5-52, Figures G20–G25 in the Schneider guide) answer one question: for a given cable type and installation method, what continuous current can it carry?

Example — 6 mm² copper, PVC insulation, 3 loaded conductors:

| Method | Approx. Iz (A) |
|--------|---------------:|
| A1 | 31 |
| B2 | 34 |
| C | 41 |
| D1 | 38 |

The cross-sectional area never changed. Only the installation method changed, so the allowable current changed.

A common misconception: "a 6 mm² cable is a 41 A cable." The accurate statement: a 6 mm² copper cable with PVC insulation, three loaded conductors, installed by method C at 30 °C ambient, carries 41 A.

## Summary: What Cable Sizing Checks

A correctly sized cable satisfies every requirement simultaneously:

- Carries the expected load continuously (IB ≤ In ≤ Iz)
- Keeps voltage drop within limits (ΔU ≤ ΔU_max)
- Survives prospective short circuits (I²t ≤ k²S²)
- Coordinates with the protective device (I₂ ≤ 1.45 × Iz)

Cable sizing is fundamentally a thermal problem with electrical constraints. The cross-sectional area is selected so that in its actual installation environment, the conductor stays within its temperature limits under every operating condition.

## References

- IEC 60364-5-52. *Selection and erection of electrical equipment — Wiring systems.*
- IEC 60364-4-43. *Protection against overcurrent.*
- IEC 60364-4-44. *Protection against voltage disturbances and electromagnetic disturbances.*
- Schneider Electric. *Electrical Installation Guide.* Chapter G: Sizing and protection of conductors. [[source]](https://www.electrical-installation.org/enwiki/General_method_for_cable_sizing)
- Schneider Electric. *Conductor sizing: methodology and definition.* [[source]](https://www.electrical-installation.org/enwiki/Conductor_sizing:_methodology_and_definition)
- BS 7671. *Requirements for Electrical Installations (IET Wiring Regulations).* Appendix 4.
