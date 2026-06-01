---
type: topic
tags: [eee, safety-circuits, interlocks, e-stop]
created: 2026-06-01
status: building
parent: "[[MOC — Electrical Installation]]"
sources:
  - "[[BMS Controls Training — 6hr Video]]"
---

# Safety Circuits & Interlocks

## The Run-Enable / Safety Circuit

A safety circuit is a chain of devices wired **in series**. Every device must be in its healthy (closed) state for the circuit to be complete. Any single device breaking the chain shuts down the system.

```
Power supply → E-stop (NC) → Thermal link 1 (NC) → Thermal link 2 (NC) → [more devices...] → Return signal
```

All closed = system healthy = return signal present.
One open = fault = return signal lost.

## Common Safety Devices

### Emergency Stop (E-stop)

Normally closed. Hit the button → contact opens → circuit breaks → system shuts down. Placed where operators can reach it quickly — plant rooms, near equipment, at panel doors.

### Thermal Links

Fusible devices that melt at a set temperature. Normally closed. If a boiler overheats, the thermal link fuses open and breaks the safety circuit. Cannot be reset — the link must be replaced.

Multiple thermal links in **series**: if one blows, the whole chain breaks. This means you can't tell *which* device triggered the fault from the circuit alone — but that's usually fine because the priority is shutting down (e.g., cutting gas supply), not identifying the source.

### Fire Alarm Signal

When integrated with the building fire alarm, a signal from the fire panel can break the safety circuit. This is typically a volt-free contact from the fire panel.

## Series vs Parallel

| Configuration | Behavior |
|---------------|----------|
| **Series** | One fault breaks the chain. Simpler, fewer wires. Can't identify which device faulted from the circuit alone. |
| **Parallel** | All must be healthy for the return signal. Lets you identify *which* device triggered. More complex wiring. |

Series is the default for most safety circuits. The trade-off is simplicity vs diagnostics.

## The Logic

The return signal from the safety circuit typically drives a relay:

- **Healthy** → relay energized → contact in one position (system enabled)
- **Fault** → relay de-energized → contact falls to default position (system disabled, alarm active)

This relay is the interface between the safety circuit and the rest of the control system.

> [!warning] NC vs NO on site
> Sometimes the correct contact state (NO or NC) isn't known until physically on site. The designer picks what seems right, and the installer may need to invert it. **Red pen the drawing** to mark what actually got installed. This is normal.
