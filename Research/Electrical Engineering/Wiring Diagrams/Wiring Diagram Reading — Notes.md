---
type: research
tags: [electrical-engineering, wiring-diagrams, learning-notes]
created: 2026-05-21
status: in-progress
parent: "[[MOCs/Motor Starter Design — Map of Content.md]]"
---




_Source: Upmation — How to Read Electrical Diagrams_

---
<iframe width="560" height="315" src="https://www.youtube.com/embed/GHhcyH99inE?si=ETElVsmGWNXOrNS7" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
## General

Wiring diagrams aren't universal — they change based on country (standards), company (layout preferences), and the software used (EPLAN, AutoCAD Electrical, etc.). 

They can range from a single page (ceiling fan wiring) to 200+ pages (industrial control panel). Same skill, different scale.

---

## Step 1 — Always Find the Legend Page First

Every proper wiring diagram should have a **legend and abbreviation page** — usually at the front. This is where all the symbols and nomenclature are defined for _that specific drawing_.

Important note: symbols can look slightly different depending on the software. A fuse in EPLAN looks different from a fuse in AutoCAD Electrical. The legend tells you what's what _for this document_. Don't assume.

---

## Reading Direction

Standard rule: **left to right, top to bottom** — like reading a book.

But designers break this when it gives a better layout. In the example shown, the power actually enters at the _bottom_ of the page, not the top. So always check before you assume where to start.

---

## Everything is Shown De-energized

All contacts, contactors, circuit breakers — drawn in their **neutral, non-energized state**. So:

- NC contacts appear closed on the diagram
- NO contacts appear open

This is standard. Never forget it — misreading this causes a lot of confusion when tracing circuits.

---

## Wire Tags

The numbers on individual wires aren't random — they're **wire tags**. Each wire has a unique tag.

Why it matters practically: if a wire comes loose during installation or maintenance, you look up the tag on the diagram and immediately know where it goes. Huge for troubleshooting. Panels built without proper wire tags are a nightmare to work on later.

Devices inside the panel also have tags — you can physically locate a device in the panel using the tag shown on the drawing.

---

## Column Numbers and Cross-Referencing

Each page is divided into **numbered columns** (the numbers at the top of the page). Used in combination with the page number to locate anything in the drawing.

Format: **page.column** — so "2.0" means page 2, column 0 (first column).

This is how cross-referencing works across pages:

- An arrow with a number next to it = "this wire/signal continues at page X, column Y"
- Below a coil = list of all the contacts belonging to that coil, with their page.column addresses
- Below a contact = where the coil driving it lives

You will constantly flip between pages on a real drawing. That's not a sign you're doing it wrong — that's just how multi-page schematics work.

---

## Terminal Strips

Groups of terminal blocks are given a **strip designation** (like X0, XC). The designation usually indicates a shared voltage level or function — all terminals in that strip carry the same voltage or serve the same purpose.

Interesting one: **double-level terminal blocks** — same footprint as standard terminals but you can connect two wires per side. Used to save panel space. Worth knowing they exist because they can look confusing on a diagram if you don't know what they are.

---

## Nomenclature (Component Labels)

The label convention is drawing-specific — always check the legend. In the example:

- **-KA** = relay (not a contactor)
- The prefix letters tell you the component type

Same physical symbol can mean different things depending on the nomenclature defined in that document. This is why jumping between different companies' drawings feels disorienting — the label system may be completely different.

---

## Design Note — Always Use Datasheets

When designing (not just reading), every component needs its datasheet consulted. The designer in the example had to reference the safety relay datasheet to complete the wiring correctly.

This is non-negotiable in professional work — assumptions about terminal layouts, connection sequences, or operating conditions will create faults that are very hard to trace later.

---

## The Cross-Referencing Habit

Reading a multi-page wiring diagram requires constantly jumping back and forth between pages — a coil on page 130 has contacts on page 2, which reference back to page 130. This is normal and intentional.

Build the habit of following references instead of trying to understand a single page in isolation. A page only makes full sense in the context of the pages it references.