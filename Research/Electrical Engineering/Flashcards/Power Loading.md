---
tags:
  - flashcards/eee/power-loading
source: "Power Loading of an Installation (Notion)"
---

#type/cloze
Text: The utilization factor (ku) for industrial motors is typically {{c1::0.75}}.
Extra: Motors rarely run at full nameplate load in practice.

---

#type/cloze
Text: The utilization factor (ku) for incandescent lighting is {{c1::1.0}} because the lamp always operates at full load.
Extra: ku = 1.0 is also mandatory for EV charging and UPS loads.

---

#type/cloze
Text: The utilization factor (ku) for EV charging is {{c1::1.0}} — it cannot be assumed to operate below nameplate.
Extra: Same applies to safety circuits and UPS loads.

---

#type/basic
Front: What is the formula for motor input power given shaft output power and efficiency?
Back: P_input = P_shaft / η (efficiency)

---

#type/basic
Front: A 7.5kW motor has efficiency 0.89 and PF 0.83. What are the input kW and kVA?
Back: P_input = 7.5 / 0.89 = 8.43 kW; S = 8.43 / 0.83 = 10.15 kVA

---

#type/cloze
Text: The diversity factor in common engineering practice means the {{c1::coincidence factor (≤ 1)}}, NOT the IEC reciprocal definition (≥ 1).
Extra: When someone says ks = 0.8, they mean 80% coincidence. The IEC reciprocal is technically correct but rarely used. This is a classic exam trap.

---

#type/basic
Front: What is the IEC definition of coincidence factor vs diversity factor?
Back: Coincidence factor = simultaneous demand / sum of individual demands (≤ 1). Diversity factor = reciprocal (≥ 1). In practice, "diversity factor" usually means the coincidence factor.

---

#type/basic
Front: What is the formula for maximum demand of an installation?
Back: P_max,demand = Σ(Pn × ku) × ks; then S_max,demand = P_max,demand / cos φ

---

#type/cloze
Text: For socket outlets in offices, the typical diversity factor (ks) is {{c1::0.1}}.
Extra: Compare to lighting (1.0), heating/AC (1.0), motors industrial (0.75), lifts (0.2).

---

#type/cloze
Text: For an apartment block with ≥35 consumers (no electric heating), the diversity factor (ks) is approximately {{c1::0.41}}.
Extra: From French standard NFC14-100, widely referenced in IEC guidance.

---

#type/cloze
Text: Transformer selection requires a growth margin of {{c1::20–25%}} above the calculated maximum kVA demand.
Extra: Then select the next standard IEC 60076 rating above that figure.

---

#type/basic
Front: What are the standard IEC 60076 transformer kVA ratings?
Back: 100, 160, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000 kVA

---

#type/basic
Front: Maximum demand is 680 kVA. What transformer rating should be selected?
Back: 680 × 1.20 = 816 kVA → next standard size = 1000 kVA (800 kVA leaves insufficient margin).

---

#type/cloze
Text: The design calculation sequence for power loading is: load characteristics → installed kW → installed kVA → {{c1::maximum kVA demand (applying ku and ks)}} → transformer rating.
Extra: Each step feeds the next. Getting maximum demand wrong makes everything downstream wrong.

---

#type/cloze
Text: For LED lighting, the power factor of quality commercial drivers is typically {{c1::0.90–0.95}}, while emergency/budget drivers can be as low as {{c2::0.5–0.7}}.
Extra: Always use driver input wattage, not lamp lumen wattage.

---

#type/basic
Front: Why is the sum of all nameplate ratings a poor basis for supply sizing?
Back: Actual demand is typically 40–60% lower due to utilization factors (ku) and diversity (ks). Sizing against nameplate sum wastes money and over-engineers the installation.

---

#type/cloze
Text: The load schedule is the core {{c1::design deliverable}} that feeds cable sizing, protection device selection, and transformer specification.
Extra: Phase 8 of the Savanna House SLD project produces exactly this.
