---
tags: [power-electronics, magnetics, transformer, inductor]
aliases: ["PE M8", "Magnetic Design"]
parent: "[[Power Electronics -- Map of Content]]"
created: 2026-06-17
status: complete
---

# M8: Magnetic Design

## Core Materials

| Material | Freq range | Saturation (T) | Permeability | Loss |
|----------|------------|----------------|--------------|------|
| Silicon steel (laminated) | 50/60 Hz - 1 kHz | 1.5-2.0 | 1500-5000 | High |
| Ferrite (MnZn) | 10 kHz - 1 MHz | 0.3-0.5 | 1000-3000 | Low |
| Ferrite (NiZn) | >1 MHz | 0.3-0.4 | 50-500 | Very low |
| Iron powder | 10 kHz - 1 MHz | 0.8-1.5 | 20-200 | High (DC bias) |
| Sendust | 10 kHz - 500 kHz | 0.8-1.0 | 26-125 | Low |
| MPP (Molypermalloy) | 10 kHz - 500 kHz | 0.7-0.8 | 14-550 | Very low |
| Amorphous | 100 Hz - 100 kHz | 1.5-1.6 | 1000-10000 | Low |
| Nanocrystalline | 100 Hz - 100 kHz | 1.2-1.3 | 5000-50000 | Very low |

**Selection rule**: use ferrite for high-frequency transformers (low loss, moderate saturation), use powder cores for inductors requiring high DC bias (distributed gap), use nanocrystalline for high-power, high-efficiency transformers.

## Inductor Design by Area-Product Method

The area product A_p = A_e × A_w (core cross-section × winding window area) determines the power handling capability.

### Design Procedure

1. Specify: L, I_DC, ΔI, f_sw, maximum B (ΔB)
2. Calculate the required energy handling: E = ½ × L × I_pk²
3. Select core: A_p = (2 × E) / (K_u × B_max × J) — basic form, varies by topology
   - K_u = winding fill factor (typically 0.2-0.4)
   - J = current density (3-6 A/mm² for copper, derated for thermal)
4. Calculate the required turns: N = L × I_pk / (B_max × A_e)
5. Check ΔB = L × ΔI / (N × A_e) — must be < B_max
6. Determine air gap: l_g = (N² × μ_0 × A_e) / L — for gapped ferrite designs
7. Select wire gauge: AWG based on current and J, use Litz wire for f_sw > 100 kHz

**Trap**: The area-product method gives a first-pass core estimate. Always verify the design with thermal calculations — the volume-to-surface ratio determines thermal resistance, and a core that fits electrically may overheat thermally.

## Transformer Design

### Turns Ratio

For a forward converter: N_p / N_s = V_in(min) × D_max / V_out

For a flyback: N_p / N_s = (V_in(min) × D_max) / ((V_out + V_diode) × (1-D_max))

### Area-Product for Transformers

A_p = (P_out × 10^4) / (K_f × K_u × B_max × J × f_sw)

Where K_f = waveform coefficient (4.0 for square wave, 4.44 for sine wave).

### Winding Loss

**Skin depth**: δ = √(ρ / (π × μ_0 × μ_r × f)) = 66 / √f (mm for copper)

At 100 kHz: δ ≈ 0.21 mm. For wire diameter > 2δ, current crowds to the outer surface — the effective resistance increases. Use Litz wire (multiple insulated strands of ≤2δ diameter).

**Proximity effect**: current in adjacent conductors induces circulating eddy currents, further increasing the AC resistance. More severe than skin effect in multi-layer windings.

Dowell's equations: model the winding layers as equivalent foils and calculate the AC resistance factor F_R = R_ac / R_dc as a function of the number of layers and the normalized conductor thickness.

**Trap**: Proximity loss can be 10× higher than skin loss in a multi-layer winding. The worst case is when two layers carry current in the same direction — the proximity effect adds constructively. Interleaving primary and secondary windings reduces proximity loss by canceling the magnetic field between layers.

### Core Loss

Steinmetz equation: P_core = K × f^α × B^β

Where K, α, β are material-specific coefficients from the datasheet. For ferrite 3C90: K ≈ 0.25, α ≈ 1.6, β ≈ 2.5-3.0 (varies with frequency and temperature).

**Improved Steinmetz Equation (ISE)**: accounts for the DC bias of the flux waveform in non-sinusoidal excitation (e.g., flyback inductor). Uses the average dV/dt correction. More accurate for square-wave excitation.

## Planar Magnetics

Uses PCB traces as windings — ideal for high-frequency, low-profile, and repeatable manufacturing.

**Advantages**:
- Excellent thermal management (PCB copper conducts heat to the edges)
- Very low leakage inductance (interleaved PCB layers)
- High repeatability (no winding variations)
- Low profile (fits in 8-10 mm height)

**Disadvantages**:
- Limited turns (one turn = one PCB layer) — not suitable for high turns ratio
- Higher capacitance between windings (layer-to-layer)
- Core must use an E-I or E-E shape designed for planar assemblies

**Design**: use 2-4 oz copper PCB, multiple layers connected in parallel for higher current, series-connected for higher turns. Core is typically ferrite E-PLT or E-I shape.

## References

- Erickson & Maksimovic. *Fundamentals of Power Electronics*. 3rd ed. Ch 13-15.
- McLyman, W.T. *Transformer and Inductor Design Handbook*. 4th ed. CRC Press.
- Dowell, P.L. "Effects of Eddy Currents in Transformer Windings." *Proc. IEE*, 1966.
- Passive Components Blog. "Magnetics Design in High-Frequency GaN Converters." Frenetic, 2025.
- Colonel Wm. T. McLyman. *Magnetic Core Selection for Transformers and Inductors*. 2nd ed.
