---
type: topic
tags: [eee, power-distribution, mcb, busbar]
created: 2026-06-01
status: building
parent: "[[MOC — Electrical Installation]]"
sources:
  - "[[BMS Controls Training — 6hr Video]]"
---

# Power Distribution

> [!example] From the BMS panel
> Single phase, 50Hz, 230V supply entering the panel. The chain: supply → isolator → busbar → MCBs → loads. This section covers the 230V (mains) side of the panel.

## The Distribution Chain

```
Supply (230V, 50Hz, single phase)
  → Isolator switch (handle on outside, shaft into disconnector inside)
    → Busbar (distributes to all MCBs)
      → MCB 2 (D-type, 6A) → transformer primary
      → MCB 3 → auxiliary socket
      → MCB 4 → field equipment (via terminal blocks)
```

## Isolator Switch

The main disconnect. Handle is on the outside of the panel door, shaft goes through to a disconnector switch mounted inside. Provides a visible break for maintenance — not just electrical isolation but physical confirmation that the panel is dead.

## Busbar Distribution

From the isolator, a **busbar** feeds all MCBs. Same principle as a domestic consumer unit. The busbar is a common conductor (usually copper strip) that all MCBs tap off. Neutral runs via a separate **neutral block**.

Cable sizing: typically 10mm from main isolator to busbar and first MCB.

## MCB Selection

MCBs are chosen based on the load characteristics:

| Type | Use case |
|------|----------|
| **B-type** | Resistive loads (heaters, lighting) |
| **C-type** | General purpose, moderate inrush |
| **D-type** | High inrush current (motors, transformers, transformers) |

The BMS panel used a D-type 6A for the transformer primary — D-type because transformers have high inrush current at switch-on.

## Field Equipment Isolation

All field equipment should have a **local isolator** as well. This allows maintenance on individual devices without shutting down the entire panel.

## Key Principle

Every circuit leaves the panel through a **terminal block**. The terminal block is the boundary between panel wiring and field wiring. This separation is critical for fault-finding — if voltage is present at the terminal block but not at the field device, the fault is in the field wiring.


- 0v supply (neutral) use case in controls:
- 