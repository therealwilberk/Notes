---
tags: [lv, switchgear, switchboard, ratings, iec-61439, parameters]
aliases: ["LV Switchgear Catalog Parameters", "Switchgear Ratings", "IEC 61439 Ratings", "Ue Ui Uimp InA InC Icw Ipk", "Switchboard Nameplate Parameters"]
parent: "[[Notes/EEE/LV/lv-switchgear]]"
created: 2026-06-27
status: complete
---

# LV Switchgear and Switchboard Catalog Parameters

## Voltage Ratings

Three distinct voltage parameters appear on every LV assembly nameplate. Each serves a different purpose and is verified by a different test.

### Rated Operating Voltage (Ue)

The voltage at which the assembly normally operates. For AC systems this is specified as an RMS value between phases. Typical values: 400 V, 415 V, 480 V, 600 V, 690 V.

The switching devices inside the assembly are tested to interrupt faults at this voltage. Operating above Ue means the breaker's arc-quenching capability may be insufficient — the arc may not extinguish.

### Rated Insulation Voltage (Ui)

The maximum continuous RMS voltage the insulation system can withstand without breakdown. Ui is always equal to or greater than Ue.

Ui is not an operating voltage. It is an insulation design parameter. It determines creepage distances — the shortest path along the surface of insulation between conductors of different phases or between phase and earth. Longer creepage paths are required for higher Ui values to prevent tracking (surface breakdown) over time.

**Why Ui exceeds Ue.** The insulation system must tolerate:
- Temporary overvoltages during earth faults (the sound phases rise to line-to-line voltage in an unearthed or impedance-earthed system)
- Voltage regulation effects — the actual voltage at the switchboard terminals may exceed the nominal system voltage
- Manufacturing tolerances in insulation thickness and material quality
- Aging — insulation properties degrade over decades of thermal cycling
- Surface contamination — dust, moisture, and chemical deposits reduce the effective creepage resistance
- Altitude — above 2000 m, air density decreases and dielectric strength is reduced

**Common values and what they imply:**

| Ui | Typical application | Creepage requirement |
|----|--------------------|---------------------|
| 660 V | Older standard, legacy systems | Shorter paths, smaller insulators |
| 690 V | Modern IEC 400 V systems | Standard creepage distances for pollution degree 3 |
| 800 V | Systems with elevated temporary overvoltages | 15-20% longer creepage than 690 V |
| 1000 V | Heavy industrial, mining | Longest creepage, largest insulator form factor |

Ui does not mean the assembly can operate at that voltage. A board with Ue = 415 V and Ui = 690 V cannot be used on a 690 V system. The switching devices inside are only rated and tested for 415 V interruption. Ui only describes the insulation's continuous withstand.

### Rated Impulse Withstand Voltage (Uimp)

The peak voltage of a specified impulse waveform (1.2/50 μs) that the assembly's insulation can withstand without flashover. Uimp is always a peak value — impulses are not sine waves, so RMS is meaningless.

**Overvoltage categories.** IEC 60664-1 and IEC 61439-1 define four categories based on where in the installation the equipment is located. A higher category means exposure to higher transient energy.

| Category | Location | Example equipment | Typical Uimp for 400/690 V system |
|----------|----------|------------------|----------------------------------|
| IV | Origin of the installation | Service entrance switchboards, main distribution boards | 8 kV |
| III | Distribution within the building | Sub-distribution boards, switchgear | 6 kV |
| II | Load equipment | Appliances, tools, plug-connected equipment | 4 kV |
| I | Specially protected circuits | Electronics with external surge protection | 1.5 kV |

From IEC 61439-1 Table G.1, for a 400/690 V system (maximum Ue-to-earth = 347-600 V RMS):
- Overvoltage category IV (main switchboard): Uimp = 8 kV
- Overvoltage category III (distribution): Uimp = 6 kV
- Overvoltage category II (load): Uimp = 4 kV

These values are at 2000 m altitude. At sea level the test voltage is higher because denser air requires a higher voltage to cause flashover — for a 8 kV rated impulse, the sea-level test voltage is 9.8 kV peak.

**Clearances are designed from Uimp, not Ue.** The minimum air gap between live parts of different phases, and between live parts and earth, is determined by Uimp and the pollution degree. For a 8 kV Uimp and pollution degree 3 (industrial environment), the minimum clearance is approximately 8 mm. A board with Ue = 415 V and Uimp = 4 kV can have smaller clearances than one with Uimp = 8 kV, even though both operate at the same Ue. This has direct consequences for busbar spacing and enclosure dimensions.

**Sources of impulses.** External: lightning strikes to nearby lines or structures. Even an indirect strike kilometers away induces a traveling wave that propagates through the utility network and arrives at the switchboard terminals. Internal: switching operations — transformer energization, motor starting, capacitor bank switching, VFD operation, welding. The voltage spike from interrupting an inductive circuit follows V = L di/dt. A small contactor opening 10 A into a 1 H motor winding produces a 10 kV spike if the current is forced to zero in 1 ms.

**Ui vs Uimp.** Ui describes sustained voltage endurance — how the insulation holds up over years of continuous stress. Uimp describes transient voltage survival — whether a microsecond spike causes instantaneous flashover. Both must be satisfied independently. A design with adequate creepage for Ui may still have insufficient clearance for Uimp, and vice versa.

## RMS vs Peak

All AC system voltages are specified in RMS unless explicitly stated otherwise. When a standard says 415 V, it means 415 V RMS. The relationship for a sinusoidal waveform:

- Peak = RMS x sqrt(2) ≈ RMS x 1.414
- For 415 V RMS: peak = 587 V
- For 230 V RMS: peak = 325 V

Uimp is the exception — it is always a peak value because the impulse waveform has no meaningful RMS equivalent.

## Current Ratings

### Assembly Rated Current (InA)

The maximum continuous current the entire assembly can carry and distribute without exceeding the temperature rise limits in IEC 61439-1 Table 6. InA is the smaller of two values:

1. The sum of the rated currents of the incoming circuits operated in parallel
2. The total current the main busbar can distribute in that specific physical arrangement

InA is not the rating of the main breaker. A common misconception: a 630 A main breaker does not guarantee InA = 630 A. If the busbar layout inside the enclosure can only distribute 500 A before exceeding the 105 K temperature rise limit for bare copper, then InA = 500 A.

InA is determined by temperature-rise testing (or calculation or derivation per IEC 61439-1 Clause 10.10) of the complete assembly in its actual physical configuration — covers closed, all internal partitions in place, busbars mounted as they would be in service. The test measures temperatures at critical points: busbar joints, breaker terminals, cable lugs, enclosure surfaces.

**Temperature rise limits (IEC 61439-1 Table 6, ambient = 35 C):**

| Component | Maximum rise | Maximum absolute |
|-----------|-------------|-----------------|
| Bare copper busbars and connections | 105 K | 140 C |
| Bolted busbar joints | 65 K | 100 C |
| Breaker and device terminals | 70 K | 105 C |
| External insulated conductors (cable lugs) | 70 K | 105 C |
| Accessible external metal surfaces | 30 K | 65 C |
| Operating handles (plastic) | 15 K | 50 C |

A 70 K rise at the terminals means if the ambient temperature in the room is 35 C, the terminal can reach 105 C. If the switchboard is installed in a 45 C boiler room, the same 70 K rise produces 115 C — exceeding the absolute limit. Altitude and ambient temperature derating must be applied when conditions exceed the standard's reference values.

### Circuit Rated Current (Inc)

The maximum continuous current a single outgoing circuit can carry when loaded alone, without exceeding temperature rise limits. Inc is higher than what that same circuit could carry when all adjacent circuits are simultaneously loaded, because the mutual heating from neighboring circuits is absent during a single-circuit test.

Inc is determined by testing a functional unit in isolation. The unit is mounted in the enclosure, all covers are in place, and current is increased until one of the temperature rise limits is reached. The current at that point becomes Inc.

### Relationship Between InA and Inc

InA is always less than the sum of all Inc values because not every circuit can be simultaneously loaded to its individual maximum without exceeding the assembly's total temperature rise. The manufacturer assigns a Rated Diversity Factor (RDF) to account for this.

## Rated Diversity Factor (RDF)

The fraction of Inc at which outgoing circuits can be continuously and simultaneously loaded, accounting for mutual thermal heating. RDF is expressed as a per-unit value: RDF = 0.8 means each circuit can carry 80% of its Inc continuously when all circuits are loaded together.

In the absence of specified load currents, IEC 61439-2 Table 101 provides default RDF values based on the number of circuits:

| Number of outgoing circuits | Default RDF |
|---------------------------|-------------|
| 2-3 | 0.9 |
| 4-5 | 0.8 |
| 6-9 | 0.7 |
| 10 or more | 0.6 |

The temperature-rise test applies the RDF: incoming circuit at InA, outgoing circuits at Inc x RDF. The test verifies that Σ(Inc x RDF) does not exceed InA and that no individual component exceeds its temperature limit.

If the manufacturer specifies RDF = 1.0, this means the busbar and enclosure can dissipate the heat from every circuit loaded to its full Inc simultaneously — a demanding design target that typically requires oversized busbars and forced ventilation.

## Short-Circuit Ratings

### Uninfluenced Short-Circuit Current (Icp)

The prospective RMS short-circuit current at the supply terminals of the assembly, determined by the upstream transformer size and impedance, cable impedance, and network configuration. Icp is not a rating — it is a site-specific calculation. The assembly's withstand ratings must be greater than or equal to Icp.

For a 1000 kVA transformer with 6% impedance at 400 V:

Icp = 1000 kVA / (sqrt(3) x 400 V x 0.06) = 24 kA approximately

For a 2000 kVA transformer: Icp ≈ 48 kA.

Typical Icp values at a main LV switchboard range from 25 kA to 65 kA depending on transformer size and impedance.

### Rated Short-Time Withstand Current (Icw)

The RMS fault current the assembly can withstand for a specified duration without damage. Icw is a thermal rating — it tests whether the busbars, joints, and conductor insulation can survive the I^2 t heating of the fault current until the protection device clears the fault.

Common values: 25 kA / 1 s, 35 kA / 1 s, 50 kA / 1 s, 65 kA / 1 s, 85 kA / 1 s.

The heating during a fault is proportional to I^2 t. A 50 kA fault for 1 second produces the same heating as a 100 kA fault for 0.25 seconds (since (100^2 x 0.25) = (50^2 x 1.0)). The manufacturer may specify Icw for multiple durations: e.g., Icw = 65 kA / 1 s or 85 kA / 0.5 s. The product I^2 t must remain within the assembly's rated thermal capability.

Icw is tested with the incoming short-circuit protective device bypassed. The test current is applied for the declared duration, and the assembly must remain mechanically intact and thermally undamaged. Busbar joints must not exceed the Class 2 temperature limit (200 C) after the test.

### Rated Peak Withstand Current (Ipk)

The maximum instantaneous peak current the assembly can withstand. Ipk determines the mechanical withstand — the electrodynamic forces between busbars during the first asymmetrical current peak of a fault.

Ipk is related to Icw through the power factor (X/R ratio) of the fault:

| Condition | Ipk / Icw ratio |
|-----------|----------------|
| Icw duration = 1 s (typical network X/R) | Ipk = 2.2 x Icw |
| Icw duration = 3 s (low X/R, generators) | Ipk = 2.0 x Icw |
| High X/R (X/R > 14) | Ipk up to 2.7 x Icw |

For Icw = 65 kA / 1 s: Ipk = 2.2 x 65 = 143 kA peak.

**Thermal vs mechanical.** Icw tests thermal survival (does the busbar overheat and sag?). Ipk tests mechanical survival (do the electrodynamic forces bend busbars, snap supports, or slam conductors together?). The peak current in the first half-cycle produces forces proportional to Ipk^2. Those forces try to push parallel conductors apart or pull them together. The busbar supports and bracing must hold the conductors rigidly in place. A board that passes the Icw thermal test may still fail the Ipk mechanical test if the supports are too widely spaced or insufficiently braced.

### Rated Conditional Short-Circuit Current (Icc)

The prospective short-circuit current the assembly can withstand when protected by a specific upstream short-circuit protective device (SCPD) — typically a current-limiting fuse or breaker with a high breaking capacity. Icc applies when the SCPD limits both the magnitude and duration of the fault current reaching the assembly.

Icc can be higher than Icw because the SCPD limits the let-through energy. For example, a fuse may limit a 100 kA prospective fault to a peak let-through of only 30 kA and clear it within 4 ms. The busbar only sees a fraction of the total fault energy. The manufacturer declares Icc = 100 kA (prospective) with the condition that a specific fuse type is installed upstream.

### Circuit Breaker Breaking Capacities

The assembly ratings above describe withstand — the ability to survive a fault. The circuit breaker ratings describe interruption — the ability to open the faulted circuit and extinguish the arc.

**Icu (ultimate breaking capacity).** The maximum fault current the breaker can interrupt once, after which it may need replacement. Test sequence: O (open under fault) — 3 minute pause — CO (close and immediately open under fault). The breaker may sustain damage and need replacement after this sequence.

**Ics (service breaking capacity).** The maximum fault current the breaker can interrupt repeatedly and remain fully serviceable. Test sequence: O — t — CO — t — CO. Ics is expressed as a percentage of Icu: typical values are 25%, 50%, 75%, or 100% of Icu. A breaker with Icu = 65 kA and Ics = 50% (32.5 kA) can interrupt a 32.5 kA fault and continue operating normally afterward.

**Coordination rule.** The operating principle: Icw (assembly withstand) and Icu (breaker interruption) are independent ratings. Neither is required to equal the other. The only requirement is that whichever is lower must exceed the system fault current (Icp). A board with Icw = 50 kA can contain breakers with Icu = 65 kA, because the fault current (Icp = say 40 kA) is below both. The breaker interrupts the fault, but the assembly must survive until the breaker clears it — hence the assembly Icw must be adequate for the fault duration, which is the breaker's total clearing time.

### Putting Short-Circuit Ratings Together

```
System fault current at board: Icp = 40 kA RMS
                                first peak = 40 x 2.2 = 88 kA peak

Assembly ratings:
  Icw = 50 kA / 1 s        → busbar survives 40 kA for the breaker's clearing time
  Ipk = 110 kA peak         → busbar supports survive 88 kA peak

Main breaker:
  Icu = 65 kA               → can interrupt 40 kA fault
  Ics = 65 kA (100%)        → fully serviceable after interruption

Result: coordinated. All ratings exceed the system fault level.
```

## Complete Nameplate Example

A typical 415 V main switchboard nameplate under IEC 61439:

| Parameter | Value | Meaning |
|-----------|-------|---------|
| Ue | 415 V | Normal operating voltage |
| Ui | 690 V | Insulation designed for 690 V continuous |
| Uimp | 8 kV | Survives 8 kV peak impulse (overvoltage cat. IV) |
| InA | 3200 A | Main bus can carry 3200 A continuously |
| RDF | 0.8 | Outgoing circuits can be loaded to 80% of Inc simultaneously |
| Icw | 65 kA / 1 s | Busbar withstands 65 kA RMS for 1 second |
| Ipk | 143 kA | Busbar supports survive 143 kA peak |
| Icc | 85 kA (with fuse type X) | Withstands 85 kA when protected by specified fuse |
| Standard | IEC 61439-1, -2 | Design and verification standard |

## References

- IEC 61439-1:2020. *Low-voltage switchgear and controlgear assemblies — General rules.*
- IEC 61439-2:2020. *Low-voltage switchgear and controlgear assemblies — Power switchgear and controlgear assemblies.*
- IEC 60664-1:2020. *Insulation coordination for equipment within low-voltage supply systems.*
- IEC 60947-2. *Low-voltage switchgear and controlgear — Circuit-breakers.*
- IEC TR 60890. *A method of temperature-rise assessment by extrapolation.*
- ABB. *Technical Application Papers No. 11: Guidelines to the construction of a low-voltage assembly complying with IEC 61439 Part 1 and Part 2.*
- Schneider Electric. *IEC 61439: Rated current of electrical panel and switchboard protection devices.*
- Eaton. *White paper: IEC/EN 61439 series — Evolution of the standard for LV switchgear and controlgear assemblies.* (technical content only)
