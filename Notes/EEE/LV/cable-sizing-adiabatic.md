---
tags: [eee, lv, cables, adiabatic, short-circuit, protection]
aliases: ["Adiabatic Equation", "Short-Circuit Withstand", "I²t = k²S²", "Cable Thermal Withstand", "k Factor"]
parent: "[[Notes/EEE/LV/lv-switchgear]]"
created: 2026-06-29
status: complete
---

# Cable Sizing — Adiabatic Equation (Short-Circuit Withstand)

Ampacity sizes the cable for normal operation. The adiabatic equation checks whether the cable survives a fault until the protective device clears it.

## The Equation

```
I²t = k²S²
```

- I = prospective short-circuit current (A rms)
- t = disconnection time (s)
- S = conductor cross-sectional area (mm²)
- k = constant that depends on conductor material, insulation type, and initial/final temperature limits

This is not a cable sizing equation in the normal sense. It answers one question: if a short circuit occurs, can the cable withstand the thermal energy until the breaker or fuse clears the fault?

## Why Resistance Does Not Appear

Ohmic heating follows Q = I²Rt. Resistance appears to be missing from the adiabatic equation because it is absorbed into k.

The derivation:

1. Heat produced: Q = I²Rt
2. Heat absorbed: Q = mcΔT
3. Substitute R = ρl/S and m = ρ_mSl

One S is in the denominator (resistance) and another S is in the numerator (mass). After simplification, S depends only on I²t and k. The constant k contains:

- Conductor resistivity (ρ)
- Specific heat capacity (c)
- Density (ρ_m)
- Initial and final temperature limits of the insulation
- Temperature coefficient of resistance (in the IEC derivation)

## Why Cable Length Does Not Appear

A longer cable has more resistance (more heat generated) but also more copper mass (more material to absorb that heat). Both increase proportionally with length and cancel during the derivation. The equation depends only on cross-sectional area S, not length.

## The k Factor

The k factor encodes the thermal limits of the cable. Higher k means the cable can withstand more fault energy for a given cross-section.

| Conductor | Insulation | Initial Temp (°C) | Final Temp (°C) | k (A·s½/mm²) |
|-----------|-----------|------------------|----------------|--------------|
| Copper | PVC (70 °C) | 70 | 160 | 115 |
| Copper | PVC (90 °C) | 90 | 160 | 100 |
| Copper | XLPE / EPR | 90 | 250 | 143 |
| Aluminium | PVC (70 °C) | 70 | 160 | 76 |
| Aluminium | XLPE / EPR | 90 | 250 | 94 |
| Copper | Bare (visible) | 30 | 200 | 159 |
| Steel | PVC (70 °C) | 70 | 160 | 51 |

XLPE tolerates a higher final temperature than PVC (250 °C vs 160 °C), so its k is larger. The same cable with XLPE insulation can survive more fault energy than with PVC.

## The Conductor and Insulation Have Different Jobs

The conductor (copper or aluminium) determines how much heat is generated and how much thermal mass exists to absorb it. The insulation determines the maximum temperature the assembly can reach before damage occurs.

A larger k does not mean the copper is different — it means the insulation allows a higher temperature before failing.

## Thermal Limit Curves

The relationship between current and allowable time follows an inverse-square curve:

```
Fault Current (kA)
 ^
 |\
 | \
 |  \     adiabatic limit
 |   \
 |    \
 |     \
 |      \
 |       \
 +--------------------> Time (s)
```

Very high currents are survivable for only milliseconds. Lower currents can be tolerated for seconds. The curve approaches the continuous rating Iz asymptotically, where the cable can operate indefinitely.

### Effect of Ambient Temperature

In a hotter environment, the conductor starts closer to its insulation limit, reducing the available temperature rise before damage:

- Cool room (20 °C ambient, 70 °C insulation limit): available rise = 105 °C at normal operation
- Hot room (45 °C ambient, 70 °C insulation limit): available rise = 80 °C

Higher ambient means less thermal headroom for faults. The cable must carry less continuous current or survive a fault for a shorter time.

## Usage in the Sizing Workflow

The adiabatic check is the final verification step after ampacity and voltage drop:

If I²t > k²S², the options are:

- Increase the cable cross-section S
- Select a faster protective device (lower t)
- Use a current-limiting device that reduces the let-through energy

## References

- IEC 60364-4-43. *Protection against overcurrent.*
- IEC 60364-5-52. *Selection and erection of electrical equipment — Wiring systems.*
- Schneider Electric. *Electrical Installation Guide.* Chapter G: Sizing and protection of conductors. [[source]](https://www.electrical-installation.org/enwiki/Verification_of_the_withstand_capabilities_of_cables_under_short-circuit_conditions)
- myCableEngineering. *The Adiabatic Equation.* [[source]](https://mycableengineering.com/knowledge-base/the-adiabatic-equation)
- BS 7671, Appendix 4. *Current-carrying capacity and voltage drop for cables and flexible cords.*
