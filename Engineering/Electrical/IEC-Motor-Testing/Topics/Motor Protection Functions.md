---
tags:
  - motor-testing
  - protection
  - functions
aliases:
  - "Motor Protection Functions"
source: scraped
parent_module: "[[Module 3 — Motor Protection & Control]]"
---

# Motor Protection Functions

> [!info] Part of [[Module 3 — Motor Protection & Control]]

Source: https://www.electrical-installation.org/enwiki/Motor_protection_functions

---

# Motor protection functions

From Electrical Installation Guide

[Home](/enwiki/Main_Page "Main Page") > [Characteristics of particular sources and loads](/enwiki/Characteristics_of_particular_sources_and_loads "Characteristics of particular sources and loads") > [Asynchronous motors](/enwiki/Asynchronous_motors "Asynchronous motors") > Motor protection functions

Jump to:navigation, search

These are the arrangements implemented in order to avoid operation of motors in abnormal conditions which could result in negative events such as: overheating, premature ageing, destruction of electrical windings, damage to coupling or gear box, … 

Four levels of protection schemes are commonly proposed: "Conventional", "Advanced", "Advanced Plus", and "High Performance", which can be adopted depending on the sophistication and power of the driven machine. 

  * **"Conventional"** protection functions apply for every type of motor or application,
  * **"Advanced"** protection functions apply to more sophisticated machines requesting special attention,
  * **"Advanced Plus"** , and **"High performance"** protection functions are justified for high power motors, high demanding applications, or motors in critical process or whenever ground current must be measured with high accuracy (~ 0,01A).



As shown in the following figure: “High performance “ protections are not based only on current but also on voltage 

Fig. N76 – Classification of protection functions

**Protection** | Conventional  | Advanced  | Advanced Plus  | High Performance     
Short-circuit / Instantaneous overcurrent  | ☑ | ☑ | ☑ | ☑  
Thermal overload  | ☑ | ☑ | ☑ | ☑  
Phase current imbalance  | ☑ | ☑ | ☑ | ☑  
Phase current loss  | ☑ | ☑ | ☑ | ☑  
Over-current(instantaneous and temporised)  | ☑ | ☑ | ☑ | ☑  
Ground fault / Instantaneous earth fault  | ☑ | ☑ | ☑ | ☑  
Long start (stall) / Incomplete sequence  |  | ☑ | ☑ | ☑  
Jam (locked rotor)  |  | ☑ | ☑ | ☑  
Under-current  |  | ☑ | ☑ | ☑  
Phase current reversal  |  |  | ☑ | ☑  
Motor temperature (by sensors)  |  |  | ☑ | ☑  
Rapid cycle lock-out / Locking out  |  |  | ☑ | ☑  
Load shedding  |  |  | ☑ | ☑  
Notching or jogging / Number of starts  |  |  | ☑ | ☑  
Phase voltage imbalance  |  |  |  | ☑  
Phase voltage loss  |  |  |  | ☑  
Phase voltage reversal  |  |  |  | ☑  
Under-voltage  |  |  |  | ☑  
Over-voltage  |  |  |  | ☑  
Under-power  |  |  |  | ☑  
Over-power  |  |  |  | ☑  
Under power factor  |  |  |  | ☑  
Over power factor  |  |  |  | ☑  
Motor reclosing  |  |  |  | ☑  
  
Here is a list of motor protection functions and the result of activation. 

**Short-circuit** = disconnection in case of a short-circuit at the motor terminals or inside the motor windings.  
**Instantaneous overcurrent** = operates with no intentional time delay when the current exceeds a preset value.  
**Thermal overload** = disconnection of motor in case of sustained operation with a torque exceeding the nominal value. Overload is detected by measurement of excessive stator current or by using PTC probes.  
**Phase current imbalance** = disconnection of the motor in case of high current imbalance, responsible for increased power losses and overheating.  
**Phase current loss** = disconnection of the motor if one phase current is zero, as this is revealing of cable or connection breaking.  
**Over-current** = alarm or disconnection of the motor in case of high phase current, revealing a shaft over-torque.  
**Ground fault / Instantaneous earth fault** = disconnection in case of a fault between a motor terminal and ground.Even if the fault current is limited, a fast action could avoid a complete destruction of the motor. It can be measured with the sum of the 3 phases if the accuracy required is not high (~ 30%). If high accuracy is required then it must be measured with a ground CT (0.01A accuracy).  
**Long start (stall)** = disconnection in case of a starting time longer than normal (due to mechanical problem or voltage sag) in order to avoid overheating of the motor.  
**Jam** = disconnection in order to avoid overheating and mechanical stress if motor is blocked while running because of congestion.  
**Undercurrent** = alarm or disconnection of the motor in case a low current value is detected, revealing a no-load condition (e.g.: pump drain, cavitation, broken shaft, …)  
**Phase current reversal** = disconnection when a wrong phase current sequence is detected  
**Motor temperature (by sensors)** = alarm or disconnection in case of high temperature detected by probes.  
**Rapid cycle lock-out** = prevent connection and avoid overheating due to too frequent start-up.  
**Load shedding** = disconnection of the motor when a voltage drop is detected, in order to reduce the supply load and return to normal voltage.  
**Notching or jogging / Number of starts** = a specified number of successive operations within a given time.  
**Phase voltage imbalance** = disconnection of the motor in case of high voltage imbalance, responsible for increased power losses and overheating.  
**Phase voltage loss** = disconnection of motor if one phase of the supply voltage is missing. This is necessary in order to avoid a single-phase running of a three-phase motor, which results in a reduced torque, increased stator current, and inability to start.  
**Phase voltage reversal** = prevent the connection and avoid the reverse rotation of the motor in case of a wrong cabling of phases to the motor terminals, which could happen during maintenance for example.  
**Under-voltage** = prevent the connection of the motor or disconnection of the motor, as a reduced voltage could not ensure a correct operation of the motor.  
**Over-voltage** = prevent the connection of the motor or disconnection of the motor, as an increased voltage could not ensure a correct operation of the motor.  
**Under-power** = alarm or disconnection of the motor in case of power lower than normal, as this situation is revealing a pump drain (risk of destruction of the pump) or broken shaft.  
**Over-power** = alarm or disconnection of the motor in case of power higher than normal, as this situation is revealing a machine overload.  
**Under power factor** = can be used for detection of low power with motors having a high no-load current.  
**Over power factor** = can be used for detection of end of the starting phase.  
**Motor reclosing** = controls the automatic reclosing and locking out of a motor. 

The consequence of abnormal overheating is a reduced isolation capacity of the materials, thus leading to a significant shortening of the motor lifetime. This is illustrated on **Figure** N77, and justifies the importance of overload or over-temperature protection. 

[](/enwiki/File:DB422690_EN.svg)

Fig. N77 – Reduced motor lifetime as a consequence of overheating

Overload relays (thermal or electronic) protect motors against overloads, but they must allow the temporary overload caused by starting, and must not trip unless the starting time is abnormally long. 

Depending on the application, the motor starting time can vary from a few seconds (for no-load starting, low resistive torque, etc.) to several tens of seconds (for a high resistive torque, high inertia of the driven load, etc.). It is therefore necessary to fit relays appropriate to the starting time. 

To meet this requirement, IEC Standard 60947-4-1 defines several classes of overload relays, each characterized by its tripping curve (see **Figure** N78). 

The relay rating is to be chosen according to the nominal motor current and the calculated starting time. 

Trip class 10 is adapted to normal duty motors. 

Trip class 20 is recommended for heavy duty motors 

Trip class 30 is necessary for very long motor starting. 

[](/enwiki/File:DB422691_EN.svg)

Fig. N78 – Tripping curves of overload relays

Retrieved from "[https://www.electrical-installation.org/enw/index.php?title=Motor_protection_functions&oldid=27164](https://www.electrical-installation.org/enw/index.php?title=Motor_protection_functions&oldid=27164)"

[Categories](/enwiki/Special:Categories "Special:Categories"): 

  * [Chapter - Characteristics of particular sources and loads](/enwiki/Category:Chapter_-_Characteristics_of_particular_sources_and_loads "Category:Chapter - Characteristics of particular sources and loads")
  * [Eig-content-pages](/enw/index.php?title=Category:Eig-content-pages&action=edit&redlink=1 "Category:Eig-content-pages \(page does not exist\)")


## See Also

- [[Module 3 — Motor Protection & Control]]
- [[IEC Motor Testing — Map of Content]]

## Sources

- Scraped from web resources collected during [[IEC Motor Testing — Map of Content]] research
