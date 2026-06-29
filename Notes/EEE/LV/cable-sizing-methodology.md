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

The current-carrying capacity (Iz) in IEC tables is determined under reference conditions. Real installations almost never match those conditions, so the cable is derated (or occasionally uprated) using correction factors:

```
Iz = Itable × k₁ × k₂ × k₃ × k₄ × ...
```

where Itable is the value from the IEC ampacity tables and each k accounts for one real-world condition.

### k₁ — Ambient Temperature

The tables assume 30 °C in air and 20 °C underground.

If a cable runs through a ceiling space at 45 °C, a PVC cable is already warmer before any current flows. Typical correction for 45 °C ambient with PVC insulation: k₁ ≈ 0.82.

```
Table ampacity = 37 A (4 mm² Cu PVC, method C)
Ambient factor  = 0.82
Corrected       = 37 × 0.82 ≈ 30.3 A
```

The cable effectively becomes a 30 A cable under those conditions.

### k₂ — Thermal Insulation

When a cable is buried in thermal insulation, heat cannot escape. Two identical cables differ only in their cooling:

- Cable A — clipped to a wall surface: heat escapes into the air.
- Cable B — buried in fibreglass insulation: heat is trapped.

The cable itself has not changed. Its cooling has. A typical factor for a cable in thermal insulation is k₂ ≈ 0.70.

### k₃ — Soil Thermal Resistivity (Buried Cables Only)

The soil acts as the cable's heatsink. Wet soil conducts heat away effectively; dry sand traps it. The IEC tables assume a soil thermal resistivity of 2.5 K·m/W. When the actual soil differs, a correction factor is applied.

| Soil Condition | k₃   |
|----------------|-----:|
| Very wet       | 1.21 |
| Wet            | 1.13 |
| Damp           | 1.05 |
| Standard (ref) | 1.00 |
| Very dry       | 0.86 |

A factor above 1.00 means the soil cools better than the reference, so permissible current increases. A factor below 1.00 means poorer cooling and a lower current rating.

### k₄ — Grouping

One of the largest derating factors. A single cable dumps heat into the surrounding air. Six cables touching each other create mutual heating — each cable heats its neighbours, and the middle cables become the hottest.

The grouping factor depends on:

- Number of circuits
- Spacing between cables
- Installation method (tray, conduit, free air, buried)
- Whether cables are touching or separated

For five circuits bunched, k₄ might be 0.60–0.70.

### Worked Example — All Factors Combined

Initial table value:

```
Iz = 37 A (4 mm² Cu PVC, method C)
```

Apply sequentially:

| Factor | Value | Cumulative Iz |
|--------|------:|--------------:|
| Table  | —     | 37.0 A |
| k₁ (ambient 45 °C) | 0.82 | 30.3 A |
| k₂ (thermal insulation) | 0.70 | 21.2 A |
| k₄ (grouping) | 0.80 | 17.0 A |

```
37 × 0.82 × 0.70 × 0.80 ≈ 17.0 A
```

A cable that looked adequate from the table alone is no longer suitable because the installation conditions are much harsher than the reference.

Two identical 4 mm² cables can legitimately have current ratings from roughly 20 A to over 40 A depending entirely on where and how they are installed — not because the copper changed, but because the thermal environment did.

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

Ampacity compliance does not guarantee acceptable voltage at the load. Ampacity answers: can the cable carry the current without overheating? Voltage drop answers: will the load still receive sufficient voltage to operate correctly? A cable can pass the first and fail the second.

Every cable has resistance (and AC impedance). As current flows, V_drop = I × Z (or approximately I × R for short LV circuits). The cable consumes part of the supply voltage:

```
Distribution board
230 V
 │
 │  Cable (voltage lost)
 ▼
Load
221 V
```

### Why Voltage Drop Matters

A resistive load (heater, oven, kettle) receiving 219 V instead of 230 V still works — it produces slightly less power. A motor receiving 360 V instead of 400 V develops less torque, draws more current, runs hotter, and may fail to start under load. Voltage drop is therefore not just an efficiency concern — it affects equipment performance.

### IEC Limits

| Supply Type | Lighting | Other Loads |
|-------------|--------:|-----------:|
| Public LV supply | 3 % | 5 % |
| Private LV supply | 6 % | 8 % |

These percentages are measured from the origin of the installation to the load under normal operating conditions. They do not apply during motor starting or other temporary events.

Lighting receives a tighter limit because humans notice voltage reduction visually. A 3 % drop on a 230 V circuit (6.9 V) can produce visibly dimmer lamps, particularly with older lighting technologies.

Power circuits allow 5 % because most resistive loads (water heaters, ovens, toasters) are insensitive. The appliance simply produces slightly less power.

### Why 8 % Is Not Recommended for Motors

If a private installation allows 8 % steady-state drop, a 400 V motor sees 368 V during normal operation. At startup, motors draw 5–7× rated current. Since voltage drop is proportional to current, the starting drop becomes approximately 48 %, leaving only about 208 V at the motor terminals. The motor may not produce enough starting torque, remain stalled, and draw high current until the overload protection trips. The guide recommends staying well below the maximum 8 % where motor loads are involved.

### Voltage Drop Calculation

Voltage drop approximation for three-phase:

```
ΔU = √3 × IB × (R cos φ + X sin φ) × L
```

For single-phase:

```
ΔU = 2 × IB × (R cos φ + X sin φ) × L
```

Where R and X are the cable resistance and reactance per unit length, and L is the cable length.

### Worked Example

An 8 kW oven on a 230 V supply:

- IB = 35 A
- Cable length = 60 m
- 6 mm² copper, PVC

Calculated voltage drop: 15 V.

```
Percentage = 15 / 230 × 100 ≈ 6.5 %
```

Power circuit limit = 5 %. The cable fails the voltage drop check despite being thermally adequate (Iz = 47 A > 35 A).

Solution: increase to 10 mm². The larger conductor has lower resistance, reducing the voltage drop to within the limit.

### Distance as the Limiting Factor

| Distance | Likely limiting factor |
|--------:|------------------------|
| 5 m | Ampacity |
| 20 m | Usually ampacity |
| 80 m | Often voltage drop |
| 200 m | Almost certainly voltage drop |

Long cable runs can force a larger conductor even though the current is modest. This explains why a house might have a 10 mm² cable feeding only a 30 A load — the driver is distance, not current.

## Step 7 — Check Short-Circuit Withstand (Adiabatic)

Verify that the cable can survive the worst-case fault until the protective device clears it (see [[Notes/EEE/LV/cable-sizing-adiabatic]]):

```
I²t ≤ k²S²
```

A cable may carry 30 A continuously and have acceptable voltage drop but still fail a 5 kA fault lasting 0.8 s. Remedies:

- Increase the cable cross-section S
- Choose a faster protective device (lower t)
- Use a current-limiting device

Correctly sized: the cable passes all four checks. Cable sizing is iterative — a cable that satisfies ampacity may fail voltage drop, requiring the next larger size.

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
- Schneider Electric. *Maximum voltage drop limit.* [[source]](https://www.electrical-installation.org/enwiki/Maximum_voltage_drop_limit)
- Schneider Electric. *Quality of supply voltage.* [[source]](https://www.electrical-installation.org/enwiki/Quality_of_supply_voltage)
- BS 7671. *Requirements for Electrical Installations (IET Wiring Regulations).* Appendix 4.
