### Scale

Scale is the relationship between the size of an object in a drawing and its real-world size. A scale of 1:1 means actual size, 1:2 means the drawing is half-size, and 1:10 means the drawing is one-tenth of the real size.

In electrical schematics, scale is usually unimportant because symbols represent functions, not physical dimensions. The goal is to show electrical relationships and current paths, not physical appearance.

In panel layouts, mechanical drawings, and enclosure drawings, scale is important because components must physically fit. Incorrect scaling can make a design impossible to build.

Good CAD practice is to draw everything at full size in Model Space and apply scale only when creating printed views or layouts.

---

### Wiring & Wire Numbers

Wire numbers identify electrical nodes and help technicians trace circuits, troubleshoot faults, and verify connections. They act like addresses for conductors within the system.

A wire number changes whenever electrical continuity is interrupted by a device such as a switch, relay contact, breaker, or overload relay. If two points can have different voltages, they must have different wire numbers.

A wire number does not change when passing through a terminal block, connector, or uninterrupted conductor because the electrical node remains the same.

Different numbering systems exist. Sequential systems use numbers such as 100, 101, 102, while IEC power circuits often use formats like 1L1, 2L1, 3L1. In IEC notation, the number identifies the power section and L1, L2, or L3 identifies the phase.

---

### Reading Current Flow

Control circuits are typically read from the power source, through switches and interlocks, to a relay coil or load, then back to the return path. Ask: "What devices must be closed for current to reach the load?"

Power circuits are usually read from supply → protection device → contactor → overload relay → motor/load.

For troubleshooting, engineers often work backward from the failed device toward the supply until the missing voltage or open circuit is found.

---

### Key Rule

Think in terms of **electrical nodes**, not wires. A wire number represents an electrical node. If two points are electrically identical, they share a wire number. If a device can separate them electrically, a new wire number is required. This rule explains nearly every wire-numbering system used in industry.

