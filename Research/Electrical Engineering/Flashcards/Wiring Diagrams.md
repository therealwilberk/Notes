---
tags: [flashcards/eee/wiring-diagrams]
source: "[[Reading Electrical Diagrams]]", "[[Wiring Diagram Reading — Notes]]"
---

## IEC Reference Designations

What does the letter F represent in IEC reference designations?::Protective device (fuse, MCB, MCCB)
What does the letter K represent in IEC reference designations?::Contactor or relay
What does the letter M represent in IEC reference designations?::Motor
What does the letter Q represent in IEC reference designations?::Isolator / disconnector
What does the letter S represent in IEC reference designations?::Switch or push button
What does the letter H represent in IEC reference designations?::Indicator lamp
What does the letter R represent in IEC reference designations?::Resistor
What does the letter T represent in IEC reference designations?::Transformer

What would the designation K1 mean on an IEC schematic?::Main contactor
What would the designation F1 mean on an IEC schematic?::Main MCB
What would the designation S1 and S2 typically represent?::S1 = stop button, S2 = start button
What would the designation H1 mean on a motor control schematic?::Run lamp (indicator)

## Diagram Types

{{c1::Schematic / Elementary diagrams}} show logical circuit operation using IEC symbols — used for design and understanding.
{{c1::Wiring diagrams}} show physical connections, terminal numbers, actual wire routing — used for installation and panel building.
{{c1::Single Line Diagrams (SLD)}} show power distribution with one line per phase — used for supply design and transformer sizing.

The schematic and wiring diagram are companions — the schematic shows {{c1::the logic}}, the wiring diagram shows {{c1::how to physically build it}}.

## Wire Numbering

What are the two purposes of wire numbers on a schematic?::Tracing circuits across multi-page documents, and telling panel builders which wires connect to which terminals
What does a change in wire number between two points indicate?::A component exists between those two points
Wire numbers increment {{c1::sequentially}} down the schematic (e.g. 120 → 121 → 122).
The same wire number appears at {{c1::both ends}} of every wire connecting two points.

## Cross-Referencing

What does the cross-reference format "page.column" mean? For example, "2.0"::Page 2, column 0 (first column)
Where is the cross-reference information for a coil's contacts typically shown on a schematic?::Below the coil — lists all contacts belonging to that coil with their page.column addresses
Where is the cross-reference for a contact's driving coil shown?::Below the contact — shows where the coil lives

## De-energized Convention

All contacts on a schematic are shown in their {{c1::de-energized / neutral}} state.
In the de-energized state, NC contacts appear {{c1::closed}} and NO contacts appear {{c1::open}}.

## IEC vs NEMA

Which standard does Kenya use — IEC 60617 or ANSI/IEEE 315?::IEC 60617
In IEC symbols, a contactor coil is drawn as a {{c1::rectangle with diagonal lines}}. In NEMA, it's drawn as a {{c1::circle}}.
In IEC symbols, resistors use {{c1::rectangles}}. In NEMA/IEEE, they use {{c1::zigzag lines}}.

## Practical Reading

What should always be found first when reading a wiring diagram?::The legend and abbreviation page
What is the standard reading direction for a wiring diagram?::Left to right, top to bottom (but always verify — designers sometimes break this)
What is a "wire tag" on a wiring diagram?::A unique number on each wire that identifies it — used to trace connections and locate where loose wires belong
What are double-level terminal blocks?::Terminal blocks with the same footprint as standard but allowing two wires per side — used to save panel space
What does the designation -KA typically represent?::A relay (not a contactor)
