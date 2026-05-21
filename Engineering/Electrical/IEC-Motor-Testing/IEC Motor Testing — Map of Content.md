---
tags:
  - moc
  - motor-testing
  - iec
aliases:
  - "Motor Testing MOC"
  - "IEC Motor Testing"
created: 2026-05-21
---

# IEC Motor Testing — Map of Content

> [!summary] A structured study of IEC motor testing standards, protection, and fault diagnosis.
> 
> **Source:** Notion curriculum modules + collected technical resources
> **Start date:** May 2026

## Modules

### [[Module 0 — Motor Family Tree]]
Classification and history of electric motors

### [[Module 1 — 3-Phase Squirrel Cage Induction Motor]]
Slip, equivalent circuit, torque-speed characteristics

### [[Module 2 — Motor Starting Methods]]
DOL, star-delta, soft starter, VFD starting

### [[Module 3 — Motor Protection & Control]]
Relays, contactors, overload protection, Schneider TeSys

### [[Module 4 — Single-Phase Induction Motors]]
Split-phase, capacitor start/run, PSC, centrifugal switch

### [[Module 5 — DC Motors]]
Series, shunt, compound, PMDC, speed control

### [[Module 6 — Synchronous Motors]]
Working principle, power factor correction, excitation

### [[Module 7 — Motor Testing & Pre-Commissioning]]
IR testing, IEEE 43, ISO 10816, polarization index

### [[Module 8 — Motor Fault Diagnosis & Troubleshooting]]
Bearing failure, winding faults, VFD troubleshooting

## Standards & References

- [[IEEE 43-2013 — What's New (EASA Summary)]]
- [[ISO 10816 Vibration Severity Charts]]

## Key Topics

- [[Single-Phase Induction Motor]]
- [[Types of Single-Phase Motors]]
- [[Split Capacitor (PSC) Motor]]
- [[Centrifugal Switch]]
- [[Schneider Electric — Induction Motors]]
- [[Motor Protection Coordination]]
- [[Basic Motor Protection Scheme]]
- [[Motor Protection Functions]]

## Attachments

- [[Attachments/ABB-Motion-Drive-Error-Troubleshooting.pdf|ABB-Motion-Drive-Error-Troubleshooting]]
- [[Attachments/IEEE-43-Review-Polarization-Index.pdf|IEEE-43-Review-Polarization-Index]]
- [[Attachments/Megger-A-Stitch-In-Time-Insulation-Testing.pdf|Megger-A-Stitch-In-Time-Insulation-Testing]]
- [[Attachments/Megger-Guide-Low-Voltage-Motor-Testing.pdf|Megger-Guide-Low-Voltage-Motor-Testing]]
- [[Attachments/SKF-Bearing-Damage-Failure-Analysis.pdf|SKF-Bearing-Damage-Failure-Analysis]]
- [[Attachments/SKF-Bearing-Maintenance-Handbook.pdf|SKF-Bearing-Maintenance-Handbook]]
- [[Attachments/Schneider-TeSys-2026-Catalogue.pdf|Schneider-TeSys-2026-Catalogue]]

## Progress

- [x] Module 0 — Motor Family Tree
- [ ] Module 1 — 3-Phase Induction
- [ ] Module 2 — Starting Methods
- [x] Module 3 — Protection & Control (resources collected)
- [x] Module 4 — Single-Phase (resources collected)
- [ ] Module 5 — DC Motors
- [ ] Module 6 — Synchronous
- [x] Module 7 — Testing & Pre-Commissioning (resources collected)
- [x] Module 8 — Fault Diagnosis (resources collected)

---

## Dataview: All Tasks

```dataview
TASK
WHERE contains(file.path, "IEC-Motor-Testing")
GROUP BY file.link
```

## Dataview: Modules by Status

```dataview
TABLE status, module AS "Module #", length(file.outlinks) AS "Links"
FROM "Engineering/Electrical/IEC-Motor-Testing/Modules"
SORT file.name ASC
```

## Dataview: Recent Changes

```dataview
TABLE file.mtime AS "Modified"
FROM "Engineering/Electrical/IEC-Motor-Testing"
SORT file.mtime DESC
LIMIT 10
```

## Dataview: All Tags

```dataview
LIST rows.file.link
FROM "Engineering/Electrical/IEC-Motor-Testing"
FLATTEN file.tags AS tag
WHERE tag != "#moc" AND tag != "#motor-testing"
GROUP BY tag
SORT length(rows) DESC
```
