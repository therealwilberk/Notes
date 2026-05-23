---
title: Reading Electrical Wiring Diagrams
tags: [electrical-engineering, wiring-diagrams, industrial-panels, troubleshooting]
created: 2026-05-23
---

# Reading Electrical Wiring Diagrams

This document summarizes key concepts and practical tips for reading and understanding electrical wiring diagrams, with a specific focus on industrial panel wiring diagrams.

## Introduction to Wiring Diagrams

Electrical wiring diagrams can range from simple single-page schematics (e.g., ceiling fan connections) to extensive multi-page documents (e.g., factory control panels).

### Key Characteristics:
- **Standards:** Vary by country.
- **Layouts:** Differ based on company and designer.
- **Software:** Often created using ECAD software like **EPLAN** or **AutoCAD Electrical**.

Initial analysis is crucial to familiarize oneself with the layout and symbols. This guide focuses on industrial panel wiring diagrams, but many principles apply universally.

## Core Components of a Wiring Diagram

Every wiring diagram typically includes:
- **Hardware Components**
- **Power Sources**
- **Ground Chassis**
- **Terminals**
- **Wires**
- **Numbers, Letters, and Nomenclatures**

## Understanding Symbols and Legends

The very first step in reading a wiring diagram is to become familiar with its symbols.
- Most diagrams include a **Legend and Abbreviation page** for this purpose.

### Common Symbols (Examples):
- **Three-phase AC electric motor** 
- **Solenoid valve** 
- **Contactor** (Coil and contacts) 

**Note:** Symbols may have minor differences depending on the ECAD software used (e.g., Fuse symbol in EPLAN vs. AutoCAD Electrical).

## Reading Direction and Layout
A general rule of thumb for standard wiring diagrams is to read:
- **Left to right**
- **Top-down**

However, designers may make exceptions for better layout. In such cases, the starting point might be different (e.g., from the bottom where power enters).
### Power Entry Example:
- Three-phase power enters the panel.
- Voltage and frequency depend on the country (e.g., 400V/50Hz in England/Austria vs. 480V/60Hz in the US).
- Power typically enters **terminal blocks** (e.g., "X0" terminal strip).
  - A **terminal strip** refers to a group of terminal blocks with the same voltage level or purpose.

## Circuit Protection and Neutral Condition

From terminal blocks, power often moves to a **three-pole circuit breaker** with thermal and short-circuit protection.

### Neutral Condition Rule:
- Wiring diagrams are drawn in the **neutral (non-energized) condition**.
- All contacts, contactors, circuit breakers, etc., are shown in their normal state.
  - A **normally-closed (NC) contact** will appear closed.
  - **Normally-open (NO) contacts** will appear open.

After manually closing the circuit breaker, power flows to **power distributor bars**, from which branches are taken.

## Wire Tags and Device Tags

- **Wire tags:** Numbers on wires that are crucial for troubleshooting. They help identify connection points if a wire becomes disconnected.
- **Device tags:** Labels for devices within the panel. These tags help locate the physical device in the panel if its function is unknown from the diagram.

### Example: Transformer Circuit
- A branch might go to a two-pole circuit breaker, then power a transformer.
- A transformer converts voltage (e.g., 400V to single-phase 230V) to feed receptacles, heaters, and fans.
- **"ST19" tag:** Refers to a thermostat for controlling a heater or fan based on temperature setpoints.
- **Earthing chassis:** And its branches are shown wherever needed.

## Page and Column Numbering

Numbers at the top of each page are **column numbers**, dividing the page into 10 columns.

### Usage:
- Column numbers, combined with page numbers, are used to address different devices, contacts, and terminal blocks across multiple pages.
- This system helps navigate complex diagrams and trace connections.

### Cross-referencing Examples:
- **Power source reference (e.g., "2.0"):** "2" refers to page two, "0" refers to the first column of page two.
- **Contact reference (e.g., "130.6"):** "130" refers to page 130, "6" refers to column six.
  - Example: A contact with tag **KA1306** on page 130, column 6, might be a relay coil.
  - **Nomenclature:** "-KA" often denotes a relay in this type of drawing (refer to the Legend page).

## Power Supply and Distribution

On page two, the mains power source feeds a **24-volt power supply** (e.g., 10 amps capacity).
- This 24V supply is then extended using **terminal blocks** to power various instruments, PLC cards, PLC CPUs, or other devices requiring 24V.

### Double-Level Terminal Blocks:
- Sometimes, **double-level terminal blocks** are used to save space. They occupy the same footprint as ordinary blocks but allow two wires to be connected to each side.

## Interlocks and Safety Relays

A branch delivering 24V power might go to another page (e.g., page 12, column zero) with **interlocks**.
- An **interlock** signifies a condition that must be met.

### Safety Relay Example (Page 130):
- A **safety relay** is used to protect personnel, materials, and machinery during operation.
- Designers must refer to the **datasheet** of such equipment to complete the wiring diagram accurately. This is a critical and unavoidable step.
- **Two channels** are typically connected to safety components (e.g., safety barriers).
- If an area is evacuated, these channels activate, causing **NO contacts to close**.
- This transfers voltage to the A1 connection of relay coils, energizing them.
- Consequently, the 13-14 NO contacts of the relays close, transferring 24V power to the intended destination (e.g., page 12, column zero).

## Next Steps

The next part of this series will cover reading and understanding **PLC (Programmable Logic Controller)** and **VFD (Variable Frequency Drive)** power and signal cabling and wiring.