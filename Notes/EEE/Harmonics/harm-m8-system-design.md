---
tags: [harmonics, system-design, transformers, k-rated, mitigation]
aliases: ["K-Rated Transformer", "Harmonic Mitigating Transformer", "HMT", "Zigzag Transformer"]
parent: "[[Harmonics -- Map of Content]]"
created: 2026-06-27
status: complete
---

# M8: System Design & Transformer Solutions

## K-Rated Transformers

A K-rated transformer is designed to withstand the additional eddy-current heating caused by harmonic currents. The K-factor rating indicates the transformer's capability relative to a standard (K-1) unit.

### K-Factor Calculation

$$
K = \sum_{h=1}^{\infty} \left(\frac{I_h}{I_1}\right)^2 h^2
$$

| K Rating | Eddy Current Capability | Typical Application |
|----------|------------------------|---------------------|
| K-4 | 4x standard | Office lighting, general office loads |
| K-13 | 13x standard | Computer rooms, moderate data centers |
| K-20 | 20x standard | Data centers, hospitals |
| K-30 | 30x standard | High-density data centers, UPS-heavy loads |
| K-40 | 40x standard | Extreme nonlinear loads |

### Construction Differences from Standard Transformers

- **Extended copper** in windings — thicker conductors reduce DC resistance to offset additional I²R from RMS current.
- **Reduced core flux density** — core is oversized to reduce core losses, providing headroom for harmonic-induced flux.
- **Double-sized neutral terminals** — accommodates the larger neutral conductor required for triplen harmonic return.
- **Electrostatic shield** between primary and secondary — reduces high-frequency coupling.
- **Lower eddy current design** — thinner laminations, transposed conductors, or interleaved windings.

### Derating Instead of K-Rating

An alternative to specifying a K-rated transformer is to derate a standard transformer. Per IEEE C57.110, the derating factor depends on the harmonic spectrum.

```
Derating Factor = (1.414 x I_RMS) / I_peak
```

For typical computer loads, derating factors range from 0.5 to 0.7. A 1000 kVA standard transformer must be loaded to only 500-700 kVA.

**Trap:** Derating is acceptable for existing installations but is not recommended for new designs. The same kVA capacity costs more as a derated standard transformer than as a properly rated K-factor unit. The standard transformer also lacks the oversized neutral and other harmonic-specific features.

## Harmonic Mitigating Transformers (HMT)

An HMT uses specialized winding configurations to cancel harmonic currents electromagnetically, rather than just surviving them.

### Phase-Shifting (Multi-Pulse)

Two or more secondary windings with a phase shift between them. The combined output from multiple 6-pulse rectifiers becomes 12-pulse, 18-pulse, or 24-pulse.

- **12-pulse:** One wye secondary + one delta secondary (30-degree shift). Cancels 5th and 7th.
- **18-pulse:** Three secondaries with 20-degree shifts. Cancels 5th, 7th, 11th, 13th.
- **24-pulse:** Four secondaries with 15-degree shifts. Cancels up to 23rd.

### Zero-Sequence Blocking (Triplen Trapping)

A delta primary winding naturally traps triplen harmonics — they circulate in the delta but do not appear in the primary line current. This is the most common "mitigation" built into standard distribution transformers.

An HMT may include additional zigzag windings or auxiliary windings to:
- Provide a low-impedance path for triplen currents at the load side, reducing neutral current.
- Prevent triplen currents from causing additional heating in the delta winding.

### Wye-Delta-Wye (Triple-Wound) Configuration

A three-winding transformer: primary delta, secondary wye (load), tertiary winding for triplen circulation. The tertiary provides a controlled low-impedance path for triplen harmonics, limiting their effect on the main windings.

## Zigzag Transformers

A zigzag transformer is a three-phase transformer with interconnected windings that present very low impedance to zero-sequence currents (and therefore triplen harmonics).

```
               ┌───┐
Load Neutral ──┤ Z ├─── Phase A
Neutral       │   ├─── Phase B
              │   ├─── Phase C
              └───┘
```

Used in shunt (parallel with the load) to:
- Divert triplen harmonics from the neutral conductor back to the phases.
- Reduce neutral current to near zero for the triplen orders.
- Provide a grounding reference for systems that need a neutral but cannot tolerate neutral current.

**Practical benefit:** A zigzag transformer installed at the load side of a delta-wye transformer can reduce neutral current by 90% for triplen harmonics. Often much cheaper than a full APF for buildings with high 3rd harmonic content (LED lighting, computers).

## System Architecture Approaches

### Segregation of Dirty and Clean Loads

Linear and nonlinear loads on separate circuits. Dirty loads (VFDs, UPS, LED lighting) are grouped and fed from dedicated transformers or panelboards. Clean loads (sensitive equipment, motors running across the line) are fed from separate, isolated circuits.

**Why it works:**
- Dirty loads share a common PCC where filtering is concentrated.
- Clean loads see low distortion because they are isolated from the harmonic current path.
- Transformer winding connections can be chosen per load type (delta-wye for dirty, wye-wye for clean).

### Oversized Neutral

For circuits feeding nonlinear loads (especially single-phase loads on a wye system):

- Size the neutral conductor at 150-200% of the phase conductor ampacity.
- Double neutral buses in panelboards.
- Use separate neutral per phase instead of a shared neutral (eliminates triplen summation).

See [[Notes/EEE/LV/LV Distribution Topologies]] for distribution topology context.

### Detuned PFC Banks

Power factor correction capacitors must include a detuning reactor when harmonic-producing loads are present.

| Reactor % | Tuned Frequency (50 Hz) | Application |
|-----------|------------------------|-------------|
| 7% | 189 Hz (3.8th harmonic) | High 3rd harmonic content (LED, SMPS) |
| 14% | 134 Hz (2.7th) | Moderate harmonics, general industrial |

The reactor shifts the resonant frequency of the capacitor + system combination below the lowest significant harmonic, preventing parallel resonance amplification.

### Isolation Transformers

A delta-wye isolation transformer between the utility supply and a nonlinear load:
- Traps triplen harmonics in the delta (upstream sees clean current).
- Provides a dedicated neutral reference for the load.
- Reduces zero-sequence harmonic propagation to the main switchboard.

## Design Checklist for New Installations

1. **Load inventory.** Categorize each load as linear or nonlinear. Estimate THD per source.
2. **K-factor estimate.** Calculate the composite K-factor for each transformer. Specify K-rated transformers accordingly.
3. **Neutral sizing.** For 208/120 V or 400/230 V wye panels with single-phase nonlinear loads, size neutral at 200% of phase.
4. **PFC detuning.** All capacitor banks serving mixed loads must have detuning reactors (7% or 14%).
5. **Transformer connection.** Prefer delta-wye for service transformers. The delta traps triplens.
6. **Dirty/clean segregation.** Separate nonlinear and sensitive loads. Consider dedicated transformers.
7. **Harmonic study.** Use power systems software (ETAP, SKM, DigSilent) to model the impedance vs frequency characteristic. Verify the absence of resonance within the harmonic spectrum up to the 50th order.
8. **Monitoring provision.** Spec permanently installed power quality meters at the PCC and at major nonlinear load groups.

## References

- IEEE C57.110-2018. *Recommended Practice for Establishing Transformer Capability When Supplying Nonsinusoidal Load Currents.*
- IEEE 519-2022. *Harmonic Control in Electric Power Systems.*
- Hammond Power Solutions. *Harmonic Mitigating Transformers (HMTs) Frequently Asked Questions.*
- Copper Development Association. *Two Modern Power Quality Issues: Harmonics & Grounding.*
- Schonek, J. *The Singularities of the Third Harmonic.* Schneider Electric Cahier Technique.
