---
tags: [harmonics, effects, overheating, k-factor, power-quality]
aliases: ["Harmonic Effects", "K-Factor", "Transformer Derating"]
parent: "[[Harmonics -- Map of Content]]"
created: 2026-06-27
status: complete
---

# M4: Effects & Equipment Impact

## Thermal Effects

### Transformers

Harmonic current through a transformer causes additional losses beyond $I^2R$:

| Loss Component | Mechanism | Harmonic Sensitivity |
|----------------|-----------|---------------------|
| $I^2R$ (DC) | RMS current heats windings | Proportional to $I_{RMS}^2$ — all harmonics contribute |
| Eddy current | Induced circulating currents in core laminations | Proportional to $h^2 I_h^2$ — high-order harmonics dominate |
| Skin effect | Current crowding at conductor surface | Increases effective resistance with $\sqrt{h}$ |
| Hysteresis | Core magnetization | Increases with harmonic content |

Eddy current loss is the most destructive. A 5th harmonic at 20% of fundamental causes $0.20^2 \times 5^2 = 1.0$ times the fundamental eddy current loss — equal to the loss from the full fundamental current. A 13th harmonic at 8% causes $0.08^2 \times 13^2 = 1.08$ times — more loss than the fundamental.

The combined effect is summarized by **K-factor**:

$$
K = \sum_{h=1}^{\infty} \left(\frac{I_h}{I_1}\right)^2 h^2
$$

A purely sinusoidal load has $K = 1$. A K-13 rated transformer can handle 13 times the eddy current loss of a standard transformer. Typical values:

| Environment | Typical K-factor |
|-------------|-----------------|
| Office (computers, LED lighting) | K-4 to K-13 |
| Data center | K-13 to K-30 |
| Industrial VFD-heavy | K-4 to K-13 |
| Hospital | K-13 to K-20 |

**Trap:** Standard transformers are K-1 rated. Running K-13+ loads on a standard transformer causes rapid insulation aging. IEEE C57.110 provides derating guidelines — a standard 2500 kVA transformer on a K-30 load can only deliver ~1260 kVA before exceeding thermal limits.

### Neutral Conductors

Triplen harmonics sum in the neutral (see [[harm-m3-triplen-propagation]]). The neutral can carry 170% of phase current or more. I²R heating at that level:

$$
P_N = I_N^2 R_N = (1.7 \times I_{phase})^2 R_N = 2.89 \times P_{phase}
$$

If the neutral conductor is sized equal to the phase conductors, it dissipates nearly three times the heat. At the Norwegian data center example, neutral temperature exceeded 180°C — PVC insulation rated for 70-90°C failed within months.

### Cables and Switchgear

All current-carrying components experience additional I²R loss from harmonic current. Skin effect increases the effective resistance for higher-order harmonics, compounding the heating.

**Trap:** Standard ampacity tables assume sinusoidal current. Derating may be required for nonlinear loads, though NFPA 70 (NEC) does not provide a simple derating factor — the onus is on the designer.

## Non-Thermal Effects

### Motors

Harmonic currents in motor windings produce additional losses and MMF harmonics:

- **Negative-sequence harmonics** (5th, 11th, 17th...) produce a counter-rotating magnetic field. This opposes the fundamental torque and increases rotor heating.
- **Positive-sequence harmonics** (7th, 13th, 19th...) produce forward-rotating fields at higher speeds. These cause torque pulsations at $6 \times f_0$ (300 Hz for 50 Hz systems).
- Total motor losses increase by 10-20% under 5% voltage THD.

### Capacitor Banks

Capacitors have low impedance at high frequencies. Harmonic voltage across a capacitor causes excessive current:

$$
I_{C,h} = V_h \times 2\pi f_0 h C
$$

A 5th harmonic at 5% voltage causes $0.05 \times 5 = 0.25$ (25%) additional capacitor current. Combined with other harmonics, the capacitor can exceed its rated current.

**Catastrophic risk:** Near parallel resonance, harmonic voltage can be 5-10x normal. Capacitor current can double or triple, causing dielectric failure, rupture, or explosion. This is why PFC banks must be detuned (with series reactors) when nonlinear loads are present.

### Protection Devices

- **MCBs and fuses** respond to RMS current. Additional heating from harmonics causes nuisance tripping at lower fundamental load levels.
- **RCCBs** can malfunction in the presence of high-frequency leakage currents from VFDs. The leakage current waveform includes switching-frequency components that the RCCB may not detect correctly.
- **Relays and contactors** may chatter if line-to-neutral voltage is distorted (flat-topped waveform caused by 3rd harmonic voltage drop in neutral).

### Metering

- **Average-sensing meters** (old analog meters) under-register when harmonics are present. A heavily distorted load draws more real power than the meter shows.
- **True RMS meters** capture harmonic energy correctly.
- **Revenue metering** at the PCC must be true RMS for installations with significant nonlinear loads.

### Generators

Generators have higher source impedance than utility feeds. The same harmonic current from a VFD produces more voltage distortion on a generator-supply bus.

**Effects:**
- Voltage regulator instability (AVR samples distorted waveform)
- Additional rotor heating from harmonic stator currents
- Reduced available real power — generator must be oversized or the load derated

**Trap:** A generator powering VFDs should have a dedicated harmonic study. IEEE 519-2022 states that the TDD limits need not be as strict for backup genset operation as for utility interconnection.

### Communications Interference

Harmonic currents in power conductors can inductively couple into adjacent communication cables. The 3rd harmonic (150 Hz) and its multiples fall within the voice frequency range and can cause audible hum in telephone lines.

## Identifying Harmonic Problems in the Field

| Symptom | Likely Cause |
|---------|-------------|
| Transformer hot at <80% load | High K-factor load — measure harmonic spectrum |
| Neutral conductor hot, phase conductors cool | Triplen harmonics — measure neutral current |
| Capacitor bank failed (ruptured, bulged) | Harmonic resonance — check tuning and ambient harmonics |
| Motors overheating with clean filter/ambient | Voltage THD >5% — measure PCC |
| Generator voltage unstable with VFD load | High source impedance + harmonics — add filtering |
| RCCB trips intermittently | VFD leakage current — check switching frequency content |
| Analog meter reads low, digital meter reads higher | Harmonics present — end-user pays less than actual usage |
| UPS input THD high | Downstream SMPS loads — check neutral current |

## References

- IEEE C57.110-2018. *Recommended Practice for Establishing Transformer Capability When Supplying Nonsinusoidal Load Currents.*
- IEEE 519-2022. *Harmonic Control in Electric Power Systems.*
- Copper Development Association. *Two Modern Power Quality Issues: Harmonics & Grounding.*
- ECalPro. *Harmonic Analysis & Neutral Conductor Sizing for a 2 MW Data Center.*
- EC&M. *The Case of Overheated Transformers and Neutral Conductors.*
