---
type: topic
tags: [eee, relays, contactors, schematics]
created: 2026-06-01
status: building
parent: "[[MOC — Electrical Installation]]"
sources:
  - "[[BMS Controls Training — 6hr Video]]"
  - "[[Upmation — How to Read Electrical Diagrams]]"
---

# Reading Relay Schematics

## The Coil

A relay coil is drawn as a **box** with two terminals:

- **A1** — positive (or line) side
- **A2** — negative (or neutral) side

A1/A2 + box = this is the coil side. The coil voltage must match the control voltage (e.g., 24V AC coil for a 24V AC system).

When the coil energizes, it creates a magnetic field that actuates all contacts associated with that relay.

## Contacts

### NO (Normally Open)

Drawn with a **gap** in the line. Circuit is broken until the relay energizes. When energized, the contact closes and current flows.

### NC (Normally Closed)

Drawn with **no gap** — the line appears continuous. Circuit is complete until the relay energizes. When energized, the contact opens and current stops.

### Multiple Poles

One relay can drive multiple contacts. Each pole is a separate switch actuated by the same coil. A relay with 2 poles is labeled e.g., R1/1 and R1/2 (relay 1, pole 1 and pole 2).

## The Parent-Child Relationship

When the same relay (say K1) appears in multiple places on a schematic — the coil on one page, a NO contact on another, an NC contact on a third — they are all **the same physical device**. The label K1 is what connects them.

This is what makes relay logic readable: the label tells you "all of these are actuated by the same coil."

## Contactor vs Relay

Both are electrically operated switches. The distinction:

| | Relay | Contactor |
|--|-------|-----------|
| Typical use | Control circuits, low current | Power circuits, motor loads |
| Physical size | Small | Larger, with arc suppression |
| Contact rating | Low (signal level) | High (motor current) |

On a schematic, the symbols are similar but contactors often have additional notation for overload protection.

## Nomenclature

Label conventions are **drawing-specific** — always check the legend. Common prefixes:

- **-KA** = relay
- **-KM** = contactor
- **-K** = generic (relay or contactor, depends on the drawing)

The same physical symbol can mean different things depending on the nomenclature defined in that document.

[[https://www.kynix.com/Blog/how-does-a-dpdt-relay-work.html]]


1. **Poles**
    
    **Pole = the number of separate circuits a relay can control.** Think of it as how many independent switches are bundled into one relay, all actuated by the same coil.
    
    - **1 pole (single pole):** Controls one circuit. One common, one set of contacts.
    - **2 poles (double pole):** Controls two independent circuits simultaneously. Two commons, two sets of contacts. This is what every relay in your project uses.
    - **4 poles (quad pole):** Four independent circuits. Less common in BMS, more in industrial.
    
    **Why 2 poles in this project?** Pole 1 drives the visible stuff (lights on the panel). Pole 2 feeds the PLC. Same relay, two purposes, one coil. Clean design.
    
2. **Throw = the number of positions each pole's contact can connect to.** How many output paths from the common terminal.
    
    - **Single throw (ST):** One output path. The contact either connects or doesn't. That's it. ON or OFF.
    - **Double throw (DT):** Two output paths. The common can connect to position A (NC) OR position B (NO). This gives you a changeover capability.
    
    ### The Four Types
    
    | Type | Full Name | Contacts | What it does | |------|-----------|----------|--------------| 
    | **SPST** | Single Pole Single Throw | 1 common → 1 contact | Simple ON/OFF switch. One circuit, either connected or not. | 
    | **SPDT** | Single Pole Double Throw | 1 common → NC + NO | Changeover. Common swings between two paths. The "Form C" contact. | 
    | **DPST** | Double Pole Single Throw | 2 commons → 2 contacts | Two circuits switch ON/OFF together. Like two SPSTs with one coil. | 
    | **DPDT** | Double Pole Double Throw | 2 commons → 2×(NC + NO) | Two independent changeover switches, one coil. The workhorse. |

![[Pasted image 20260602084540.png]]
