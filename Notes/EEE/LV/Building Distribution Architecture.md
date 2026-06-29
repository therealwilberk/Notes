---
tags: [lv, mv, architecture, distribution, buildings]
aliases: ["MV/LV Architecture", "Building Electrical Architecture", "Distribution Architecture"]
parent: "[[Notes/EEE/LV/LV Distribution Topologies]]"
created: 2026-06-27
status: in-progress
---

# MV/LV Architecture Design for Buildings

Design process for electrical distribution architecture in medium and large buildings. Covers the decision framework from initial characteristics through equipment selection. Complements [[Notes/EEE/LV/LV Distribution Topologies]] (which covers specific circuit topologies) by explaining *why* and *when* each configuration is chosen.

Based on the Schneider Electric *Electrical Installation Guide* (Chapter D: MV and LV architecture selection guide for buildings), incorporated into IEC 60364-8-1.

## Stakes of Architecture Design

The choice of distribution architecture has a decisive impact across the installation's lifecycle:

| Phase | Impact |
|-------|--------|
| Construction | Installation time, work rate achievable, competencies required from installation teams |
| Operation | Quality and continuity of supply to sensitive loads, power losses in supply circuits |
| End-of-life | Proportion of the installation that can be recycled |

Architecture decisions involve the spatial configuration, power source selection, distribution levels, single-line diagram, and equipment choice. The optimal solution is a compromise between competing performance criteria — and the earlier in the design process trade-offs are explored, the more optimization is possible.

![[assets/image.png|Optimization potential — earlier design decisions enable more optimization]]

A successful outcome depends on exchange between:
- The architect (building organization, user requirements)
- Designers of other technical sections (lighting, HVAC, fluids)
- The user's representatives (process definition)

**Trap:** Architecture decisions made in isolation by one discipline (e.g., electrical only without architectural input) often require costly rework later. The iterative process between steps exists precisely because early assumptions are refined as more constraints surface.

## Architecture Scope

The architecture design process covers three levels of distribution in the building (from upstream to downstream):

1. **MV/LV main distribution** — utility connection point through MV/LV substation(s) to the main LV switchboard
2. **LV power distribution** — from main LV switchboard to sub-distribution boards
3. **Terminal distribution** — from sub-distribution boards to final loads (exceptionally included)

In buildings, all consumers connect at low voltage. MV distribution therefore consists only of:
- Connection to the utility network
- Distribution to MV/LV substation(s)
- The MV/LV substation(s) themselves

## Installation Characteristics

These characteristics define the inputs to the architecture design process. Each has several categories that constrain the decisions made in subsequent steps.

### Sector of Activity (IEC 60364-8-1)

| Sector | Examples |
|--------|----------|
| Residential | Private habitation |
| Commercial | Offices, retail, public buildings, banks, hotels |
| Industrial | Factories, workshops, distribution centers |
| Infrastructure | Airports, harbors, rail, transport facilities |

### Site Topology

| Category | Description |
|----------|-------------|
| Single storey | One level |
| Multi-storey | Multiple floors in one building |
| Multi-building | Campus or site with several buildings |
| High-rise | Building exceeding local height threshold |

On multi-building sites, the trade-off is between a central substation vs distributed substations per building. Centralization reduces transformer count and MV cable length but increases LV feeder length and losses.

### Layout Latitude

The degree of freedom in positioning electrical equipment:

| Level | Meaning |
|-------|---------|
| Low | Position virtually imposed (existing constraints, heritage buildings) |
| Medium | Partially imposed — compromises needed |
| High | No constraints — equipment can be positioned to best satisfy criteria |

Layout latitude directly affects the feasibility of centralized vs distributed LV distribution (see [[Notes/EEE/LV/LV Distribution Topologies]]).

### Service Reliability

The ability of the power system to meet its supply function for a specified period.

| Level | Description |
|-------|-------------|
| Minimum | Risk of interruptions from geographical, technical, or economic constraints |
| Standard | Normal utility supply reliability |
| Enhanced | Special measures (underground network, strong meshing, dual feeds) |

Reliability level drives the choice of LV circuit configuration — a minimum level may accept a radial feeder, while enhanced reliability requires double-ended or ring configurations.

### Maintainability

Features that limit the impact of maintenance on installation operation.

| Level | Description |
|-------|-------------|
| Minimum | Installation must be stopped for maintenance |
| Standard | Maintenance possible during operation with degraded performance — scheduled during low activity. Example: parallel transformers with partial redundancy and load shedding |
| Enhanced | Maintenance without disturbing operation. Example: double-ended configuration with bus coupler |

Maintainability also constrains the choice of LV topology. A split bus (normally open coupler) allows one transformer to be serviced while the other carries the full load.

### Installation Flexibility

The possibility of moving power delivery points or increasing supplied power after commissioning.

| Level | Description |
|-------|-------------|
| None | Load positions fixed for lifecycle (smelting works, heavy process) |
| Design flexibility | Delivery points, power, or locations not precisely known during design |
| Implementation flexibility | Loads installed after commissioning |
| Operating flexibility | Load positions fluctuate during operation (reorganization, partitioning) |

Flexibility requirements influence busway vs cable distribution, and the sizing of upstream infrastructure for future expansion.

### Power Demand

Maximum apparent power demand used to size the installation:

- < 630 kVA
- 630 to 1250 kVA
- 1250 to 2500 kVA
- > 2500 kVA

Power demand brackets drive the number of transformers, MV connection type (simple or dual), and MV switchgear ratings.

### Load Distribution

The uniformity of load distribution in kVA/m²:

| Type | Characteristics | Examples |
|------|-----------------|----------|
| Uniform | Low/medium unit power spread over large area | Lighting, individual workstations |
| Intermediate | Medium power in groups | Assembly machines, workstations, modular logistics |
| Localized | High power concentrated in specific areas | HVAC, chillers, data center pods |

Uniform loads favor distributed LV distribution (long feeders, many small panels). Localized loads favor centralized distribution with dedicated feeds to high-power equipment.

**Trap:** Load distribution is often assumed uniform during the preliminary design phase and later discovered to be localized — this can require reworking the LV layout. Leave flexibility margin in busbar sizing.

### Voltage Interruption Sensitivity

The aptitude of a circuit to accept a power interruption:

| Category | Description |
|----------|-------------|
| Sheddable | Can be shut down at any time for indefinite duration |
| Long interruption acceptable | > 3 minutes |
| Short interruption acceptable | < 3 minutes |
| No interruption acceptable | UPS or backup required |

Criticality levels inform which loads get backup power:

| Criticality | Consequence of Interruption | Example Loads |
|-------------|----------------------------|---------------|
| Non-critical | No notable consequence | Sanitary water heating |
| Low | Temporary discomfort, no financial loss | HVAC |
| Medium | Short process break, deterioration if prolonged | Refrigeration, lifts |
| High | Mortal danger or unacceptable financial loss | Operating theatres, IT, security |

Circuit criticality determines whether a UPS, backup generator, or automatic transfer scheme is required. See [[Notes/EEE/LV/LV Distribution Topologies]] for the double-ended supply configuration used for high-criticality loads.

### Disturbance Sensitivity

The ability of a circuit to work correctly in the presence of electrical disturbances (overvoltages, harmonics, voltage dips, imbalance, fluctuation).

| Level | Effect | Examples |
|-------|--------|----------|
| Low | Disturbances have little effect | Heating |
| Medium | Notable deterioration in operation | Motors, lighting |
| High | Stopping or deterioration of equipment | IT equipment |

**Design implication:** Sensitive loads should be separated from disturbing loads. This is the basis for segregating "dirty" circuits (VFDs, UPS) from "clean" circuits (computers, medical equipment). See [[harm-m4-effects]] for how harmonic-sensitive equipment interacts with nonlinear loads.

### Disturbance Potential of Circuits

The ability of a circuit to disturb surrounding circuits through harmonics, inrush current, imbalance, HF currents, or electromagnetic radiation.

| Level | Design Response | Examples |
|-------|----------------|----------|
| Non-disturbing | No special precautions | Resistive heating |
| Moderate/occasional | Separate supply may be needed near sensitive circuits | Lighting (harmonic currents) |
| Very disturbing | Dedicated circuit or mitigation essential | Motors (high inrush), welding (fluctuating current) |

Disturbance potential and disturbance sensitivity are paired characteristics. A circuit high on one scale matched with a circuit high on the other on the same bus creates a power quality problem. The solution is either spatial separation (dedicated transformers or panelboards) or mitigation equipment (filters, soft starters).

## Architecture Fundamentals — Stage 1 Decisions

The first stage defines the high-level architecture:

### 1. Connection to the Utility Network

- Simple connection (single MV feeder)
- Dual connection (two independent MV feeders for redundancy)
- Loop connection (part of a ring)

### 2. Internal MV Distribution

- Radial MV feeders to each substation (simplest, lowest cost)
- Loop MV feeders (partial redundancy)
- Double-ended MV supply (full redundancy)

### 3. Number and Location of MV/LV Substations

Driven by:
- Site topology (single vs multi-building)
- Power demand and load distribution
- LV feeder length limits (voltage drop, cable cost)
- Architectural constraints (substation footprint, ventilation)

### 4. Number of MV/LV Transformers

Driven by:
- Total power demand
- Redundancy requirements (N, N+1, 2N)
- Load distribution (centralized vs distributed substations)
- Space and cost constraints

### 5. MV Back-up Generator

Decision factors:
- Which loads require backup (criticality assessment)
- Interruption sensitivity of those loads
- Generator sizing and fuel storage

## Architecture Details — Stage 2 Decisions

The second stage refines the LV distribution:

- Centralized vs distributed LV layout
- LV backup generator or UPS presence
- Configuration of LV circuits (see [[Notes/EEE/LV/LV Distribution Topologies]] for radial, parallel, split bus, ring, double-ended)
- Protection coordination and discrimination

## The Whole 3-Step Process

![[assets/image 2.png|Flow diagram for choosing electrical distribution architecture (Fig. D3)]]

```
Step 1: Architecture Fundamentals
  ↓
Step 2: Architecture Details ← ─ ─ ─ ┐
  ↓                                    │
Step 3: Equipment Selection ← ─ ─ ─ ─ ┘
  ↓
Assessment (review with customer)
  ↓ (iterate if criteria not met)
Back to Step 1, 2, or 3 as needed
```

### Step 1: Architecture Fundamentals

Define the general features based on macroscopic characteristics (sector, site topology, power demand, service reliability). Output: several distribution schematic diagram solutions that serve as a starting point for the single-line diagram.

### Step 2: Architecture Details

Define the installation in detail based on the fundamental choices and criteria related to implementation and operation. If criteria are not satisfied, iterate back to Step 1. Output: a detailed single-line diagram.

### Step 3: Equipment Selection

Select equipment from manufacturer catalogs based on the chosen architecture. Iterate back to Step 2 if equipment characteristics cannot satisfy requirements.

### Assessment

The design office presents figures to the customer and other stakeholders as a basis for discussion. Iteration can loop back to any of the three steps depending on feedback.

**Trap:** The iterative nature of this process means early-stage assumptions about cost or space often get revised. Reserving budget and schedule contingency for at least one loop-back is prudent. Projects that treat architecture as a once-through linear process consistently produce suboptimal results.

## Architecture Assessment Criteria

The guide enumerates these evaluation dimensions (detailed in the "Architecture assessment criteria" and "Recommendations for architecture optimization" pages):

| Criterion | What It Evaluates |
|-----------|-------------------|
| Availability | Probability of supply continuity — affects process uptime |
| Capex / Opex | Initial cost vs lifetime operating cost (losses, maintenance) |
| Power quality | Voltage distortion levels, harmonic compliance — see [[harm-m5-standards]] |
| Scalability | Ease of future expansion without major rework |
| Selectivity | Fault isolation capability — which loads are lost vs retained |
| Safety | Compliance with regulations, arc flash risk, emergency disconnect |

## References

- Schneider Electric. *Electrical Installation Guide.* Chapter D: MV and LV architecture selection guide for buildings.
  - [Stakes of architecture design](https://www.electrical-installation.org/enwiki/Stakes_of_architecture_design)
  - [The architecture design](https://www.electrical-installation.org/enwiki/The_architecture_design)
  - [Electrical installation characteristics](https://www.electrical-installation.org/enwiki/Electrical_installation_characteristics)
  - [Choice of architecture fundamentals](https://www.electrical-installation.org/enwiki/Choice_of_architecture_fundamentals)
  - [The whole process](https://www.electrical-installation.org/enwiki/The_whole_process)
- IEC 60364-8-1. *Low voltage electrical installations — Energy Efficiency.*
