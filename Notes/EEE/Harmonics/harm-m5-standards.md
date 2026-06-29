---
tags: [harmonics, standards, ieee-519, iec-61000, compliance]
aliases: ["Harmonic Standards", "IEEE 519", "IEC 61000-3-2", "EN 50160"]
parent: "[[Harmonics -- Map of Content]]"
created: 2026-06-27
status: complete
---

# M5: Standards & Compliance Limits

## Overview

Harmonic standards fall into two categories:

| Category | Scope | Examples |
|----------|-------|----------|
| Equipment-level | Limits what a single device can emit | IEC 61000-3-2, IEC 61000-3-12 |
| Installation-level | Limits at the point of common coupling (PCC) with the utility | IEEE 519, EN 50160, IEC 61000-2-4 |

An installation can pass PCC limits while individual devices meet equipment limits — or fail both. The two tiers are independent but complementary.

## IEEE 519-2022

The primary North American standard for harmonic control at the PCC. Originally a *recommended practice*, IEEE 519-2022 is now a *standard*.

### Voltage Distortion Limits (PCC)

| Bus Voltage $V_{PCC}$ | Individual Harmonic (%) | THD_V (%) |
|----------------------|----------------------|-----------|
| $\leq$ 1.0 kV | 5.0 | 8.0 |
| 1 kV < V $\leq$ 69 kV | 3.0 | 5.0 |
| 69 kV < V $\leq$ 161 kV | 1.5 | 2.5 |
| > 161 kV | 1.0 | 1.5 |

Lower voltage systems tolerate higher THD because the same absolute voltage distortion is a smaller percentage.

### Current Distortion Limits

Current limits depend on the **short-circuit ratio** $I_{SC} / I_L$:

- $I_{SC}$ = maximum short-circuit current at the PCC
- $I_L$ = maximum demand load current (fundamental) at the PCC

A strong (stiff) PCC with $I_{SC} / I_L > 100$ can inject more harmonic current (as a percentage of load) than a weak PCC with ratio < 20.

**TDD limits for $V_{PCC} \leq 69$ kV:**

| $I_{SC} / I_L$ | h < 11 | 11 $\leq$ h < 17 | 17 $\leq$ h < 23 | 23 $\leq$ h < 35 | 35 $\leq$ h $\leq$ 50 | TDD |
|----------------|--------|-----------------|-----------------|-----------------|---------------------|-----|
| < 20 | 4.0 | 2.0 | 1.5 | 0.6 | 0.3 | 5.0 |
| 20-50 | 7.0 | 3.5 | 2.5 | 1.0 | 0.5 | 8.0 |
| 50-100 | 10.0 | 4.5 | 4.0 | 1.5 | 0.7 | 12.0 |
| 100-1000 | 12.0 | 5.5 | 5.0 | 2.0 | 1.0 | 15.0 |
| > 1000 | 15.0 | 7.0 | 6.0 | 2.5 | 1.4 | 20.0 |

### Key Changes in IEEE 519-2022

- TDD calculation changed from $I_{harm} / I_{fund}$ to $I_{harm} / I_{total}$ where $I_{total} = \sqrt{I_{fund}^2 + I_{harm}^2}$. This slightly reduces the TDD number.
- Even harmonic limits now use the same percentages as odd harmonics — except for 2nd, 4th, and 6th, which are limited to 50% of the odd limits.
- Clarified that backup generator operation does not require 5% TDD compliance (previously misinterpreted).
- Now a standard (mandatory) rather than a recommended practice.

### Where to Apply

IEEE 519 applies at the **PCC** — the point where the utility connects to the customer. The PCC is not always the same as the transformer secondary. For a facility with multiple buildings, the PCC might be at the main service entrance.

## IEC 61000 Series

### IEC 61000-3-2 (Equipment < 16 A)

Limits harmonic current emissions for equipment drawing less than 16 A per phase.

Four classes of equipment with different limits:

| Class | Equipment | Key Requirements |
|-------|-----------|-----------------|
| A | Balanced 3-phase, all other not Class B/C/D | Fixed harmonic current limits per order |
| B | Portable tools | 1.5x Class A limits |
| C | Lighting | PF > 0.9, 3rd harmonic < 0.3 x fundamental |
| D | Equipment with "special waveform" (power < 600 W) | Limits based on input power (mA/W) |

**Trap:** Class D applies only to equipment that draws the characteristic "input current having a special waveform" and has active input power $\leq$ 600 W. Equipment > 600 W defaults to Class A even if the waveform is special.

### IEC 61000-3-12 (Equipment 16-75 A)

For larger equipment. THD < 48%, with individual harmonic limits per order.

### IEC 61000-2-4 (Compatibility Levels in Industrial Plants)

Defines three compatibility classes based on the network environment:

| Class | Application | THD_V Limit |
|-------|-------------|-------------|
| 1 | Protected supplies, sensitive equipment | Lower than Class 2 |
| 2 | General industrial and utility (PCC) | 8% |
| 2a/2b/2L | 2024 revision sub-classes of Class 2 | Specific per sub-class |
| 3 | Industrial with heavy nonlinear loads | 10% |

The 2024 revision (3rd edition) introduced Classes 2a, 2b, and 2L to replace the former broad Class 2, and added compatibility levels for the 2-150 kHz range (supraharmonics).

## EN 50160 (Europe)

Voltage characteristics of electricity supplied by public distribution networks:

| Parameter | Limit |
|-----------|-------|
| THD_V (up to 40th harmonic, 95% of week) | $\leq$ 8% |
| Individual harmonic voltage (odd, < 95% of week) | Per order table (e.g., 3rd: 5%, 5th: 6%, 7th: 5%) |
| Individual harmonic voltage (even, < 95% of week) | 25-50% of adjacent odd limits |

Applies at the customer's supply point in public LV and MV networks. Excludes industrial networks with dedicated transformers.

## Comparison: IEEE 519 vs IEC Approach

| Aspect | IEEE 519 | IEC 61000 / EN 50160 |
|--------|----------|---------------------|
| Scope | PCC (utility-customer interface) | Equipment emissions + network compatibility |
| Metric | TDD (current), THD_V (voltage) | THD_V, individual harmonics, PWHD |
| Philosophy | Utility sets limit based on available fault current | Equipment must limit emissions, network must tolerate |
| Enforcement | Contractual (utility specifies in service agreement) | Regulatory (CE marking, product compliance) |
| Key strength | Flexible — adapts to system strength | Comprehensive — covers device to network |

## Designing for Compliance

- **New installations:** Perform a harmonic study during design. Identify the dominant harmonics at the PCC and size mitigation accordingly.
- **Expansions:** Adding VFDs or PV inverters to an existing system requires re-evaluation. The $I_{SC} / I_L$ ratio changes as load grows.
- **Retrofits:** Replacing linear loads with nonlinear equivalents (e.g., LED retrofit) can push a formerly compliant installation over the limit.
- **PFC capacitors:** Always detune (7% or 14% reactor) when nonlinear loads are present. A harmonic study should verify the resonant frequency.

## References

- IEEE 519-2022. *IEEE Standard for Harmonic Control in Electric Power Systems.*
- IEC 61000-3-2:2018+A1:2020. *EMC — Limits for harmonic current emissions.*
- IEC 61000-3-12:2011. *EMC — Limits for harmonic currents produced by equipment connected to public low-voltage systems (16-75 A).*
- IEC 61000-2-4:2024. *EMC — Compatibility levels in industrial plants for low-frequency conducted disturbances.*
- EN 50160:2022. *Voltage characteristics of electricity supplied by public electricity networks.*
- ABB. *Tech Note 158: IEEE 519-2022 Review.*
- Siemens. *Whitepaper: Harmonics in Power Systems.*
