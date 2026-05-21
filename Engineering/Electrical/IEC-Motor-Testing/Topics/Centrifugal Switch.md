---
tags:
  - motor-testing
  - single-phase
  - starting
aliases:
  - "Centrifugal Switch"
source: scraped
parent_module: "[[Module 4 — Single-Phase Induction Motors]]"
---

# Centrifugal Switch

> [!info] Part of [[Module 4 — Single-Phase Induction Motors]]

# Centrifugal Switch: What Is It & How Does It Work

Source: https://www.electrical4u.com/centrifugal-switch/
Last updated: May 2, 2024

---

Key learnings:
- **Definition**: A centrifugal switch is an electrical component that activates based on centrifugal force from a motor's rotating shaft to control motor start-up.
- **Operational Mechanism**: The switch engages a boost circuit to start the motor and disconnects once the motor reaches sufficient speed.
- **Impact of Malfunction**: If the centrifugal switch fails to disconnect after the motor starts, the starting winding burns out.

## What is a Centrifugal Switch?

A centrifugal switch is an electrical switch powered by the centrifugal force created by a rotating shaft (typically from an electric motor or gasoline engine). Centrifugal switches activate or deactivate based on the rotational speed of the shaft.

## How Do Centrifugal Switches Work?

A centrifugal switch is normally found in single-phase induction motors and split-phase induction motors. It provides controlled switching when the specified engine speed is generated.

A single-phase AC motor has a centrifugal switch inside its case, attached to the motor shaft. When the motor is off and motionless, the switch is closed. When the motor is switched on, the switch drives electricity to the capacitor and extra coil winding, increasing starting torque. As RPM increases, the switch opens — the motor no longer needs the boost.

A centrifugal switch solves the problem that single-phase AC motors don't develop enough torque on their own to start from a dead stop:
1. Circuit switches on the centrifugal switch → provides boost to start motor
2. Switch turns off the boost circuit when motor reaches running speed
3. Motor runs normally

## What Happens if the Centrifugal Switch Does Not Open?

If the start switch does not open when needed, the starting winding will overheat and burn out, and the motor will not start next time.

## What is the Effect if the Centrifugal Switch is Not Disconnected After the Motor Starts?

The centrifugal switch should disconnect at about 70 to 80% of full speed. If not disconnected, heavy current continues through the starting winding, resulting in starting winding failure. Speed and current cannot reach maximum.

## Do All Single Phase Motors Have a Centrifugal Switch?

Not all. Permanent split capacitor (PSC) motors and shaded pole motors have no centrifugal switch. The start winding becomes an auxiliary winding when the motor reaches running speed, making it essentially a two-phase motor. These are considered the most reliable single-phase motors because there is no centrifugal starting switch.

## Centrifugal Switch in Induction Motors

Induction motors have a stator winding and auxiliary winding. Single-phase AC current is applied to the stator winding, but this alone cannot produce enough rotating field for starting torque. The auxiliary winding generates a field out of phase with the stator field, producing starting torque.

Once the motor starts and speed reaches a specified percentage of synchronous speed, the auxiliary winding circuit must be disconnected — this is where the centrifugal switch comes in.

## Why is the Centrifugal Switch Used in Most Single-Phase Induction Motors?

In common induction motors (drill presses, furnaces, table saws, pumps, grinders, washers/dryers), centrifugal switches are used with an additional winding to start the motor.

Single-phase induction motors require start auxiliary circuits. In very small motors (cooling fans), the auxiliary circuit can be on at all times, but this wastes electricity and generates heat. Above 1/10hp, it becomes attractive to turn off the starting circuit after spinning. A centrifugal switch does this.


## See Also

- [[Module 4 — Single-Phase Induction Motors]]
- [[IEC Motor Testing — Map of Content]]

## Sources

- Scraped from web resources collected during [[IEC Motor Testing — Map of Content]] research
