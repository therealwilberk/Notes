---
type: topic
tags: [eee, panel-layout, wiring-diagrams]
created: 2026-06-01
status: building
parent: "[[MOC — Electrical Installation]]"
sources:
  - "[[BMS Controls Training — 6hr Video]]"
  - "[[Upmation — How to Read Electrical Diagrams]]"
---

# Panel Layout & Structure

## The Divider Line

Every page of a schematic has a **horizontal line** separating two zones:

- **Above the line** — equipment *inside* the panel (breakers, relays, terminal blocks, transformers)
- **Below the line** — field equipment *outside* the panel (sensors, actuators, motors, push buttons)

This line is the single most important visual reference on any panel schematic. Everything above is what gets mounted in the enclosure. Everything below is what gets wired out to the plant.

## Schematic ≠ Physical Layout

How things are drawn on the schematic is **not** how they're physically arranged in the panel. A panel builder can wire things in any order, in any physical arrangement, as long as the electrical connections are correct. The schematic shows *function*, not *position*.

This matters when troubleshooting — don't assume the relay drawn at the top-left of the page is physically in the top-left of the panel.

## Not All Schematics Look the Same

Different designers, different software (EPLAN, AutoCAD Electrical, others), different layout preferences. The structure is the same but the visual style varies. This is why the **legend page** exists (see [[Cross-Referencing Multi-Page Diagrams]]).

## Reading Direction

Standard: **left to right, top to bottom** — like reading text.

But designers break this rule when it makes a better layout. Power might enter at the bottom of the page. Always check before assuming where signal flow starts.

## De-energized State

All contacts and devices are drawn in their **neutral, non-energized state**:

- **NC (normally closed)** contacts appear *closed* on the diagram
- **NO (normally open)** contacts appear *open* on the diagram

This is universal. Misreading this is one of the most common mistakes when tracing circuits — if a contact looks "closed" on paper, it only means the device is de-energized, not that current is flowing.
