---
tags:
  - flashcards/eee/motors
source: "Motors — Module Map (Notion)"
---

#type/cloze
Text: The 3-phase squirrel cage induction motor accounts for approximately {{c1::80%}} of motors encountered in industrial and commercial practice.
Extra: This is why Module 1 is the foundation — everything else builds on it.

---

#type/cloze
Text: A motor at standstill draws {{c1::6–8×}} its full-load current at the moment of starting.
Extra: This inrush current drives fuse selection, cable sizing, contactor ratings, and protection relay settings.

---

#type/basic
Front: Star-Delta starting reduces inrush current to what fraction of DOL inrush? What is the tradeoff?
Back: 1/3 of DOL inrush. The tradeoff: starting torque is also reduced to 1/3 (because torque is proportional to voltage squared, and star connection reduces voltage by √3).

---

#type/cloze
Text: Single-phase induction motors are {{c1::not self-starting}} because a single phase does not produce a rotating magnetic field.
Extra: Various starting mechanisms solve this: capacitor-start, split-phase, shaded pole.

---

#type/basic
Front: What is the #1 cause of motor burnout in practice?
Back: Single phasing (phase loss). Standard overload relays may not catch it reliably.

---

#type/basic
Front: What are the four layers of motor protection and what does each protect against?
Back: MCP/MCCB → short circuit; thermal overload relay → overcurrent/heating; thermistors → winding temperature; RCD → earth fault. Each protects against a different failure mode.

---

#type/cloze
Text: A synchronous motor can be over-excited to act as a {{c1::capacitor bank}}, supplying reactive power to the grid for power factor correction.
Extra: This is a major reason large industrial facilities install synchronous motors.

---

#type/basic
Front: Why are DC motors still used in modern installations despite AC dominance?
Back: Lifts/elevators, traction systems (trains, EVs), and some precision industrial drives. The commutator is their defining feature and main maintenance liability.

---

#type/cloze
Text: The module sequence for motors mirrors the SLD design workflow: identify motor type → determine starting method → specify protection → {{c1::verify with testing}} → diagnose faults.
Extra: This is exactly how motor circuits appear on the SLD.

---

#type/basic
Front: What does VFD stand for, and why is it increasingly replacing other starting methods?
Back: Variable Frequency Drive. It provides both starting current reduction AND speed control, making it the modern answer to motor starting and operation.

---

#type/cloze
Text: For a VFD-fed motor, common fault issues include {{c1::bearing currents}}, cable length limitations, and {{c2::harmonic heating}}.
Extra: These are VFD-specific problems that don't occur with direct-on-line operation.
