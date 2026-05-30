---
tags:
  - flashcards/eee/wiring-diagrams
source: "[[Reading Electrical Diagrams]], [[Wiring Diagram Reading — Notes]]"
---

#type/basic
Front: What does the letter F represent in IEC reference designations?
Back: Protective device (fuse, MCB, MCCB)
---
#type/basic
Front: What does the letter K represent in IEC reference designations?
Back: Contactor or relay
---
#type/basic
Front: What does the letter M represent in IEC reference designations?
Back: Motor
---
#type/basic
Front: What does the letter Q represent in IEC reference designations?
Back: Isolator / disconnector
---
#type/basic
Front: What does the letter S represent in IEC reference designations?
Back: Switch or push button
---
#type/basic
Front: What does the letter H represent in IEC reference designations?
Back: Indicator lamp
---
#type/basic
Front: What does the letter R represent in IEC reference designations?
Back: Resistor
---
#type/basic
Front: What does the letter T represent in IEC reference designations?
Back: Transformer
---
#type/basic
Front: What would the designation K1 mean on an IEC schematic?
Back: Main contactor
---
#type/basic
Front: What would the designation F1 mean on an IEC schematic?
Back: Main MCB
---
#type/basic
Front: What would the designation S1 and S2 typically represent?
Back: S1 = stop button, S2 = start button
---
#type/basic
Front: What would the designation H1 mean on a motor control schematic?
Back: Run lamp (indicator)
---
#type/basic
Front: What are the three main types of electrical diagrams and what does each show?
Back: Schematic (logic), Wiring (physical connections), SLD (power distribution). Schematic shows the logic, wiring shows how to build it, SLD shows supply design.
---
#type/basic
Front: What are the two purposes of wire numbers on a schematic?
Back: Tracing circuits across multi-page documents, and telling panel builders which wires connect to which terminals
---
#type/basic
Front: What does a change in wire number between two points indicate?
Back: A component exists between those two points
---
#type/basic
Front: What does the cross-reference format "page.column" mean? Example: "2.0"
Back: Page 2, column 0 (first column)
---
#type/basic
Front: Where is the cross-reference information for a coil's contacts shown on a schematic?
Back: Below the coil — lists all contacts belonging to that coil with their page.column addresses
---
#type/basic
Front: Where is the cross-reference for a contact's driving coil shown?
Back: Below the contact — shows where the coil lives
---
#type/basic
Front: Which standard does Kenya use for electrical symbols — IEC 60617 or ANSI/IEEE 315?
Back: IEC 60617
---
#type/basic
Front: What should always be found first when reading a wiring diagram?
Back: The legend and abbreviation page
---
#type/basic
Front: What is a "wire tag" on a wiring diagram?
Back: A unique number on each wire that identifies it — used to trace connections and locate where loose wires belong
---
#type/basic
Front: What are double-level terminal blocks?
Back: Terminal blocks with the same footprint as standard but allowing two wires per side — used to save panel space
---
#type/basic
Front: What does the designation -KA typically represent?
Back: A relay (not a contactor)
---
#type/cloze
Text: All contacts on a schematic are shown in their {{c1::de-energized / neutral}} state.
Extra: This means NC contacts appear closed and NO contacts appear open.
---
#type/cloze
Text: In the de-energized state, NC contacts appear {{c1::closed}} and NO contacts appear {{c1::open}}.
Extra: The de-energized convention is the starting point for reading any schematic.
---
#type/cloze
Text: Wire numbers increment {{c1::sequentially}} down the schematic (e.g. 120 → 121 → 122).
Extra: A change in number between two points means a component exists between them.
---
#type/cloze
Text: The same wire number appears at {{c1::both ends}} of every wire connecting two points.
Extra: This is how panel builders trace which terminal a loose wire belongs to.
---
#type/cloze
Text: In IEC symbols, a contactor coil is drawn as a {{c1::rectangle with diagonal lines}}. In NEMA, it's drawn as a {{c1::circle}}.
Extra: Kenya uses IEC, not NEMA.
---
#type/cloze
Text: In IEC symbols, resistors use {{c1::rectangles}}. In NEMA/IEEE, they use {{c1::zigzag lines}}.
Extra: IEC = clean geometric shapes. NEMA = more pictorial.
---
#type/cloze
Text: Schematic / Elementary diagrams show {{c1::logical circuit operation}} using IEC symbols — used for design and understanding.
Extra: Wiring diagrams show the physical counterpart.
---
#type/cloze
Text: Wiring diagrams show {{c1::physical connections, terminal numbers, actual wire routing}} — used for installation and panel building.
Extra: The schematic shows the logic; the wiring diagram shows how to physically build it.
---
#type/cloze
Text: Single Line Diagrams (SLD) show {{c1::power distribution with one line per phase}} — used for supply design and transformer sizing.
Extra: SLD is the starting point for any electrical installation design.
---
#type/basic
Front: What is the standard reading direction for a wiring diagram?
Back: Left to right, top to bottom (but always verify — designers sometimes break this)
