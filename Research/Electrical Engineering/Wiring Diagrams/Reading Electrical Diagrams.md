---
type: research
tags: [electrical-engineering, wiring-diagrams, symbols]
created: 2026-05-21
status: complete
parent: "[[MOCs/Motor Starter Design — Map of Content.md]]"
---


## The Actual Gap

Power engineering curricula teach SLDs — single line diagrams for distribution systems. They don't teach **IEC schematic sets** — the multi-page document format used for motor control panels, machine wiring, and industrial installations. These are different skills. The second one is being learned by doing, which is why some fundamentals feel unfamiliar.

The five things to build:

---

### 1. The Four Diagram Types and What Each Does

A schematic diagram illustrates the logical connections and functionality of components in a circuit using standardized symbols, focusing on how the circuit works electrically. A wiring diagram depicts the physical layout and actual wire connections between components, often showing their relative positions and how they should be physically assembled or wired. Schematics prioritize electrical function, while wiring diagrams prioritize physical construction.

In practice for motor control work, three are relevant:

| Type                               | What it shows                                               | When to use it                                    |
| ---------------------------------- | ----------------------------------------------------------- | -------------------------------------------------- |
| **Single Line Diagram (SLD)**      | Power distribution, one line per phase                      | Supply design, transformer sizing                  |
| **Schematic / Elementary diagram** | Logical circuit operation, IEC symbols                      | Design and understanding — what's being drawn now |
| **Wiring diagram**                 | Physical connections, terminal numbers, actual wire routing | Installation and panel building                    |

The schematic and wiring diagram are companions — the schematic shows the logic, the wiring diagram shows how to physically build it. Both need to be readable.

---

### 2. IEC Reference Designation System

Every component on an IEC schematic has a reference label. Each element is marked according to its function, location, and product type. The function marker defines the function (e.g. control circuits, 24VDC power supply), the location marker defines the location (e.g. main switchboard), and the element marker identifies the target device (e.g. motor -M1, relay -K2).

The letters for motor control work:

|Letter|Device type|Example|
|---|---|---|
|**F**|Protective device (fuse, MCB, MCCB)|F1 = main MCB|
|**K**|Contactor or relay|K1 = main contactor, KT = timer relay|
|**M**|Motor|M1 = the motor|
|**Q**|Isolator / disconnector|Q1 = main isolator|
|**S**|Switch or push button|S1 = stop button, S2 = start button|
|**H**|Indicator lamp|H1 = run lamp|
|**R**|Resistor|R1 = starting resistor|
|**T**|Transformer|T1 = control transformer|

When K1 appears in three places on a schematic — the coil, a NO contact, and an NC contact — they are all the same physical device. The label K1 is what connects them. This is the parent-child relationship that was confusing with "multiple contactors."

---

### 3. Wire Numbering

The numbers on a reference diagram (120, 121, 122, 123, 130) are **wire numbers** — every node in the circuit gets a unique number. Understanding line reference and sequential device and wire numbering systems is fundamental to reading industrial motor control diagrams.

Wire numbers serve two purposes: tracing a circuit across a multi-page document, and telling a panel builder exactly which wires to connect to which terminals. The convention:

- Numbers increment sequentially down the schematic (120 → 121 → 122)
- The same number appears at both ends of every wire connecting two points
- A change in wire number = a component between those two points

This is why the reference diagram showed 120 above the Start button and 121 below it — the Start button separates those two nodes.

---

### 4. Cross-Referencing (Across Pages)

In more complex systems, diagrams often span several pages, with cross-references showing the location of the next part of the connection.

On a real multi-page schematic set, when the K1 coil appears on page 3 and its contacts appear on page 5, a cross-reference notation tells where to find them. Standard IEC practice shows the page and column reference next to every contact symbol. For single-page drawings, this doesn't apply yet — but it's what makes large industrial schematics readable and is fundamental to know before encountering them.

---

### 5. IEC vs NEMA/IEEE — Know Which World You're In

The two most common standards are IEC 60617 (international, often uses rectangles for passives) and ANSI/IEEE 315 (historically North American, often uses zigzag lines for resistors).

Kenya, East Africa, and the UK-influenced engineering traditions all use IEC 60617. The NEMA/IEEE symbols look different for the same components. When searching "motor control schematic" online, many results are NEMA style (North American). The symbols will look wrong because they are from a different standard. Filter searches for IEC specifically.

Practical differences:

- **Contactor coil:** IEC = rectangle with diagonal lines; NEMA = circle
- **NO contact:** IEC = two short lines with a gap; NEMA = similar but layout differs
- **Motor:** IEC = circle with M; NEMA = similar
- **Overload relay:** IEC = rectangle with thermal element notation; NEMA = different symbol

---

## Resources — Ranked by ROI 

### 1. Upmation — Free, Start Here

**`upmation.com/wiring-diagrams`**  [[Wiring Diagram Reading — Notes]]

---

### 2. ControlByte — Free Deep Dive on IEC Conventions

**`controlbyte.tech/blog/how-to-read-electrical-wiring-diagram`**

https://controlbyte.tech/blog/how-to-read-electrical-wiring-diagram/

---

### 3. WiredWhite — "Basic Electrical Controls & Diagram Reading"

**`wiredwhite.com/courses/basic-electrical-controls-diagram-reading`**

Covers exactly what the project requires — DOL, reversing starters, soft starters, VFDs — in IEC format. Worth paying for if the price is reasonable. Check the site directly for current pricing.

---

### 4. Udemy — "Introduction to Electrical Controls & Diagram Reading"

Covers DOL starters, reversing controllers, soft starters, VFDs, wire numbering. Udemy courses go on sale constantly — often $10–15. Check during a sale.

---

## The Learning Order

Don't try to learn everything before finishing the project. This sequence works:

1. Watch the **Upmation YouTube video** today — 20 minutes, gives the IEC reading framework
2. Read the **ControlByte article** for the reference designation and wire numbering conventions — apply immediately to Drawing 1 (add wire numbers, fix device labels to K1/F1/M1 format)
3. Finish drawings 2 and 3 applying what's been learned
4. Take the **WiredWhite or Udemy course** after the project — it'll make far more sense once the circuits have been drawn

The project is the best learning context. Reading about schematics before drawing them is half as effective as reading while actively drawing them.
