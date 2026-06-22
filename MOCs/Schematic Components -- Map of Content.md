---
type: moc
tags: [moc, eee, schematic, components]
aliases: ["Schematic Components", "SC MOC"]
created: 2026-06-17
status: complete
parent: "[[Power Electronics -- Map of Content]]"
---

# Schematic Components — Map of Content

Reference notes on electrical subcomponents and devices that appear in schematic diagrams and control panels. Each module covers operating principles, schematic symbols, selection criteria, common traps, and driving/wiring circuits.

> **How to use**: New to a component? Read the *Thinking Pattern* box first — it gives the mental model. The *mermaid diagrams* show relationships and decision trees. *Traps* are failure modes that catch experienced engineers too.

## Modules

| Module | What it covers | Key mermaid | Thinking pattern |
|--------|---------------|-------------|------------------|
| [[Notes/EEE/Schematic Components/sc-relays\|Relays]] | Poles/throws, Form A/B/C, relay types, coil drive & suppression, arc suppression, datasheet parameters | Relay type selection flowchart | "A relay is a remote-controlled switch — coil and contacts are electrically isolated" |
| [[Notes/EEE/Schematic Components/sc-contactors\|Contactors & Motor Starters]] | Relay vs contactor, arc chutes, shading ring, IEC vs NEMA, utilisation categories, OL relay types, trip classes, starter configurations | Trip class selection, contactor vs relay decision | "A contactor is a relay built for high current. A motor starter is a contactor + overload relay" |
| [[Notes/EEE/Schematic Components/sc-solenoids\|Solenoids & Linear Actuators]] | Force-stroke characteristic, AC vs DC, shading ring trap, duty cycle, proportional solenoids, driving circuits | AC vs DC solenoid decision, force-stroke curve | "A solenoid is a coil that pulls metal — force drops off as 1/x²" |
| [[Notes/EEE/Schematic Components/sc-circuit-protection\|Circuit Breakers & Fuses]] | Fuse types (gG/aM/aR), MCB trip curves (B/C/D/K/Z), MCCB LSIG, ACB, RCD types, selectivity | Fuse type selection, RCD type selection | "Protection devices protect the wiring, not the load — the OL relay protects the load" |
| [[Notes/EEE/Schematic Components/sc-transformers\|Control & Signal Transformers]] | Control transformer sizing, CT principles & saturation, VT/PT, pulse transformer V·µs, current sense transformer | CT wiring safety, CT selection, control transformer sizing | "A transformer couples through magnetic fields — CTs are current sources, never open the secondary" |
| [[Notes/EEE/Schematic Components/sc-switches-indicators\|Switches, Buttons & Indicators]] | Contact forms, pushbuttons, E-stop circuit, selector switches, limit switches, pilot lights, buzzers, stack lights | E-stop circuit, contact form states, stack light pattern, ghost voltage trap | "A switch is a mechanical gate — drawn in its rest (unactuated) position" |
| [[Notes/EEE/Schematic Components/sc-terminals\|Terminals & Connectors]] | Connection technology (screw/spring/push-in/stud), terminal block types, DIN rail, pluggable connectors, wire ferrules, IDC | Technology selection flowchart | "A terminal block is a structured junction — wire in, connection out, with organisation and serviceability" |
| [[Notes/EEE/Schematic Components/sc-diagram-types\|Diagram Types]] | Ladder, SLD, connection, block — what each communicates, when to use each, how to identify at a glance | Diagram identification flowchart | "A diagram type is defined by what it's meant to communicate — never read one expecting the other's job" |
| [[Notes/EEE/Schematic Components/sc-symbols-labels\|Symbols, Labels & Reference Codes]] | IEC 81346 letter codes (K, Q, F, S, M...), NEMA/ANSI equivalents, terminal numbering on relays/contactors/breakers, wire numbering conventions | Reference code table, terminal numbering diagram | "Every label tells you what a component DOES (letter code) and which instance it is (number)" |
| [[Notes/EEE/Schematic Components/sc-reading-ladder\|Reading Ladder Diagrams]] | Power vs control split, tracing logic top-to-bottom, using cross-references, series=AND/parallel=OR, traps (de-energised state, mechanical interlocks) | Tracing flowchart, power/control split layout | "Every ladder has power and control sections — learn to separate them and you'll never be lost" |
| [[Notes/EEE/Schematic Components/sc-iec-nema\|IEC vs NEMA Standards]] | Symbol differences, terminal numbering, coil/contact drawing conventions, geography of each standard, mixed-schematic survival tips | Geography map, terminal comparison | "IEC and NEMA are different dialects of the same language — the logic is identical, only the symbols change" |
| [[Notes/EEE/Schematic Components/sc-cheatsheet\|Schematic Decode Method]] | The 6-step method: identify type → find source → separate power/control → decode labels → trace one load → work backwards. Wire numbering, circuit state traps, common mistakes | 6-step flowchart, SLD/ladder/power/control reading order diagrams | "Schematics are a language with a grammar — the method is always the same, only the application changes" |

## Related

See [[Power Electronics -- Map of Content]] for power conversion circuits (converters, inverters, magnetics design) that use these components.
See [[Notes/EEE/Wiring-scale AutoCAD]] for panel layout drawings and schematic drafting.
