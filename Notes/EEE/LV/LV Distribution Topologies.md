---
tags: [lv, distribution, topologies, redundancy, power-system]
aliases: ["LV Circuit Configurations", "LV Distribution Topologies", "LV Config", "Circuit Topologies"]
parent: "[[Notes/EEE/LV/Building Distribution Architecture]]"
created: 2026-06-27
status: in-progress
---

# LV Distribution Topologies

Every LV distribution configuration is a different answer to one question: **if a component fails, is there another path for power to reach the load?**

As redundancy increases, so do installation cost and protection complexity. The choice is a trade-off between availability and economics.

---

## 1. Single Feeder (Radial)

```text
Utility
   │
Transformer
   │
Main LV Switchboard
   │
Loads
```

One transformer feeding one switchboard via a single supply path. The simplest and lowest-cost configuration. Protection coordination is straightforward because there is only one path — no directional overcurrent or bus transfer logic needed.

**Failure mode:** Any upstream fault (transformer, cable, main breaker) interrupts all downstream loads. No redundancy.

**Applications:** Small commercial buildings, residential installations, small workshops.

**Trap:** A radial feeder is often adequate for a standalone building but becomes a single point of failure when critical loads are added later. If a building is later expanded or the tenant mix changes to include sensitive equipment, retrofitting redundancy is expensive. Sizing the main switchboard with future bus coupler provisions during initial install is cheap insurance.

---

## 2. Parallel Transformers

```text
        T1
         │
         ├──── Main LV Bus ─── Loads
         │
        T2
```

Two (or more) transformers feeding the same bus. Load is shared under normal operation.

**Failure mode:** If T1 fails, T2 carries the full load — provided T2 was sized for this contingency (N+1). The bus itself remains a single point of failure; a bus fault takes everything down.

**Advantages:**
- Increased total capacity. Transformers can share the load at partial loading for better efficiency.
- N+1 redundancy. One transformer can fail without dropping load.

**Disadvantages:**
- Higher fault current — both transformers contribute to a bus fault. Switchgear must be rated for the combined short-circuit current.
- A bus fault affects all loads. No isolation between transformer sections.
- Protection coordination is more complex — requires differential protection or directional overcurrent for the transformer incomers.

**Applications:** Large commercial buildings, data centers, hospitals.

**Trap:** Parallel transformers must have matched impedance percentages (within 7.5% per IEC 60076) to share load proportionally. Mismatched impedances cause unequal loading — one transformer carries more than its share, potentially tripping on overload while the other remains underloaded.

---

## 3. Split Bus (Normally Open Coupled Transformers)

```text
      T1              T2
       │               │
   MLVS A          MLVS B
       X
(Normally Open Bus Coupler)
```

The main switchboard is split into two independent sections, each fed by its own transformer. A bus coupler connects the two sections but remains normally open.

**Normal operation:** T1 feeds MLVS A. T2 feeds MLVS B. No power flows through the coupler.

**Failure operation (T1 fails):**
1. Isolate T1 (open its incomer).
2. Verify T2 is healthy and has capacity.
3. Close the bus coupler.
4. T2 now supplies both bus sections.

The split bus provides the isolation benefits of independent sections with the ability to cross-feed during a contingency.

**Advantages:**
- High availability. A transformer failure does not drop its section — just requires a transfer.
- Lower fault current than parallel transformers — each transformer sees only its own contribution plus the remote contribution through the coupler (which is limited by the coupler impedance).
- Better fault isolation — a fault on one bus section does not affect the other.
- Maintenance can be performed on one transformer without affecting the other.

**Disadvantages:**
- More switchgear — two incomers plus a bus coupler.
- Automatic transfer logic (bus coupler auto-close) may be required for fast restoration. Without it, restoration is manual.

### ATS Clarification

The "ATS" in this context is an **Automatic Bus Transfer** scheme that monitors transformer incomers and controls the bus coupler. It is not a utility-generator transfer switch. The ATS logic must ensure the failed incomer is open before closing the coupler (break-before-make) to avoid backfeeding the fault.

**Applications:** Hospitals, data centers, critical process plants.

---

## 4. Interconnected Switchboards (Busway)

```text
T1 ── MLVS1 ===== MLVS2 ── T2
```

`=====` = Busway (busbar trunking)

Two (or more) separate switchboards connected by a busway. Power can flow in either direction depending on the operating condition.

**Normal operation:** Each transformer feeds its own switchboard. The busway carries minimal current.

**Failure mode:** If T1 fails, the busway carries power from MLVS2 (fed by T2) back to MLVS1. The busway rating must be adequate for this reverse feed.

**Advantages:**
- Flexible distribution — loads can be added at either switchboard.
- Easier expansion — additional switchboards can be added along the busway.
- One transformer can support both switchboards during a contingency.

**Disadvantages:**
- Higher installation cost than a single switchboard.
- Protection coordination requires directional overcurrent relays — fault current direction changes depending on the source.

**Applications:** Large factories, industrial plants, airports, campus installations.

---

## 5. LV Ring

```text
      SB1 ------ SB2
       |          |
       |          |
      SB4 ------ SB3
```

Instead of one path to each switchboard, there are two possible paths. This is the LV equivalent of a ring main.

### Comparison to Radial

A radial feeder from a central switchboard has a single path to each downstream board. A cable fault between SB1 and SB2 leaves SB2 and SB3 without supply.

In a ring configuration, a cable fault between SB1 and SB2 means power travels the opposite way around the ring (SB1 → SB4 → SB3 → SB2). No switchboard loses supply.

### Operating Practice

The ring is often operated with one **Normally Open Point (NOP)** to maintain radial protection logic. The NOP is typically at the midpoint of the ring. During a fault, the affected section is isolated and the NOP is closed to restore supply to all loads.

### Advantages

- Excellent reliability. No single cable failure disconnects any load.
- Maintenance on any cable section can be performed without a complete shutdown — the section is isolated and the ring is reclosed on the other side.
- Good for long-distribution sites where running dual independent radial feeders would be more expensive due to additional cable length.

### Disadvantages

- More cabling than a radial configuration.
- Protection coordination is more complex — directional overcurrent is required, and fault current levels are different depending on where on the ring the fault occurs.

**Applications:** Large industrial plants, refineries, utility distribution networks, university campuses.

---

## 6. Double-Ended Supply

```text
Utility A          Utility
     │                │
     │               ATS
     │                │
 Main LV Bus       Loads
     ▲                ▲
     │                │
Utility B          Generator
```

Two independent power sources feeding the same bus, with only one source active at a time. An Automatic Transfer Switch (ATS) monitors the active source and transfers to the alternate source upon failure.

**Configurations:**
- Utility A + Utility B (two independent grid feeds)
- Utility + Generator (grid primary, generator backup)
- Utility + UPS (grid primary, UPS for no-break transfer)

**Failure operation:** If the active source fails, the ATS disconnects it, verifies the alternate source is healthy, then connects it. Transfer time depends on the ATS type (open transition: 1-10 cycles; closed transition: no break).

### Advantages

- Very high availability — two completely independent sources.
- Supports critical loads (life safety, data center, surgical).
- Can be combined with any of the above topologies at the load level.

### Disadvantages

- Highest cost — duplicate sources, switchgear, cabling.
- More equipment and floor space required.
- Requires transfer logic and regular testing of the alternate source.

**Applications:** Hospitals, data centers, emergency services, critical infrastructure.

---

## Comparison

| Configuration | Redundancy | Normal Paths | Transfer Mechanism |
|---------------|------------|--------------|--------------------|
| Single Feeder | None | 1 | None |
| Parallel Transformers | Medium | Shared bus | Remaining transformer carries all |
| Split Bus (NO Coupler) | High | Independent buses | Close bus coupler |
| Interconnected Busways | High | Independent + link | Feed through busway |
| LV Ring | Very High | Two cable paths | Open NOP, feed from other side |
| Double-Ended Supply | Very High | Two independent sources | ATS changes source |

## Selection Guide

| If you need... | Start with... |
|----------------|---------------|
| Lowest cost, no critical loads | Single feeder |
| Capacity + some redundancy | Parallel transformers |
| High availability, maintenance without shutdown | Split bus |
| Flexible expansion across a site | Interconnected busways |
| No single cable failure to drop loads | LV Ring |
| Two independent sources for life-safety | Double-ended supply |

**Trap:** Topology choice must be integrated with protection coordination (discrimination, arc flash) and harmonic management (see [[harm-m3-triplen-propagation]] for how triplen harmonics propagate through different configurations). A split bus with an open coupler, for example, naturally limits triplen harmonic circulation between sections — a double-ended supply may not.
