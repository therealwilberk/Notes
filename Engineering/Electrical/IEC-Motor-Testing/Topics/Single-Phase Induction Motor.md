---
tags:
  - motor-testing
  - single-phase
  - induction
aliases:
  - "Single-Phase Induction Motor"
source: scraped
parent_module: "[[Module 4 — Single-Phase Induction Motors]]"
---

# Single-Phase Induction Motor

> [!info] Part of [[Module 4 — Single-Phase Induction Motors]]

# Single Phase Induction Motor: Working Principle & Construction

Source: https://www.electrical4u.com/single-phase-induction-motor/
Last updated: April 18, 2024

---

Key learnings:
- **Single Phase Induction Motor Definition**: A single-phase induction motor is an electrical motor that converts single-phase electrical energy into mechanical energy using magnetic interactions.
- **Construction**: The construction features two main parts—stator and rotor—with the stator receiving AC power and the rotor designed to rotate and drive mechanical loads.
- **Working Principle**: These motors use alternating magnetic fields produced in the stator to induce current in the rotor, creating the torque necessary for rotation.
- **Self-Starting Challenge**: Unlike three-phase motors, single-phase induction motors are not self-starting because the opposing magnetic forces at startup cancel out, producing no torque.
- **Improving Startability**: To become self-starting, these motors employ techniques like split-phase and capacitor methods to create an initial rotating magnetic field.

## What is a Single Phase Induction Motor?

Single-phase power systems are more commonly used than three phase system in homes, businesses, and to some extent in industry. This is because single-phase systems are more economical and sufficient for the low power needs of most houses, shops, and offices.

Single-phase motors are simple to build, cost-effective, reliable, and easy to maintain. Thanks to these benefits, they are used in appliances like vacuum cleaners, fans, and washing machines, as well as in devices like centrifugal pumps and blowers.

The single phase AC motors are further classified as:
1. Single phase induction motors or asynchronous motors.
2. Single phase synchronous motors.
3. Commutator motors.

## Construction of Single Phase Induction Motor

Like any other electrical motor, asynchronous motor also have two main parts namely rotor and stator.

**Stator:**
As its name indicates stator is a stationary part of induction motor. A single phase AC supply is given to the stator of single phase induction motor.

**Rotor:**
The rotor is a rotating part of an induction motor. The rotor connects the mechanical load through the shaft. The rotor in the single-phase induction motor is of squirrel cage rotor type.

The construction of a single-phase induction motor closely resembles that of a squirrel cage three-phase induction motor. However, the single-phase motor's stator features two windings, unlike the single three-phase winding found in three phase induction motor.

### Stator of Single Phase Induction Motor

The stator of the single-phase induction motor has laminated stamping to reduce eddy current losses on its periphery. The slots are provided on its stamping to carry stator or main winding. Stampings are made up of silicon steel to reduce the hysteresis losses. When we apply a single phase AC supply to the stator winding, the magnetic field gets produced, and the motor rotates at speed slightly less than the synchronous speed Ns. Synchronous speed Ns is given by:

Ns = 120f/P

Where:
- f = supply voltage frequency
- P = No. of poles of the motor

The construction of the stator of the single-phase induction motor is similar to that of three phase induction motor except there are two dissimilarities in the winding part:

1. The single-phase induction motors are mostly provided with concentric coils. We can easily adjust the number of turns per coil with the help of concentric coils. The mmf distribution is almost sinusoidal.
2. In all types except for the shaded pole motor, an asynchronous motor includes two stator windings: the main and the auxiliary winding. These windings are positioned at right angles to each other in what is known as space quadrature.

### Rotor of Single Phase Induction Motor

The construction of the rotor of the single-phase induction motor is similar to the squirrel cage three-phase induction motor. The rotor is cylindrical and has slots all over its periphery. The slots are not made parallel to each other but are a little bit skewed as the skewing prevents magnetic locking of stator and rotor teeth and makes the working of induction motor more smooth and quieter.

The squirrel cage rotor consists of aluminum, brass or copper bars. These aluminum or copper bars are called rotor conductors and placed in the slots on the periphery of the rotor. The copper or aluminum rings permanently short the rotor conductors called the end rings.

To provide mechanical strength, these rotor conductors are braced to the end ring and hence form a complete closed circuit resembling a cage and hence got its name as squirrel cage induction motor. As end rings permanently short the bars, the rotor electrical resistance is very small and it is not possible to add external resistance as the bars get permanently shorted. The absence of slip ring and brushes make the construction of single phase induction motor very simple and robust.

## Working Principle of Single Phase Induction Motor

NOTE: For the working of any electrical motor whether its AC or DC motor, we require two fluxes as the interaction of these two fluxes produced the required torque.

When we apply a single phase AC supply to the stator winding of single phase induction motor, the alternating current starts flowing through the stator or main winding. This alternating current produces an alternating flux called main flux. This main flux also links with the rotor conductors and hence cut the rotor conductors.

According to Faraday's law of electromagnetic induction, emf gets induced in the rotor. As the rotor circuit is closed one so, the current starts flowing in the rotor. This current is called the rotor current. This rotor current produces its flux called rotor flux. Since this flux is produced due to the induction principle so, the motor working on this principle got its name as an induction motor. Now there are two fluxes one is main flux, and another is called rotor flux. These two fluxes produce the desired torque which is required by the motor to rotate.

## Why Single Phase Induction Motor is not Self Starting?

According to double field revolving theory, we can resolve any alternating quantity into two components. Each component has a magnitude equal to the half of the maximum magnitude of the alternating quantity, and both these components rotate in the opposite direction to each other.

When we apply a single phase AC supply to the stator winding of single phase induction motor, it produces its flux of magnitude φm. According to the double field revolving theory, this alternating flux φm is divided into two components of magnitude φm/2. Each of these components will rotate in the opposite direction, with the synchronous speed Ns.

Let us call these two components of flux as forwarding component of flux φf and the backward component of flux φb. The resultant of these two components of flux at any instant of time gives the value of instantaneous stator flux at that particular instant.

At starting condition, both the forward and backward components of flux are exactly opposite to each other. Also, both of these components of flux are equal in magnitude. So, they cancel each other and hence the net torque experienced by the rotor at the starting condition is zero. So, the single phase induction motors are not self-starting motors.

## Methods for Making Single Phase Induction as Self Starting Motor

From the above topic, we can easily conclude that the single-phase induction motors are not self-starting because the produced stator flux is alternating in nature and at the starting, the two components of this flux cancel each other and hence there is no net torque. The solution to this problem is that if we make the stator flux rotating type, rather than alternating type, which rotates in one particular direction only. Then the induction motor will become self-starting.

Now for producing this rotating magnetic field, we require two alternating flux, having some phase difference angle between them. When these two fluxes interact with each other, they will produce a resultant flux. This resultant flux is rotating in nature and rotates in space in one particular direction only.

Once the motor starts running, we can remove the additional flux. The motor will continue to run under the influence of the main flux only. Depending upon the methods for making asynchronous motor as Self Starting Motor, there are mainly four types of single phase induction motor:

1. Split phase induction motor
2. Capacitor start induction motor
3. Capacitor start capacitor run induction motor
4. Shaded pole induction motor
5. Permanent split capacitor motor or single value capacitor motor

## Comparison between Single Phase and Three Phase Induction Motors

- Single phase induction motors are simple in construction, reliable and economical for small power rating as compared to three phase induction motors.
- The electrical power factor of single phase induction motors is low as compared to three phase induction motors.
- For the same size, the single-phase induction motors develop about 50% of the output as that of three phase induction motors.
- The starting torque is also low for asynchronous motors/single phase induction motor.
- The efficiency of single phase induction motors is less compared to that of three phase induction motors.
- Single phase induction motors are simple, robust, reliable and cheaper for small ratings. They are available up to 1 KW rating.


## See Also

- [[Module 4 — Single-Phase Induction Motors]]
- [[IEC Motor Testing — Map of Content]]

## Sources

- Scraped from web resources collected during [[IEC Motor Testing — Map of Content]] research
