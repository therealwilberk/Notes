---
type: topic
tags: [eee, circuit-numbering, wire-tags, conventions]
created: 2026-06-01
status: building
parent: "[[MOC — Electrical Installation]]"
sources:
  - "[[BMS Controls Training — 6hr Video]]"
  - "[[Upmation — How to Read Electrical Diagrams]]"
---

# Circuit Numbering & Wire Tags

## Wire Numbers

Every node in a circuit gets a unique number. These are **wire numbers** — they identify the electrical connection point, not the physical wire.

### The Rule

Wire numbers increment sequentially down the schematic. A change in number means a component sits between those two points.

```
120 → [Start Button] → 121 → [Contactor Coil] → 0V
```

The Start button separates node 120 from node 121. If tracing a wire with number 120, it runs from the MCB output down to one side of the Start button. The other side of the button is 121.

### Two Purposes

1. **Tracing** — follow a circuit across multi-page documents. Same number at both ends = same electrical node.
2. **Building** — tells the panel builder exactly which wires to connect to which terminals.

## Circuit Numbering (by MCB)

> [!important] The numbering rule
> Circuits are numbered based on which MCB they originate from. The number changes every time the circuit passes through a device.

- **100 circuit** = everything directly from MCB 1, before any device
- Once it passes through a device → becomes a new number (e.g., 400, 200)
- Example: 24V from MCB → through lamp test push button → now it's the **400 circuit**

This is how you know *which MCB* feeds a given circuit just by looking at the number.

## Wire Tags

Each physical wire has a tag — a label attached to the wire. If a wire comes loose during installation or maintenance, the tag tells you exactly where it goes by looking it up on the diagram.

Panels built without proper wire tags are a nightmare to troubleshoot. This is a build quality indicator — if you open a panel and see no wire tags, expect other problems.

## Device Tags

Devices inside the panel also have tags. A device can be physically located in the panel using the tag shown on the drawing. The tag is the link between the schematic and the physical hardware.
