---
tags: [eee, earthing, electrodes, installation, measurement, fall-of-potential, soil-resistivity]
aliases: ["Earth Electrode Installation", "Earth Resistance Measurement", "Three-Electrode Test", "Buried Ring Electrode", "Earth Rod Installation"]
parent: "[[Notes/EEE/Earthing/earthing-electrodes]]"
created: 2026-06-29
status: complete
---

# Earth Electrode Installation and Measurement

The earth electrode is not the protection. It is the interface between the installation and the earth. The entire design revolves around one goal: get the earth resistance as low as reasonably possible.

## What is Earth Resistance?

Water pushed into the ground encounters different resistance depending on the soil. Wet sand allows water through easily; concrete blocks it. Current behaves similarly — some soils conduct electricity well, some do not. The earth electrode attempts to make a good electrical contact with the soil.

Earth resistance is approximately determined by:

- Soil resistivity (ρ)
- Electrode size
- Installation method

## Soil Resistivity (ρ)

Soil resistivity answers: how difficult is it for current to flow through this soil? It is the single most important factor determining earth electrode resistance. Measured in ohm-metres (Ω·m).

### Typical Values

| Soil | Approximate Resistivity |
|------|-----------------------:|
| Sea water | Very Low |
| Wet clay | Low |
| Moist soil | Moderate |
| Dry sand | High |
| Rock | Very High |

Two identical earth rods can measure 2 Ω at one site and 150 Ω at another purely because of soil resistivity differences.

## Why Bury Conductors?

For a buried ring, the guide gives the approximation:

```
R ≈ 2ρ / L
```

Resistance is inversely proportional to length. A longer conductor means more soil contact, which means lower resistance — analogous to rubbing a hand against a wall: one fingertip contacts a tiny area, the whole hand contacts a much larger area. The conductor does the same thing.

## Method 1 — Buried Ring (Best for New Buildings)

In a new factory before concrete is poured, bare copper is placed around the foundation perimeter:

```
Top View

+=======================+
||                     ||
||                     ||
||                     ||
+=======================+
```

### Why It Is Effective

**Huge contact area.** Instead of a single rod, the conductor encircles the entire building, providing far more soil contact.

**Moist soil.** Foundation excavations tend to remain relatively moist. Moisture lowers resistivity, which lowers earth resistance.

**Fault current spreads across the perimeter.** Instead of concentrating at one small rod, current distributes around the whole building perimeter, giving much better potential distribution.

### Why Not to Place It in the Concrete

The conductor must contact soil, not concrete. Concrete generally has a higher resistivity than moist soil and isolates the conductor from direct soil contact. The conductor should be buried in the earth outside the foundation.

## Method 2 — Earth Rod

The most common type for existing buildings. A copper-clad steel rod is driven into the ground:

```
Ground
──────────────
      |
      |
      |
      |
```

Simple, cheap, excellent for retrofitting.

### Why Copper-Clad Steel

Solid copper is an excellent conductor but soft and expensive. Steel is strong and cheap but corrodes poorly. Copper-clad steel combines a steel core for strength with a copper outer layer for conductivity and corrosion resistance.

### Why Deeper Rods

Soil moisture becomes more stable with depth:

```
0.5 m  — Dry
2 m    — Moist
5 m    — Very Moist
```

Stable moisture content gives stable, lower resistance.

### Multiple Rods and Spacing

If one rod gives 20 Ω, two rods in parallel give approximately 10 Ω if spaced sufficiently far apart.

Current does not leave the rod as a straight line — it spreads outward in a zone of influence. If a second rod is placed too close, the two current fields overlap and both rods compete for the same volume of soil. The second rod contributes much less than expected.

Rods should be spaced approximately 2–4 rod lengths apart to ensure each one uses a distinct volume of earth.

## Method 3 — Plate Electrode

A metal plate (copper or steel, typically 0.5–1 m²) buried vertically in the ground. More surface area gives lower resistance, but rods are generally easier to install, so plate electrodes are used less frequently today.

## Measuring Earth Resistance

Once the electrode is installed, the only way to know it is adequate is to measure it.

### Why Disconnect First

The removable link between the MET and the earthing conductor (see [[Notes/EEE/Earthing/earthing-fundamentals]]) must be opened before testing. Without disconnection, the tester sees building steel, water pipes, neighbouring electrodes, and cable armour in parallel with the electrode under test — the measured resistance is artificially low and meaningless.

### The Three-Electrode (Fall of Potential) Test

Three points:

- **X** = electrode under test
- **P** = potential probe (auxiliary voltage probe)
- **C** = current probe (auxiliary current electrode)

Arranged in a straight line:

```
X-----------P----------------C
```

The tester injects AC current between X and C. At the same time, it measures the voltage between X and P. Resistance is calculated internally via Ohm's law (R = V/I).

### Why AC Instead of DC

The soil already contains galvanic potentials, corrosion currents, and stray DC currents that would corrupt a DC measurement. Earth testers generate their own small AC signal, typically around 85–135 Hz, deliberately different from the 50 Hz power frequency and its harmonics, so the instrument can distinguish its own test current from everything else.

### Why Move the Middle Probe

If the potential probe P sits inside the zone of influence of either X or C, the voltage measurement is distorted. The electrician moves P to several positions:

```
X-----P1------C
X------P2-----C
X-------P3----C
```

If all readings are nearly the same, the measurement is considered reliable. See [[Notes/EEE/Earthing/earthing-electrodes]] for the 62% rule and detailed procedure.

## Does Lower Resistance Always Mean Better?

Generally yes, but only to a point. 100 Ω is poor. 20 Ω is much better. 5 Ω is excellent for many applications. 0.5 Ω is outstanding.

There is no single magic number. The acceptable earth resistance depends on the earthing system and the protection method.

## Connecting to Earthing Systems

### TT

```
Transformer
    │
 Earth Rod A

          Soil

Earth Rod B
    │
Building
```

The soil is part of the fault loop. Earth electrode quality is crucial. See [[Notes/EEE/Earthing/earthing-systems]].

### TN

```
Transformer
     │
     PE
     │
Building
```

Fault current returns mainly through the PE conductor, not the soil. The earth electrode is still valuable for bonding, surges, and potential equalisation, but it is not the primary fault-current path. See [[Notes/EEE/Earthing/earthing-tn-types]].

### IT

The earth electrode mainly stabilises the system, provides a reference to earth, and assists with transient and lightning protection. The first earth fault produces very little current because the source is not solidly earthed. See [[Notes/EEE/Earthing/earthing-systems]].

## The Four Design Levers

This chapter is fundamentally about improving the electrical contact between the installation and the earth. Four main design levers are available:

1. **Choose better soil** — moist, low-resistivity soil if available at the site.
2. **Increase contact area** — rings, longer rods, plates, or strips.
3. **Reach deeper, wetter soil** — longer rods to access stable moisture layers.
4. **Use multiple well-spaced electrodes** — each one uses a different volume of earth, maximising the benefit of each additional rod.

Everything else — the formulas, installation methods, and measurement techniques — is an engineering toolkit for achieving one objective: a low-resistance, stable, and verifiable connection between the installation's earthing system and the earth itself.

## References

- Schneider Electric. *Electrical Installation Guide.* Chapter E: Earthing connections. [[source]](https://www.electrical-installation.org/enwiki/Installation_and_measurements_of_earth_electrodes)
- IEC 60364-5-54. *Low-voltage electrical installations — Earthing arrangements and protective conductors.*
- IEEE Std 81-2012. *IEEE Guide for Measuring Earth Resistivity, Ground Impedance, and Earth Surface Potentials of a Grounding System.*
- BS 7430. *Code of practice for earthing.*
