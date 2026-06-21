---
tags: [power-electronics, thermal, emc, layout, pcb]
aliases: ["PE M11", "Thermal, EMC & Layout"]
parent: "[[Power Electronics -- Map of Content]]"
created: 2026-06-17
status: complete
---

# M11: Thermal, EMC & System Integration

## Loss Calculation

### Conduction Loss

MOSFET: $P_{cond} = I_{D(rms)}^2 R_{DS(on)}$ ($R_{DS(on)}$ is temperature-dependent — use value at expected $T_j$)

IGBT: $P_{cond} = V_{CE(sat)} I_{avg}$ ($V_{CE(sat)}$ is current and temperature dependent)

Diode: $P_{cond} = V_F I_{F(avg)}$

**Trap**: R_DS(on) roughly doubles from 25°C to 125°C. A MOSFET selected for 10 mΩ at 25°C will be ~20 mΩ at operating temperature. Use the hot value for thermal design.

### Switching Loss

MOSFET: $P_{sw} = \frac{1}{2} V_{DS} I_D (t_{rise} + t_{fall}) f_{sw}$ — the triangular approximation.

More accurate: E_on + E_off from the datasheet switching energy curves, multiplied by f_sw.

**Hard switching** vs **soft switching**:

| | Hard switching | Soft switching (ZVS) |
|---|---|---|
| Turn-on | V_DS > 0 when I_D starts | V_DS ≈ 0 when I_D starts |
| Turn-off | I_D > 0 when V_DS rises | I_D ≈ 0 when V_DS rises |
| Switching loss | Significant | Near zero |
| Typical efficiency | 90-96% | 95-99% |

### Core Loss

See [[pe-m8-magnetic-design]] — Steinmetz equation: $P_{core} = K f^\alpha \hat{B}^\beta$ where $\hat{B}$ is the peak AC flux density (half the peak-to-peak value, $\hat{B} = \Delta B / 2$).

## Thermal Management

### Thermal Resistance Model

$T_j = T_{amb} + P_{loss} (R_{\theta JC} + R_{\theta CS} + R_{\theta SA})$

Where:
- R_θJC: junction-to-case (device package)
- R_θCS: case-to-sink (thermal interface material — TIM)
- R_θSA: sink-to-ambient (heatsink)

### Heatsink Design

For natural convection: heatsink size is dominated by surface area. Rule of thumb: 10-15 cm² surface area per watt dissipated, depending on orientation (vertical fins are better than horizontal) and ambient temperature.

For forced convection: airflow velocity is the dominant factor. Doubling airflow roughly halves R_θSA. Use fan curves to determine actual airflow (static pressure vs flow rate).

**Heatsink optimization tips**:
- Fin thickness: 1-2 mm typical for extruded aluminum
- Fin spacing: 4-8 mm for natural convection, 2-4 mm for forced (tighter = more area, but higher pressure drop)
- Base thickness: 3-6 mm — thick enough to spread heat without being excessively heavy
- Surface treatment: black anodizing increases emissivity (improves radiation heat transfer)

### Thermal Interface Material (TIM)

| TIM | Conductivity | R_θ for typical thickness | Reusability |
|-----|-------------|---------------------------|-------------|
| Thermal grease | 3-10 W/m·K | 0.1-0.5 °C·cm²/W | No (pump-out) |
| Thermal pad | 1-6 W/m·K | 0.5-2.0 °C·cm²/W | Limited |
| Phase change material | 3-8 W/m·K (active) | 0.3-1.0 °C·cm²/W | No |
| Graphite sheet | 5-15 W/m·K | 0.1-0.5 °C·cm²/W | Yes |
| Solder (to DBC) | 30-60 W/m·K | <0.1 °C·cm²/W | No (permanent) |

**Trap**: Thermal grease pump-out — under thermal cycling, the grease migrates out of the interface. After thousands of cycles, the thermal resistance increases. Phase change materials and some graphite sheets are more reliable for high-vibration, high-cycling environments.

## EMC / EMI

### Conducted Emissions (150 kHz - 30 MHz)

Source: switching current harmonics. Propagates through input and output cables.

**Differential-mode (DM) noise**: current flows between line and neutral (or +V and return). Filtered by an LC filter (DM choke + X-capacitors).

**Common-mode (CM) noise**: current flows from the power stage to ground through parasitic capacitance. Filtered by a CM choke + Y-capacitors.

EMI filter design procedure:
1. Measure or estimate the DM and CM noise spectrum (up to 30 MHz)
2. Determine the required attenuation at the worst-case frequency
3. Design the filter corner frequency: $f_c = f_{sw}/10$ to $f_{sw}/5$ (for DM)
4. Select X-caps (across L-N, 0.1-1 µF) and Y-caps (L/N to ground, nF range — limited by leakage current standard)
5. Design the CM choke: $L_{cm} = \frac{1}{(2\pi f_c)^2 C_y}$
6. Verify that the filter does not resonate with the converter input impedance

**Trap**: An LC filter's output impedance (looking from the converter) can resonate with the converter's negative input impedance — this causes instability. The filter must be damped. Middlebrook stability criterion: $Z_{out(filter)} < Z_{in(converter)}$ at all frequencies. A practical damping approach: add $R_d \approx \sqrt{L_{cm}/C_x}$ in series with $C_d \approx 4 C_x$ across the filter output.

### Radiated Emissions (30 MHz - 1 GHz)

Sources:
- Switching node (drain/collector) voltage ringing — the largest contributor
- Inductor/transformer magnetic field
- Cable radiation due to CM current

Mitigation:
- Keep the switching node copper area as small as possible (tiny island)
- Use a ground plane on an adjacent layer to provide a return path for displacement currents
- Shield the inductor/transformer with a copper foil (connected to ground)
- Add ferrite beads on cables at the chassis entry point

### PCB Layout for EMI

- **Hot loop (commutation loop)**: minimize the area of the loop that carries switched current — this is the #1 source of radiated EMI. Place the input capacitor as close as possible to the MOSFET drain and the diode cathode.
- **Snubber across the switching node**: an RC snubber (R_s = √(L_parasitic / C_parasitic), typically 10-47 Ω + 100-470 pF) dampens the ringing at the switching node.
- **Gate drive**: a series gate resistor controls dV/dt. Higher R_g → slower switching → lower EMI but higher switching loss. Typical: 5-50 Ω depending on the device and acceptable loss.
- **Keep high dV/dt traces short**: the switching node, gate drive traces, and any trace carrying fast edges must be minimized.

### Standards

| Standard | Scope | Key limits |
|----------|-------|------------|
| CISPR 32 / EN 55032 | IT equipment (Class A/B) | Conducted: 150 kHz-30 MHz, Radiated: 30 MHz-6 GHz |
| CISPR 11 / EN 55011 | Industrial, scientific, medical (ISM) | Conducted + radiated, Class A (industrial) / B (residential) |
| CISPR 25 | Automotive | Conducted + radiated, strictest limits |
| IEC 61000-4-x | Immunity standards | ESD, EFT, surge, conducted RF, magnetic field |

## AutoCAD Connection — Panel & Enclosure Integration

Power electronics system design extends into mechanical CAD. Key elements when translating an electrical design into a panel layout (AutoCAD Electrical or standard AutoCAD):

### Busbar Design
- Busbars carry high current between components (rectifier → DC link → inverter)
- Cross-section: 1 A per 1-2 mm² of copper cross-section (rule of thumb, depends on allowable temp rise)
- Clearance: per IEC 61439-1, minimum clearance for 1000 V is 8 mm (pollution degree 2)
- Creepage: minimum 14 mm for 1000 V (pollution degree 2, CTI group IIIa)
- Use standoffs or insulating brackets to prevent busbar vibration and short circuits

### Component Placement Order
1. Heavy components (transformer, DC link caps, heatsinks) — determine the structural skeleton
2. Power semiconductors — mount on heatsinks with proper TIM and electrical insulation
3. Busbars — route between DC link caps and semiconductor terminals
4. Control PCBs — position away from high dI/dt and high dV/dt areas
5. EMI filter — at the power entry point (AC input)
6. Fan/filter assembly — airflow path must cross the heatsink fins

### Clearance and Creepage (IEC 60950 / 62368 / 61439)

| Voltage | Clearance (basic) | Creepage (basic) |
|---------|-------------------|-------------------|
| 50 V | 0.2 mm | 0.6 mm |
| 100 V | 0.5 mm | 1.5 mm |
| 250 V | 2.0 mm | 3.2 mm |
| 400 V | 3.0 mm | 5.0 mm |
| 800 V | 5.5 mm | 10.0 mm |
| 1000 V | 8.0 mm | 14.0 mm |

Above values are minimum — double for reinforced insulation. Actual values depend on pollution degree, material group, and altitude derating.

### Grounding in Panel Layout
- **PE (Protective Earth)**: green-yellow wire, connected to the chassis ground bar. Every conductive enclosure part >50 V must be bonded to PE.
- **Star ground**: power ground (DC bus return), control ground, and chassis ground meet at a single point (typically the DC bus capacitor ground). Prevents ground loops between circuits.
- **Shield grounding**: cable shields should be grounded at 360° at the panel entry point using EMC cable glands, not pigtail connections.

## References
- Erickson & Maksimovic. *Fundamentals of Power Electronics*. 3rd ed. Ch 4, 18.
- Ott, H.W. *Electromagnetic Compatibility Engineering*. Wiley, 2009.
- Maniktala, S. *Switching Power Supplies A-Z*. 2nd ed.
- IEC 61439-1: Low-voltage switchgear and controlgear assemblies.
- Williams, T. *EMC for Product Designers*. 5th ed. Newnes.
- Schneider Electric. *Electrical Installation Guide*. Ch E, G, M.
