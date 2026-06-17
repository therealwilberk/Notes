---
tags: [power-electronics, grid, renewables, solar, pv, storage]
aliases: ["PE M13", "Grid Integration & Renewables"]
parent: "[[Power Electronics -- Map of Content]]"
created: 2026-06-17
status: complete
---

# M13: Grid Integration & Renewables

## PV Inverter Architectures

| Architecture | Power range | Efficiency | Isolation | Use case |
|-------------|-------------|------------|-----------|----------|
| Central inverter | 100 kW - MW | 97-98% | Transformer (or transformerless) | Utility-scale solar farms |
| String inverter | 5-100 kW | 97-98.5% | Transformerless (HF transformer in some) | Commercial rooftop |
| Microinverter | 200-500 W per panel | 95-97% | HF transformer | Residential (per-panel MPPT) |
| Power optimizer + central | 200-500 W per panel | 99% (optimizer) | No (optimizer is DC-DC) | Residential (per-panel MPPT, central inverter) |

### Central Inverter

Single large inverter for the entire array. The lowest cost per watt. Requires high-voltage DC string wiring (up to 1500 V DC). String diodes prevent reverse current. MPPT is applied to the entire array — partial shading reduces yield significantly.

### String Inverter

Each string of panels (typically 10-20) has its own MPPT. Multiple MPPT inputs allow handling of partial shading on different roof orientations. Transformerless designs (no galvanic isolation) achieve the highest efficiency but require GFDI (ground fault detector/interrupter).

**Trap**: Transformerless inverters require the PV array to be ungrounded (floating). Ground faults are detected by monitoring the current imbalance between positive and negative conductors (residual current monitoring). If the array ground fault occurs, the inverter must disconnect within IEEE 1547 / VDE 0126 timing requirements.

### Microinverter

Each panel has a dedicated inverter. MPPT per panel — maximizes energy harvesting under partial shading. AC output is directly connected to the home AC wiring. Easy expansion. Higher cost per watt.

## Maximum Power Point Tracking (MPPT)

PV cells have a single operating point where P = V × I is maximum. This point varies with irradiance and temperature.

### Perturb & Observe (P&O)

Perturb the operating voltage and observe the resulting power change. If power increases, continue in the same direction. If power decreases, reverse direction.

- Simple, widely used
- Oscillates around the MPP in steady state (step size determines the trade-off between tracking speed and oscillation amplitude)
- Can fail under rapidly changing irradiance (cloud edge effect) — the power change from the irradiance change is interpreted as a response to the perturbation

### Incremental Conductance (INC)

Compares dI/dV to -I/V. At the MPP, dI/dV = -I/V. Determines whether the operating point is to the left (increase V) or right (decrease V) of the MPP.

- More accurate than P&O under steady irradiance
- Does not oscillate in steady state (if the threshold is set properly)
- More complex to implement
- Better performance under rapidly changing irradiance

### Other Methods

| Method | Speed | Complexity | Sensor requirement |
|--------|-------|------------|-------------------|
| P&O | Moderate | Low | V, I |
| INC | Moderate | Moderate | V, I |
| Constant voltage (V_ref = 0.75-0.8 × V_OC) | Fast | Very low | V only (periodic V_OC measurement) |
| Constant current | Fast | Low | I only |
| Fuzzy logic | Fast | High | V, I (expert knowledge) |
| Neural network | Very fast | Very high | Irradiance, temperature, V, I (training required) |

## Grid Synchronization (PLL)

A phase-locked loop synchronizes the inverter output to the grid voltage. The standard three-phase SRF-PLL (synchronous reference frame PLL) uses a Park transform to align the d-axis with the grid voltage vector, then regulates V_q = 0.

**Key parameters**:
- Bandwidth: typically 10-50 Hz — fast enough to track grid frequency variations, slow enough to reject grid voltage harmonics and noise
- PI gains tuned for locking time and overshoot

**Trap**: PLL performance under weak grid (high grid impedance) or under distorted grid (high harmonic content) requires additional filtering. A pre-filter (notch at 2× grid frequency) is essential for single-phase PLLs because the 2nd harmonic ripple appears at the Park output. For three-phase, grid voltage imbalance creates 100 Hz ripple — use a notch filter at 100 Hz or decouple the positive and negative sequences.

## Anti-Islanding

When the grid disconnects, the inverter must detect the island condition and stop energizing the line within standard timing (typically <2 seconds per IEEE 1547).

### Passive Methods
- **OVP/UVP / OFP/UFP**: detect voltage or frequency outside nominal range. Works for large power imbalances but fails when the local load matches the inverter output (an exact power match makes voltage and frequency stay within limits).
- **Voltage phase jump detection**: detect a sudden change in the grid voltage phase angle.

### Active Methods
- **Frequency drift**: inject a small frequency error and detect the frequency drift when the grid is absent (the inverter's frequency control loop has no grid reference)
- **Impedance measurement**: inject a current perturbation and measure the resulting voltage change — grid impedance increases in an island

**Standards**: IEEE 1547-2018 (US), VDE-AR-N-4105 (Germany), AS/NZS 4777.2 (Australia). Islanding detection + voltage regulation + frequency response + power quality requirements.

## Energy Storage Systems

### Battery Storage Inverter Architectures

| Architecture | Efficiency | DC link | Typical use |
|-------------|------------|---------|-------------|
| Single-stage (battery → inverter → grid/load) | ~97% | No (battery directly to inverter) | Low-voltage battery systems |
| Dual-stage (battery → DC-DC → DC link → inverter) | ~95% | Regulated (400-800 V) | High-voltage battery or wide voltage range |
| Cascaded H-bridge | ~96% | Per-cell (fraction of total) | Utility-scale (multi-module) |

### Battery Chemistry Impact on Converter Design

| Chemistry | Cell voltage | String configuration | Converter implications |
|-----------|-------------|---------------------|------------------------|
| Lead-acid | 2.0 V nominal | N× 2 V | Wide voltage range per cell (1.75-2.4 V) |
| Li-ion (LFP) | 3.2 V nominal | 16S typical for 48 V system | Narrower range (2.5-3.65 V per cell) |
| Li-ion (NMC) | 3.6 V nominal | 14S typical for 48 V system | Higher energy density, tighter voltage range |
| Li-ion (LTO) | 2.3 V nominal | 22S for 48 V system | Very wide voltage range, high C-rate |

**Trap**: Battery systems have a wide voltage range — from fully discharged to fully charged, the voltage can swing by 30% or more. The downstream converter (or upstream, for charging) must operate efficiently across this range. A dual-stage architecture (battery DC-DC + inverter) handles this better than a single-stage design.

### BMS Communication

The power converter must communicate with the battery management system (BMS) to:
- Receive charge/discharge current limits
- Forward fault signals (over-temperature, cell imbalance, over-voltage, under-voltage)
- Coordinate the charging profile (CC-CV sequence)

Protocol: CAN bus (most common for automotive and high-power), SMBus / I²C (lower power), RS-485 / Modbus (industrial).

## Microgrids

A microgrid is a localized group of generation, storage, and loads that can operate grid-connected or islanded.

### Grid-Connected Mode
The microgrid follows the grid voltage and frequency. Power converters operate in grid-following mode (current source — inject P and Q as commanded).

### Islanded (Off-Grid) Mode
The microgrid must establish its own voltage and frequency reference. The primary power converter (typically the battery inverter) operates in grid-forming mode (voltage source — regulate V and f).

**Grid-forming vs grid-following**:

| Characteristic | Grid-following | Grid-forming |
|---------------|----------------|--------------|
| Control target | Current injected | Voltage and frequency |
| Grid reference | Required (PLL) | Self-generated |
| Black-start capable | No | Yes |
| Synchronization | PLL to grid | Droop control among peers |
| Dominant | Utility grid-tie | Islanded microgrid |

## Standards for Grid-Tie

| Standard | Scope | Key requirements |
|----------|-------|-----------------|
| IEEE 1547-2018 | Interconnection of DERs | Voltage/freq ride-through, anti-islanding, power quality, reactive power support |
| IEC 61727 | PV grid connection | Harmonic limits, power factor, DC injection limit |
| VDE-AR-N 4105 | Germany (low-voltage DER) | 1:1 phase balance, 50% P 1-min ramp, frequency-dependent power reduction |
| IEC 62109 | PV inverter safety | Clearance/creepage, ground fault protection, arc fault detection |
| UL 1741 | US inverter safety | Anti-islanding, DC injection, ground fault (SA) |

## References
- Blaabjerg, F. et al. "Power Electronics in Renewable Energy Systems." *IEEE Trans. Power Elec.*, 2006.
- Teodorescu, R. et al. *Grid Converters for Photovoltaic and Wind Power Systems*. Wiley, 2011.
- Rashid, M.H. *Power Electronics Handbook*. 4th ed. Ch 26-28 (Renewable Energy).
- IEEE 1547-2018: Standard for Interconnection and Interoperability of DERs.
- VDE-AR-N 4105: Generators connected to the LV distribution network — Technical requirements.
- Mohan, N. et al. *Power Electronics*. 3rd ed. Ch 28 (Utility Applications).
