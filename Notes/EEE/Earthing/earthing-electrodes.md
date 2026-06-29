---
tags: [eee, earthing, electrodes, soil-resistivity, measurement, fall-of-potential]
aliases: ["Earth Electrode", "Ground Rod", "Soil Resistivity", "Fall of Potential Method", "Earth Resistance Measurement", "Wenner Method"]
parent: "[[Notes/EEE/Earthing/earthing-fundamentals]]"
created: 2026-06-27
status: complete
---

# Earth Electrodes and Measurement

See [[Notes/EEE/Earthing/earthing-electrode-installation]] for practical installation guidance and measurement procedures.

## What an Earth Electrode Does

The earth electrode is the physical interface between the electrical system and the general mass of earth. It provides:

- A low-impedance path for fault current to return to the source via the soil (TT systems and the electrode side of TN systems)
- A stable voltage reference for the entire system
- A dissipation path for lightning and surge currents
- An equipotential reference for bonding

The quality of an earth electrode is measured by its **resistance to earth** — the lower, the better.

## Types of Earth Electrodes

### Vertical Rod

A copper-clad steel rod driven into the ground. The most common type for new installations.

Typical dimensions: 12-20 mm diameter, 1.2-3 m length (driven or augered to 3-10 m). Multiple rods can be paralleled at spacing ≥ rod length to reduce resistance.

Resistance approximation for a single rod in uniform soil:

```
R = (ρ / (2 × π × L)) × ln(4 × L / d)
```

Where ρ = soil resistivity (Ω·m), L = rod length (m), d = rod diameter (m).

For a 2.4 m rod in 100 Ω·m soil: R ≈ 35 Ω. Adding a second rod 5 m away in parallel: R ≈ 20 Ω.

### Horizontal Strip or Conductor

A buried horizontal conductor, typically copper strip (25 × 3 mm) or bare copper cable (35-70 mm²), buried 0.5-1 m deep. Used where rock prevents rod driving or where low resistance with large surface area is needed.

### Plate Electrode

A copper or steel plate (typically 0.5-1 m²) buried vertically in the ground at 1.5 m depth. Older design — largely replaced by rods and strips because plates require significant excavation and achieve limited benefit for the earth volume disturbed.

### Ring Earth Electrode

A buried ring conductor encircling the building or substation. Common for lightning protection and substations. The ring surrounds the structure, ensuring all equipment within the ring is at approximately the same potential during a fault.

### Foundation Earth Electrode

Bare conductor embedded in the concrete foundation of a building. The concrete provides a low-resistivity environment (concrete retains moisture and has lower resistivity than most soils). The large surface area of the foundation achieves low resistance with minimal additional cost.

### Structural Steelwork

In steel-framed buildings, the steel columns and beams buried in the foundation concrete can serve as the earth electrode. The foundation concrete provides the contact to the soil. This is the default electrode in modern steel-framed commercial construction — no separate electrode is required if the foundation connection meets the resistance target.

## Soil Resistivity

Soil resistivity is the single most important factor determining earth electrode resistance. It is measured in ohm-meters (Ω·m) — the resistance between opposite faces of a 1 m cube of soil.

### Typical Values

| Soil Type | Resistivity (Ω·m) |
|-----------|-------------------|
| Boggy / swamp / marsh | 10-50 |
| Clay (moist) | 20-100 |
| Loam / topsoil | 50-200 |
| Sand (moist) | 200-500 |
| Sand (dry) | 500-2000 |
| Gravel (dry) | 1000-5000 |
| Rock (weathered) | 500-2000 |
| Rock (solid granite) | 5000-50000 |
| Concrete | 50-300 |

### Factors Affecting Resistivity

**Moisture content.** A dry soil can be 1000× more resistive than the same soil when wet. Seasonal variation of 5× is common. Electrode design should be based on dry-season measurements.

**Temperature.** Frozen soil has significantly higher resistivity than the same soil above freezing. In permafrost regions, electrodes must be buried below the frost line.

**Salt content.** Dissolved electrolytes reduce resistivity. Adding salt around an electrode temporarily reduces resistance, but the effect washes out over time. Not a permanent solution.

**Grain size and compaction.** Finer, well-compacted soils have lower resistivity than coarse, loose soils.

### Measuring Soil Resistivity — Wenner Four-Probe Method

Four probes are driven into the ground in a straight line at equal spacing a, to a depth b (where b ≤ a/20). A current I is passed between the outer probes, and the voltage V is measured between the inner probes. The apparent resistivity is:

```
ρ = 2 × π × a × R (for a >> b)
```

Where R = V/I.

By varying the spacing a, resistivity at different depths is obtained — a = 2 m probes ≈ 2 m depth of investigation. Increasing a gives deeper resistivity data, which is used to design deep rod electrodes.

A minimum of three measurements at different spacings should be taken to profile the soil vertically.

## Measuring Earth Electrode Resistance — Fall of Potential Method

The fall of potential method is the standard technique for measuring the resistance of an installed earth electrode.

### Setup

```
         C1/P1        P2           C2
Electrode ●────────────●────────────●
                               D
           ←—— X = 0.62·D ——→
```

Three terminals:
- **C1/P1 (jumped):** Connected to the electrode under test
- **P2:** Connected to a potential probe (auxiliary voltage probe)
- **C2:** Connected to a current probe (auxiliary current electrode)

A test current I is injected between the electrode and the current probe (C2). The voltage drop between the electrode and the potential probe (P2) is measured at various distances X.

### The 62% Rule

For a small electrode (single rod or small grid) in uniform soil and with sufficient probe distance D, the measured resistance curve has a flat region. The resistance measured when the potential probe is at approximately 62% of the distance D to the current probe equals the true electrode resistance:

```
X ≈ 0.62 × D
```

This is the standard position for a single reading. D should be at least 5 times the maximum dimension of the electrode (for a 3 m rod, D ≥ 15 m; the standard often recommends D ≥ 40 m for distribution substations).

### Practical Procedure

1. Place the current probe (C2) at distance D from the electrode — at least 10× the electrode length for a rod, or 10× the diagonal for a grid
2. Place the potential probe (P2) in line between the electrode and C2
3. Measure resistance at X = 0.2D, 0.3D, 0.4D, 0.5D, 0.62D, 0.7D, 0.8D
4. Plot resistance vs. distance
5. If the curve has a flat section, the true resistance is the value at the flat section
6. If no flat section appears (curve rises or falls continuously), increase D and repeat
7. If the curve has a rising or falling trend without a plateau, the soil is non-uniform or D is insufficient

### Measurement Pitfalls

- Underground metallic pipes, cables, or structural steel near the probes distort the measurement — position the probes away from buried services
- The current probe must have a resistance low enough to pass test current — a poor probe connection limits the test current and reduces accuracy
- Multiple electrodes in parallel (as in a building's interconnected earthing system) require special procedures because the individual electrode cannot be isolated
- The attached rod technique (ART) allows measurement without disconnecting the electrode from the system, using a clamp-on CT to isolate the test current from the installation's PE conductor

## Target Resistance Values

| Application | Target Resistance | Standard |
|-------------|------------------|----------|
| LV consumer (TT system) | ≤ 200 Ω (for 30 mA RCD) | IEC 60364 |
| LV consumer (TT system, main switch with 300 mA RCD) | ≤ 167 Ω | IEC 60364 |
| LV substation | ≤ 10 Ω (typical) | Local utility regulations |
| MV substation | ≤ 1-10 Ω | IEEE 80, EN 50522 |
| High-voltage substation | ≤ 1 Ω | IEEE 80 |
| Lightning protection (telecom tower) | ≤ 5-10 Ω | IEC 62305 |
| Lightning protection (building) | ≤ 10 Ω | IEC 62305 |

## References

- IEC 60364-5-54. *Low-voltage electrical installations — Earthing arrangements and protective conductors.*
- IEC 62305-3. *Protection against lightning — Physical damage and life hazard.*
- IEEE Std 81-2012. *IEEE Guide for Measuring Earth Resistivity, Ground Impedance, and Earth Surface Potentials of a Grounding System.*
- IEEE Std 80-2013. *IEEE Guide for Safety in AC Substation Grounding.*
- EN 50522. *Earthing of power installations exceeding 1 kV a.c.*
- BS 7430. *Code of practice for earthing.*
- Megger. *Getting Down to Earth: A practical guide to earth resistance testing.*
