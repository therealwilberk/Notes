---
tags: [lv, switchgear, power-distribution, protection]
aliases: ["Low-Voltage Switchgear", "LV Switchgear Fundamentals", "Metal-Enclosed LV Switchgear"]
parent: "[[Notes/EEE/LV/Building Distribution Architecture]]"
created: 2026-06-27
status: complete
---

# Low-Voltage Switchgear

Three-phase power distribution product that supplies electric power at voltages up to 1000 V and current up to 6000 A. ANSI/NEMA switchgear is rated up to 635 V with main bus continuous current up to 10,000 A (parallel sources).

Found on the secondary side of a power distribution transformer (transformer + switchgear = substation). Feeds LV motor control centers, switchboards, and branch/feeder circuits. Used in heavy industry, manufacturing, mining, petrochemical, pulp and paper, utilities, water treatment, data centers, healthcare.

## Construction and Compartments

Each vertical section divides into three isolated compartments:

### Breaker Compartment

Holds up to four LV power circuit breakers vertically, each individually compartmentalized. Breakers are typically draw-out — movable to test/disconnect positions and fully withdrawable for service without de-energizing the gear. Faceplate and controls accessible without opening the enclosure (through-the-door).

### Bus Compartment

Behind the breaker compartment, separated by solid barriers. Silver- or tin-plated copper bus. Vertical risers connect to breaker stabs via finger clusters. Horizontal (main) bus connects adjacent sections. Insulated barrier between adjacent bus compartments. Insulation applied where air gap is insufficient for dielectric strength.

### Cable Compartment

Rear of the section. Hinged doors or removable covers for access to landing lugs.

Two configurations:
- **Rear-accessible**: cable compartment at rear, requires rear access
- **Front-accessible**: cable compartment adjacent to breaker compartment with doors on the front — shallower, wall-mountable like a switchboard

Compartmentalization prevents accidental contact with energized conductors during maintenance and limits arc flash damage propagation.

See [[Notes/EEE/LV/lv-switchgear-ratings]] for the full treatment of IEC 61439 catalog parameters including Ui, Uimp, InA, Inc, Icw, Ipk, RDF, and their interrelationships.

## Ratings

| Rating | Typical Value |
|--------|---------------|
| Maximum voltage | Up to 635 V (ANSI/NEMA) |
| Power frequency | 50 / 60 Hz |
| Insulation level | 2.2 kV |
| Continuous current | Up to 10,000 A |
| Short-circuit withstand (SCCR) | Up to 200 kA |
| Short-time withstand | Up to 100 kA, 30 cycles |

### Short-Circuit Withstand Current Rating (SCCR)

The maximum short-circuit current the assembly can safely withstand for at least four cycles (60 Hz basis) when protected by an overcurrent protective device. Defined per ANSI/IEEE C37.20.1. Determines minimum bus bracing.

The SCCR of the switchgear must equal the SCCR of the lowest-rated breaker in the assembly.

### Short-Time Withstand Current Rating

The fault current the assembly can endure for 30 cycles (0.5 s) without damage. Tested as two periods of 0.5 s separated by 15 s of zero current.

LV power circuit breakers are designed to withstand a fault for up to 30 cycles without tripping. Compare to molded case circuit breakers (MCCBs) which trip instantaneously within 3-4 cycles. The longer withstand enables selective coordination.

### Interrupt Rating

The maximum current a circuit breaker can safely interrupt at a specified voltage. Must meet or exceed both the short-circuit withstand rating of the breaker and the maximum available fault current from the upstream source.

## Circuit Breakers

Low-voltage power circuit breakers (LV-PCBs) interrupt faults via main contacts parting in open air — these are air circuit breakers (ACBs). MV breakers instead use vacuum interrupters. Integral trip units provide short-circuit and overload protection. Draw-out design enables service without de-energizing.

## Selective Coordination

The device closest to the fault opens first while upstream breakers remain closed. Achieved by programming upstream LV-PCBs with short-time delay (up to 30 cycles) to let downstream devices clear the fault first.

**Trade-off:** Selective coordination increases incident energy at certain points. NEC Article 240.87 requires technologies that reduce arc energy when selective coordination is implemented — e.g., overriding short-time delays during an arcing fault.

## Switchgear vs Switchboards

| Property | Switchgear | Switchboard |
|----------|------------|-------------|
| Standard | UL 1558 | UL 891 |
| Construction | Compartmentalized barriers | Dead-front, open chassis |
| Circuit breakers | Draw-out LV-PCB | Fixed-mounted MCCB |
| Short-time rating | 30 cycles | 3 cycles |
| Selective coordination | Yes (programmable delay) | Limited |
| Arc-flash safety tech | Available | Not available |
| Serviceability | Breakers removed while energized | Must de-energize |
| Footprint | Larger | Smaller |
| Cost | Higher | Lower |

In practice: switchgear at the service entrance or transformer secondary feeds switchboards and MCCs downstream. See [[Notes/EEE/LV/lv-switchboard-operation]] for the detailed operating sequence of a switchboard.

## Applicable Standards

| Standard | Scope |
|----------|-------|
| ANSI/IEEE C37.20.1 | Metal-enclosed LV power circuit breaker switchgear (1000 Vac, 3200 Vdc) |
| ANSI/IEEE C37.20.7 | Internal arcing fault testing (up to 38 kV) |
| UL 1558 | Safety standard for metal-enclosed LV power circuit breaker switchgear |
| UL 1066 | LV AC and DC power circuit breakers used in enclosures |

## Safety Technologies

- **Arc Quenching Switchgear**: Contains and extinguishes an internal arc fault
- **Arc-Resistant Switchgear**: Channels arc gases away from personnel via plenums
- **Zone Selective Interlocking (ZSI)**: Breakers communicate fault location; upstream breaker restrains while downstream clears
- **Arc Flash Reduction Maintenance System (ARMS)**: Temporarily lowers instantaneous trip settings during maintenance
- **Arc Flash Detection Relay**: Detects light from an arc and trips upstream breaker
- **Bus Differential Protection**: Detects difference between current entering and leaving a bus section

These technologies reduce incident energy, limit arc flash damage, and improve safety without sacrificing selective coordination during normal operation.

## See Also

- [[Notes/EEE/LV/cable-sizing-methodology]] — complete cable sizing workflow from IB to short-circuit check
- [[Notes/EEE/LV/cable-sizing-protection-coordination]] — IB, In, Iz, I₂ coordination rules
- [[Notes/EEE/LV/cable-sizing-adiabatic]] — short-circuit withstand verification (I²t = k²S²)

## References

- Eaton. *Low-voltage switchgear fundamentals.* (Technical content only; vendor-specific sales content discarded)
- ANSI/IEEE C37.20.1. *Standard for Metal-Enclosed Low-Voltage Power Circuit Breaker Switchgear.*
- UL 1558. *Metal-Enclosed Low-Voltage Power Circuit Breaker Switchgear.*
