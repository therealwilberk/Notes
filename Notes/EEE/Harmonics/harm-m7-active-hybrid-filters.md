---
tags: [harmonics, active-filters, hybrid-filters, mitigation, VFD]
aliases: ["Active Power Filters", "Hybrid Filters", "AFE", "APF"]
parent: "[[Harmonics -- Map of Content]]"
created: 2026-06-27
status: complete
---

# M7: Active & Hybrid Filters

## Active Power Filters (APF)

An APF is a power electronic converter (typically a voltage-source inverter with IGBTs) connected in shunt with the load. It measures the load current, extracts the harmonic content, and injects a compensating current that cancels the harmonics at the PCC.

```
Supply ────────── PCC ────────── Load
                     │
                   APF
```

### How It Works

1. Measure load current $i_L(t)$ via CT.
2. Extract harmonic components $i_{L,h}(t)$ — subtract the fundamental from the measured current.
3. Generate a reference current $i_{ref}(t) = -i_{L,h}(t)$.
4. PWM inverter injects $i_{ref}(t)$ into the PCC.
5. The net supply current $i_S(t) = i_L(t) + i_{ref}(t) = i_{L,1}(t)$ — only the fundamental remains.

### Key Specifications

| Parameter | Typical Range | Notes |
|-----------|---------------|-------|
| Filter rating | 50-600 A (LV), up to 5000 A (MV) | Rated by compensating current, not load current |
| Compensation bandwidth | Up to 50th harmonic | Depends on switching frequency and control loop |
| Response time | < 1 ms (one cycle or less) | Tracks changing loads cycle-by-cycle |
| Switching frequency | 10-20 kHz | IGBT-based, determines max harmonic order |
| Topology | 2-level or 3-level VSI | 3-level NPC for MV applications |

### Advantages

- Adapts to changing load — no retuning needed.
- Compensates multiple harmonic orders simultaneously.
- Can also compensate reactive power and unbalance.
- No resonance risk with system impedance (unlike passive filters).
- Physically compact relative to multiple passive filter banks.

### Disadvantages

- Higher cost per amp of compensation than passive filters (2-3x).
- Active device — requires maintenance and has finite lifespan (DC link capacitors).
- Self-consumption (2-4% of rated power).
- Cannot compensate harmonics above the controller bandwidth.
- May saturate with very high harmonic content — the APF has a maximum compensating current rating.

**Trap:** An APF with a 300 A compensating rating connected to a 1000 A load with 50% THD will saturate — the harmonic current is 500 A, but the filter can only inject 300 A. The APF must be sized for the harmonic current, not the load current.

### Sizing Rule

$$
I_{APF} = I_{load} \times THD_I
$$

For a 600 A load with 30% THD, the APF should be rated at least 180 A.

## Active Front End (AFE)

An AFE replaces the diode/thyristor rectifier of a VFD with an IGBT-based PWM rectifier. It draws sinusoidal current with THD < 5% and provides bidirectional power flow (regenerative braking).

```
Supply ──── Line Reactor ──── IGBT Rectifier ──── DC Bus ──── Inverter ──── Motor
                               (AFE)
```

**Advantages over diode rectifier + APF:**
- THD < 5% inherently — no external filter needed.
- Regenerative capability — energy returns to the grid during braking.
- DC bus voltage is regulated (boosted above peak AC).
- Power factor can be controlled (unity or leading).

**Disadvantages:**
- Higher cost than standard VFD + APF for small drives.
- Larger line reactors required.
- Higher switching losses than diode bridge.

AFE is the standard choice for VFDs above ~500 kW, for regenerative applications (cranes, elevators, test stands, centrifuges), and where THD requirements are very strict (< 5%).

## Hybrid Filters

A hybrid filter combines passive and active filtering to leverage the strengths of each:

| Aspect | Standalone Passive | Standalone Active | Hybrid |
|--------|-------------------|-------------------|--------|
| Cost | Low | High | Medium |
| Resonance risk | High | None | Low (active damps passive resonance) |
| Adaptability | Fixed tuning | Adaptive | Adaptive |
| Bandwidth | Narrow | Wide | Wide |
| Power rating | Full load | Full harmonic | Active section is < 5% of load rating |

### Shunt Hybrid Filter

A passive filter (tuned to dominant harmonics) in parallel with a smaller-rating APF. The passive filter handles the bulk low-order harmonics (5th, 7th). The APF handles residual high-order harmonics and adapts to load changes.

```
Supply ────────── PCC ────────── Load
                     │
               ┌─────┴─────┐
            Passive       APF
            (5th/7th)    (small)
```

### Series Hybrid Filter

A small series active filter (connected via coupling transformer) forces the passive filter to absorb more harmonic current. The active filter is rated only 5-10% of the load kVA. The series configuration improves the passive filter's performance and dampens system resonance.

### Hybrid Inductive-Active Filter (HIAF)

An emerging topology where a passive inductive filter near the nonlinear load (e.g., converter transformer with extended-delta windings) suppresses harmonics at the source, and a small-series VSI damps system resonance. Used in large industrial distribution networks and wind farm collector systems.

### Hybrid Filter Design Considerations

- The passive section handles steady-state dominant harmonics.
- The active section handles transient conditions, system resonance damping, and residual harmonics.
- The active section rating can be as low as 5% of the load kVA (compared to 30-50% for standalone APF).
- The active section can also damp the parallel resonance between the passive filter and system impedance — a key advantage.

## Technology Selection Guide

| Scenario | Recommended Approach |
|----------|---------------------|
| Single VFD < 100 kW, THD target 8-10% | 3-5% line reactor |
| Multiple VFDs, THD target < 8% | Passive tuned filter (5th + 7th) |
| Multiple VFDs, THD target < 5%, varying load | Shunt APF |
| Variable load, regenerative, strict THD | AFE drives |
| Large installation, cost-sensitive, stable load | Hybrid (passive + small APF) |
| Weak grid + VFDs (genset operation) | APF or AFE (resonance-resistant) |
| Arc furnace / rolling mill | C-type + APF hybrid |
| Data center with UPS + IT loads | K-rated transformers + APF at PDU level |
| Building with LED retrofits + computers | Delta-wye isolation + oversize neutral |
| Multiple reactors and active/passive options | Hybrid combination |

## References

- IEEE 519-2022. *Harmonic Control in Electric Power Systems.*
- Comsys. *Comparing Harmonics Mitigation Techniques.* IEEE.
- Transcoil. *Hybrid Power Quality Solutions using Line Reactors, Active and Passive Filters.*
- Energies 17(11), 2024. *Design and Performance Evaluation of a Hybrid Active Power Filter Controller.*
- Energies 19(3), 2026. *Advanced Universal Hybrid Power Filter Configuration for Enhanced Harmonic Mitigation.*
- IET Power Electronics, 2015. *Hybrid Inductive and Active Filtering Method for Damping Harmonic Resonance.*
