---
type: topic
tags: [eee, iec, reference-designations, symbols, nema]
created: 2026-06-01
status: building
parent: "[[MOC — Electrical Installation]]"
sources:
  - "[[BMS Controls Training — 6hr Video]]"
  - "[[Upmation — How to Read Electrical Diagrams]]"
---

# IEC Reference Designations

## The System

Every component on an IEC schematic has a reference label made up of:

- **Function marker** — what it does (e.g., control circuit, power supply)
- **Location marker** — where it is (e.g., main switchboard, plant room)
- **Element marker** — the specific device (e.g., motor M1, relay K2)

## Letter Codes for Motor Control

| Letter | Device type | Example |
|--------|-------------|---------|
| **F** | Protective device (fuse, MCB, MCCB) | F1 = main MCB |
| **K** | Contactor or relay | K1 = main contactor, KT = timer relay |
| **M** | Motor | M1 = the motor |
| **Q** | Isolator / disconnector | Q1 = main isolator |
| **S** | Switch or push button | S1 = stop button, S2 = start button |
| **H** | Indicator lamp | H1 = run lamp |
| **R** | Resistor | R1 = starting resistor |
| **T** | Transformer | T1 = control transformer |

## The K1 Example

When K1 appears in three places on a schematic — the coil, a NO contact, and an NC contact — they are all the **same physical device**. The label K1 is what connects them. This parent-child relationship is fundamental to reading relay logic.

## IEC vs NEMA/IEEE

Two major standards:

| | IEC 60617 | ANSI/IEEE 315 |
|--|-----------|---------------|
| Used in | International (Kenya, UK, Europe, Asia) | North America |
| Contactor coil | Rectangle with diagonal lines | Circle |
| Resistor | Rectangle | Zigzag line |
| Motor | Circle with M | Similar |

**Kenya uses IEC.** When searching "motor control schematic" online, many results are NEMA style (North American). The symbols look different for the same components. Filter searches for IEC specifically.

## The Legend

Symbols can look slightly different depending on the software used (EPLAN, AutoCAD Electrical, etc.). The **legend page** of each drawing set defines what the symbols mean *for that specific document*. Always check it first. Don't assume.
