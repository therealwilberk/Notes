---
tags:
  - motor-testing
  - single-phase
  - motor-types
aliases:
  - "Types of Single-Phase Motors"
source: scraped
parent_module: "[[Module 4 — Single-Phase Induction Motors]]"
---

# Types of Single-Phase Motors

> [!info] Part of [[Module 4 — Single-Phase Induction Motors]]

# Types of Single Phase Induction Motors (Split Phase, Capacitor Start, Capacitor Run)

Source: https://www.electrical4u.com/types-of-single-phase-induction-motor/
Last updated: April 26, 2024

---

Key learnings:
- **Single Phase Induction Motor Definition**: A single-phase induction motor is a type of electric motor that operates with a single alternating current phase, requiring additional mechanisms to initiate rotation.
- **Split Phase Operation**: The split phase motor utilizes an auxiliary winding with higher resistance and a centrifugal switch that disengages at 75-80% of the synchronous speed, facilitating the motor start.
- **Capacitor Start and Run**: These motors use capacitors to create a necessary phase difference, producing a strong starting torque and improving the power factor during operation.
- **Permanent Split Capacitor Advantages**: The PSC motor maintains a constant capacitor connection, which eliminates the need for a starting switch and enhances efficiency.
- **Shaded Pole Characteristics**: Shaded pole motors use a copper ring to induce a phase shift in part of the pole, creating a rotating magnetic field suitable for small, low-power devices.

Single-phase induction motors are made self-starting by providing additional flux by some supplementary means.

Single-phase induction motors are classified depending on how this additional flux is generated:

1. Split phase induction motor.
2. Capacitor-start inductor motor.
3. Capacitor-start capacitor-run induction motor (two-value capacitor method).
4. Permanent split capacitor (PSC) motor.
5. Shaded pole induction motor.

## Split Phase Induction Motor

In addition to the main winding, the stator of a single-phase induction motor includes an auxiliary or starting winding. This winding is linked to a centrifugal switch, which disconnects it from the circuit at 75-80% of the motor's top speed.

This switch aims to disconnect the auxiliary winding from the main circuit when the motor attains a speed up to 75 to 80% of the synchronous speed.

We know that the running winding is inductive in nature. We aim to create the phase difference between the two windings, and this is possible if the starting winding carries high resistance.

In a highly resistive winding, the current aligns closely with the voltage. Conversely, in a highly inductive winding, the current significantly lags behind the voltage.

The starting winding is highly resistive so, the current flowing in the starting winding lags behind the applied voltage by a very small angle and the running winding is highly inductive in nature so, the current flowing in running winding lags behind applied voltage by a large angle.

The resultant of these two currents is IT — the resultant of these two currents produce a rotating magnetic field which rotates in one direction.

In a split-phase induction motor, the starting and main current get split from each other by some angle, so this motor got its name as a split-phase induction motor.

### Applications of Split Phase Induction Motor

Split phase induction motors have low starting current and moderate starting torque. Available in sizes from 1/20 to 1/2 KW, they power devices such as fans, blowers, washing machines, and lathes.

## Capacitor Start IM and Capacitor Start Capacitor Run IM

The working principle of capacitor-start inductor motors is almost the same as capacitor-start capacitor-run induction motors.

We already know that a single-phase induction motor is not self-starting because the magnetic field produced is not a rotating type. To produce a rotating magnetic field, there must be some phase difference.

In the case of a split-phase induction motor, we use resistance for creating phase difference, but here we use a capacitor for this purpose. We are familiar with the fact that the current flowing through the capacitor leads to the voltage.

So, in capacitor start inductor motor and capacitor start capacitor run induction motor, we use two windings: the main winding, and the starting winding.

With starting winding, we connect a capacitor, so the current flowing in the capacitor (Ist) leads the applied voltage by some angle φst.

The running winding is inductive in nature so, the current flowing in running winding lags behind applied voltage by an angle φm.

Now there occur large phase angle differences between these two currents, which produce a resultant current. This will produce a rotating magnetic field since the torque produced by these motors depends upon the phase angle difference, which is almost 90°.

So, these motors produce very high starting torque. In the case of capacitor start induction motor, the centrifugal switch is provided to disconnect the starting winding when the motor attains a speed up to 75 to 80% of the synchronous speed. But in the case of capacitor start capacitor run induction motor, there is no centrifugal switch so, the capacitor remains in the circuit and improves the power factor and the running conditions.

### Application of Capacitor Start IM and Capacitor Start Capacitor Run IM

These motors have high starting torque; hence they are used in conveyors, grinders, air conditioners, compressors, etc. They are available up to 6 kW.

## Permanent Split Capacitor (PSC) Motor

It has a cage rotor and stator. The stator has two windings – main and auxiliary winding. It has only one capacitor in series with starting winding. It has no starting switch.

### Advantages of PSC Motor

- No centrifugal switch is needed
- Higher efficiency and pull-out torque

### Applications of PSC Motor

The PSC motor is commonly used in fans and blowers within heaters and air conditioners, as well as in office machinery.

## Shaded Pole Single Phase Induction Motors

The stator of the shaded pole single-phase induction motor has salient or projected poles. These poles are shaded by a copper band or ring, which is inductive in nature.

The poles are divided into two unequal halves. The smaller portion carries the copper band and is called the shaded portion of the pole.

When a single-phase supply is given to a shaded pole induction motor's stator, an alternating flux is produced. This change of flux induces emf in the shaded coil. Since this shaded portion is short-circuited, the current is produced in it in such a direction to oppose the main flux.

The flux in the shaded pole lags behind the flux in the unshaded pole. The phase difference between these two fluxes produces resultant rotating flux.

### How the Rotating Field is Produced (Three Regions)

**REGION 1:** When flux changes from zero to nearly maximum positive — rate of rising flux is very high. According to Faraday's law, emf gets induced in the copper band. Per Lenz's law, the induced current opposes the change. The shaded ring flux opposes the main flux, crowding flux in the non-shaded part. The magnetic axis shifts to the non-shaded part.

**REGION 2:** When flux remains almost constant at maximum — very little induced emf in shaded portion. Flux distribution remains uniform, magnetic axis at center of pole.

**REGION 3:** When flux decreases from maximum to zero — rate of decrease is very high. Induced emf in copper band produces flux that aids the main flux, crowding flux in the shaded part. Magnetic axis shifts to the shaded part.

This shifting of the magnetic axis continues for the negative cycle and leads to the production of a rotating magnetic field. The direction is from the non-shaded part to the shaded part.

### Advantages of Shaded Pole Motor

- Very economical and reliable
- Construction is simple and robust (no centrifugal switch)

### Disadvantages of Shaded Pole Motor

- Low power factor
- Starting torque is very poor
- Efficiency is very low (copper losses high due to copper band)
- Speed reversal is difficult and expensive (requires another set of copper rings)

### Applications of Shaded Pole Motor

Small instruments, hairdryers, toys, record players, small fans, electric clocks. Usually available in a range of 1/300 to 1/20 KW.


## See Also

- [[Module 4 — Single-Phase Induction Motors]]
- [[IEC Motor Testing — Map of Content]]

## Sources

- Scraped from web resources collected during [[IEC Motor Testing — Map of Content]] research
