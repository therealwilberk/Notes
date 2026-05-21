---
tags:
  - motor-testing
  - single-phase
  - psc
aliases:
  - "Split Capacitor (PSC) Motor"
source: scraped
parent_module: "[[Module 4 — Single-Phase Induction Motors]]"
---

# Split Capacitor (PSC) Motor

> [!info] Part of [[Module 4 — Single-Phase Induction Motors]]

# Split Capacitor Motor (Permanent Split Capacitor)

Source: https://www.electrical4u.com/split-capacitor-motor/
Last updated: May 9, 2024

---

Key learnings:
- **PSC Motor Definition**: A permanent split capacitor motor is a split-phase induction motor with a capacitor permanently connected to enhance operation.
- **Capacitor Functionality**: The capacitor ensures a phase difference between main and auxiliary windings, crucial for smooth operation and consistent torque.
- **Torque Generation**: As load changes, rotor torque adjusts automatically to maintain consistent speed.
- **Speed Adjustment Methods**: Motor speed can be controlled through input voltage or frequency changes.
- **Practical Uses**: Fans in air conditioning systems, compressors in refrigerators.

## What is a Permanent Split Capacitor Motor?

A permanent split capacitor motor (PSC motor) is a split-phase induction motor with a capacitor permanently connected to enhance operation. It is a type of single-phase induction motor with a stator and cage-type rotor.

The permanent split capacitor motor features a capacitor that remains connected during both the start and run phases. As the capacitor always remains in the circuit, this motor does not require a centrifugal switch. This motor produces uniform torque. Because the auxiliary winding is always connected, it operates like a balanced two-phase motor.

## How Does a Permanent Split Capacitor Motor Work?

Two windings are connected in the stator:
- Main winding
- Auxiliary winding (Starting winding)

The single-phase power supply is given to the main winding. The auxiliary winding is connected via a capacitor C.

The capacitor linked to the auxiliary winding renders it highly capacitive, contrasting with the highly inductive main winding. Therefore, it creates a 90° electrical angle between main and auxiliary winding.

When a single-phase supply is given to the main winding, Im current flows through it. Due to the capacitor, a short delay occurs in auxiliary winding and Ia current flows after the delay.

The currents produce a rotating magnetic field which generates torque in the rotor, and the rotor starts rotating.

In the auxiliary winding, a counter EMF is produced as speed increases, limiting current through the auxiliary winding. At rated speed, very small current passes through the auxiliary winding, so it won't overheat.

When load increases, speed reduces slightly, reducing counter EMF. This creates a significant potential difference, causing increased auxiliary winding current and increased torque. The motor tries to operate at constant speed under varying load conditions.

## Speed Control

The PSC motor can be used for variable speed applications:

**Method 1: Varying input voltage** — An autotransformer is used. But for low voltage conditions, starting torque is very low and speed is sensitive to voltage changes.

**Method 2: Controlling frequency** — A controlled rectifier converts AC to DC and back to AC at the desired frequency. Speed can be controlled in the range of 20 to 110% of full-load speed.

## Advantages

- No centrifugal switch needed (reduces maintenance)
- High efficiency
- Higher power factor (capacitor permanently connected)
- High pull-out torque

## Disadvantages

- Electrolytic capacitor cannot be used for continuous running; paper-spaced oil-filled type capacitors are required (costly and larger)
- Single value capacitor has low starting torque

## Applications

- Refrigerator compressors
- Office machinery
- Fans in heaters and air-conditioners


## See Also

- [[Module 4 — Single-Phase Induction Motors]]
- [[IEC Motor Testing — Map of Content]]

## Sources

- Scraped from web resources collected during [[IEC Motor Testing — Map of Content]] research
