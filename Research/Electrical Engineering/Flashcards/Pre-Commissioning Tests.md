---
tags:
  - flashcards/eee/pre-commissioning
source: "Pre-Commissioning Electrical Tests (Notion)"
---

#type/cloze
Text: IEC 60364-6 mandates that {{c1::visual inspection}} must be performed before any testing begins.
Extra: A test result is meaningless if the installation hasn't been visually confirmed safe to energise. This is the most commonly skipped step.

---

#type/cloze
Text: For LV circuits up to 500V (including 230/400V systems), the insulation resistance test uses {{c1::500V DC}} test voltage with a minimum of {{c2::1.0 MΩ}}.
Extra: SELV/PELV circuits use 250V DC with 0.5 MΩ minimum. Circuits above 500V use 1000V DC with 1.0 MΩ minimum.

---

#type/basic
Front: What sensitive equipment must be disconnected before insulation resistance testing, and why?
Back: SPDs, VFDs, electronic ballasts, capacitors, and semiconductor-based equipment. The 500V/1000V DC test voltage will destroy semiconductor components. This is the most common commissioning mistake.

---

#type/cloze
Text: Insulation resistance halves approximately every {{c1::10°C}} rise in temperature.
Extra: Always record ambient temperature with the test result.

---

#type/basic
Front: What are the four RCD test conditions and their expected results?
Back: ½×IΔn → must NOT trip; 1×IΔn → trip within 300ms; 5×IΔn → trip within 40ms; test button → must trip. The ½×IΔn test verifies correct threshold (prevents nuisance tripping).

---

#type/cloze
Text: The 80% rule for Zs verification: measured Zs must be ≤ {{c1::80%}} of the maximum tabulated Zs value.
Extra: The 20% margin accounts for conductor resistance increase at operating temperature — the test is done cold, but faults happen when cables are warm.

---

#type/basic
Front: For a Type B 32A MCB, what is the maximum Zs, and what measured value passes the 80% rule?
Back: Zs_max = 230 / (5 × 32) = 1.44 Ω. Pass threshold: 80% × 1.44 = 1.15 Ω.

---

#type/cloze
Text: ADS disconnection time for final circuits ≤32A at 230V is {{c1::0.4 seconds}}. For distribution circuits and final circuits >32A, it is {{c2::5 seconds}}.
Extra: From IEC 60364-4-41.

---

#type/basic
Front: What is the key equation for total earth fault loop impedance in TN systems?
Back: Zs = Ze + (R₁ + R₂), where Ze = external loop impedance, R₁ = line conductor resistance, R₂ = CPC resistance.

---

#type/cloze
Text: In TT systems, RCDs are mandatory because the earth return path goes through {{c1::soil}} — a high-impedance path that limits fault current too low for overcurrent devices to trip.
Extra: ADS condition: RA × IΔn ≤ 50V.

---

#type/basic
Front: What is the TT system ADS condition formula, and what does 30mA RCD require for electrode resistance?
Back: RA × IΔn ≤ 50V. For 30mA RCD: RA ≤ 50/0.030 = 1667 Ω. Typical driven rod: 20–200 Ω (well within limit).

---

#type/cloze
Text: In IT systems, a first earth fault does not trip any device. An {{c1::Insulation Monitoring Device (IMD)}} detects the fault and raises an alarm.
Extra: The fault must be located and cleared before a second fault occurs, which would create a phase-to-phase or line-to-earth fault.

---

#type/basic
Front: What is the difference between SELV and PELV?
Back: SELV (Safety Extra Low Voltage): ≤50V AC, no earth connection, double/reinforced insulation from all other circuits. PELV (Protective Extra Low Voltage): same voltage limits but the circuit or equipment may be earthed.

---

#type/cloze
Text: The maximum permitted voltage drop from the origin of the installation to the load is {{c1::4%}} (IEC 60364-5-52).
Extra: Some national interpretations allow 5% for certain applications.

---

#type/basic
Front: What does the abbreviation Ze stand for, and what does it represent?
Back: External Loop Impedance — the impedance of the earth fault loop external to the installation (supply network), measured at the incomer.

---

#type/basic
Front: What does Zs stand for, and how does it relate to Ze?
Back: Total Earth Fault Loop Impedance. Zs = Ze + R₁ + R₂ (external impedance + line conductor resistance + CPC resistance).

---

#type/cloze
Text: For floor and wall resistance testing in special locations, the minimum resistance for systems up to 500V is {{c1::50 kΩ}} using a {{c2::500V DC}} test voltage.
Extra: A tripod electrode weighted to ~270 N (representing a person's foot force) is used.

---

#type/basic
Front: What is the purpose of the phase sequence check, and how is a wrong sequence corrected?
Back: Verifies 3-phase supply is in correct order (L1→L2→L3 clockwise). Incorrect sequence causes motors to rotate in reverse. Fix: swap any two phase conductors at the supply terminal.

---

#type/cloze
Text: For 11kV cable insulation resistance testing, a {{c1::5000V DC}} megger is used, with a minimum acceptable value of {{c2::100 MΩ}}.
Extra: A healthy new cable will read in the gigaohm range.

---

#type/basic
Front: In the Kericho case study, what was the measured voltage drop on the dryer feeder, and did it pass?
Back: 13V drop (401V at MDB, 388V at machine terminals) = 3.2%. Pass (within 4% limit).

---

#type/cloze
Text: For VCB contact resistance testing, a DLRO is used at {{c1::100A DC}}. New VCB contact resistance should be <{{c2::100 µΩ}} per pole.
Extra: DLRO = Digital Low Resistance Ohmmeter, measures in the µΩ–mΩ range.
