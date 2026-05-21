---
tags:
  - motor-testing
  - induction
  - schneider
aliases:
  - "Schneider Electric — Induction Motors"
source: scraped
parent_module: "[[Module 4 — Single-Phase Induction Motors]]"
---

# Schneider Electric — Induction Motors

> [!info] Part of [[Module 4 — Single-Phase Induction Motors]]

# Schneider Electric — Induction Motors (Electrical Installation Wiki)

Source: https://www.electrical-installation.org/enwiki/Induction_motors

---

# Induction motors

From Electrical Installation Guide

[Home](/enwiki/Main_Page "Main Page") > [General rules of electrical installation design](/enwiki/General_rules_of_electrical_installation_design "General rules of electrical installation design") > [Installed power loads - Characteristics](/enwiki/Installed_power_loads_-_Characteristics "Installed power loads - Characteristics") > Induction motors

Jump to:navigation, search

## Contents

  * 1 Current demand
  * 2 Subtransient current and protection setting
  * 3 Motor starting current
  * 4 Compensation of reactive-power (kvar) supplied to induction motors



The nominal power in kW (Pn) of a motor indicates its rated equivalent mechanical power output. 

The apparent power in kVA (Pa) supplied to the motor is a function of the output, the motor efficiency and the power factor: Pa=Pnηcos⁡φ

## Current demand

The rated current In supplied to the motor is given by the following formulae: 

### 3-phase motor

In=Pn×1033×U×η×cosφ

### 1-phase motor

In=Pn×103U×η×cosφ

where 

**In** = rated demand (in amps)  
**Pn** = nominal power (in kW)  
**U** = voltage between phases for 3-phase motors and voltage between the terminals for single-phase motors (in volts). A single-phase motor may be connected phase-to-neutral or phase-to-phase.  
**η** = per-unit efficiency, i.e. output kW / input kW  
**cos φ** = power factor, i.e. kW input / kVA input 

## Subtransient current and protection setting

  * Subtransient current peak value can be very high; typical value is about 12 to 15 times the rms rated value In. Sometimes this value can reach 25 times In.
  * Schneider Electric circuit-breakers, contactors and thermal relays are designed to withstand motor starts with very high subtransient current (subtransient peak value can be up to 19 times the rms rated value In).
  * If unexpected tripping of the overcurrent protection occurs during starting, this means the starting current exceeds the normal limits. As a result, some maximum switchgear withstands can be reached, life time can be reduced and even some devices can be destroyed. In order to avoid such a situation, oversizing of the switchgear must be considered.
  * Schneider Electric switchgears are designed to ensure the protection of motor starters against short-circuits. According to the risk, tables show the combination of circuit-breaker, contactor and thermal relay to obtain type 1 or type 2 coordination (see chapter [Characteristics of particular sources and loads](/enwiki/Characteristics_of_particular_sources_and_loads "Characteristics of particular sources and loads")).



## Motor starting current

Although high efficiency motors can be found on the market, in practice their starting currents are roughly the same as some of standard motors. The use of start-delta starter, static soft start unit or variable speed drive allows to reduce the value of the starting current (Example: 4 In instead of 7.5 In). 

See also "[Asynchronous motors](/enwiki/Asynchronous_motors "Asynchronous motors")" for more information. 

## Compensation of reactive-power (kvar) supplied to induction motors

It is generally advantageous for technical and financial reasons to reduce the current supplied to induction motors. This can be achieved by using capacitors without affecting the power output of the motors. 

The application of this principle to the operation of induction motors is generally referred to as “power-factor improvement” or “power-factor correction”. As discussed in chapter [Power Factor Correction](/enwiki/Power_Factor_Correction "Power Factor Correction"), the apparent power (kVA) supplied to an induction motor can be significantly reduced by the use of shunt-connected capacitors. Reduction of input kVA means a corresponding reduction of input current (since the voltage remains constant). 

Compensation of reactive-power is particularly advised for motors that operate for long periods at reduced power. 

As noted above cosφ=kW inputkVA input so that a kVA input reduction in kVA input will increase (i.e. improve) the value of cosφ 

The current supplied to the motor, after power-factor correction, is given by: 

I=Iacosφcosφ'

where cos φ is the power factor before compensation and cos φ' is the power factor after compensation, In being the original current. 

**Figure** A4 below shows, in function of motor rated power, standard motor current values for several voltage supplies (IEC 60947-4-1 Annex G). 

Fig. A4 – Rated operational power and currents

kW  | hp  | 230V  | 380 - 415V  | 400V  | 440- 480 V  | 500V  | 690V   
---|---|---|---|---|---|---|---  
A  | A  | A  | A  | A  | A   
0.18  
0.25  
0.37  | -  
-  
\-  | 1.0  
1.5  
1.9  | -  
-  
\-  | 0.6  
0.85  
1.1  | -  
-  
\-  | 0.48  
0.68  
0.88  | 0.35  
0.49  
0.64   
-  
0.55  
\-  | 1/2  
-  
3/4  | -  
2.6  
\-  | 1.3  
-  
1.8  | -  
1.5  
\-  | 1.1  
-  
1.6  | -  
1.2  
\-  | -  
0.87  
\-   
-  
0.75  
1.1  | 1  
-  
\-  | -  
3.3  
4.7  | 2.3  
-  
\-  | -  
1.9  
2.7  | 2.1  
-  
\-  | -  
1.5  
2.2  | -  
1.1  
1.6   
-  
-  
1.5  | 1-1/2  
2  
\-  | -  
-  
6.3  | 3.3  
4.3  
\-  | -  
-  
3.6  | 3.0  
3.4  
\-  | -  
-  
2.9  | -  
-  
2.1   
2.2  
-  
3.0  | -  
3  
\-  | 8.5  
-  
11.3  | -  
6.1  
\-  | 4.9  
-  
6.5  | -  
4.8  
\-  | 3.9  
-  
5.2  | 2.8  
-  
3.8   
4  
-  
5.5  | -  
5  
\-  | 15  
-  
20  | 9.7  
9.7  
\-  | 8.5  
-  
11.5  | 7.6  
7.6  
\-  | 6.8  
-  
9.2  | 4.9  
-  
6.7   
-  
-  
7.5  | 7-1/2  
10  
\-  | -  
-  
27  | 14.0  
18.0  
\-  | -  
-  
15.5  | 11.0  
14.0  
\-  | -  
-  
12.4  | -  
-  
8.9   
11  
-  
\-  | -  
15  
20  | 38.0  
-  
\-  | -  
27.0  
34.0  | 22.0  
-  
\-  | -  
21.0  
27.0  | 17.6  
-  
\-  | 12.8  
-  
\-   
15  
18.5  
\-  | -  
-  
25  | 51  
61  
\-  | -  
-  
44  | 39  
35  
\-  | -  
-  
34  | 23  
28  
\-  | 17  
21  
\-   
22  
-  
\-  | -  
30  
40  | 72  
-  
\-  | -  
51  
66  | 41  
-  
\-  | -  
40  
52  | 33  
-  
\-  | 24  
-  
\-   
30  
37  
\-  | -  
-  
50  | 96  
115  
\-  | -  
-  
83  | 55  
66  
\-  | -  
-  
65  | 44  
53  
\-  | 32  
39  
\-   
-  
45  
55  | 60  
-  
\-  | -  
140  
169  | 103  
-  
\-  | -  
80  
97  | 77  
-  
\-  | -  
64  
78  | -  
47  
57   
-  
-  
75  | 75  
100  
\-  | -  
-  
230  | 128  
165  
\-  | -  
-  
132  | 96  
124  
\-  | -  
-  
106  | -  
-  
77   
90  
-  
110  | -  
125  
\-  | 278  
-  
340  | -  
208  
\-  | 160  
-  
195  | -  
156  
| 128  
-  
156  | 93  
-  
113   
-  
132  
\-  | 150  
-  
200  | -  
400  
\-  | 240  
-  
320  | -  
230  
\-  | 180  
-  
240  | -  
184  
\-  | -  
134  
\-   
150  
160  
185  | -  
-  
\-  | -  
487  
\-  | -  
-  
\-  | -  
280  
\-  | -  
-  
\-  | -  
224  
\-  | -  
162  
\-   
-  
200  
220  | 250  
-  
\-  | -  
609  
\-  | 403  
-  
\-  | -  
350  
\-  | 302  
-  
\-  | -  
280  
\-  | -  
203  
\-   
-  
250  
280  | 300  
-  
\-  | -  
748  
\-  | 482  
-  
\-  | -  
430  
\-  | 361  
-  
\-  | -  
344  
\-  | -  
250  
\-   
-  
-  
300  | 350  
400  
\-  | -  
-  
\-  | 560  
636  
\-  | -  
-  
\-  | 414  
474  
\-  | -  
-  
\-  | -  
-  
\-   
315  
-  
335  | \-   
450  
\-  | 940  
-  
\-  | -  
\-   
\-  | 540  
-  
\-  | -  
515  
\-  | 432  
-  
\-  | 313  
-  
\-   
355  
-  
375  | -  
500  
\-  | 1061  
\-   
\-  | -  
786  
\-  | 610  
-  
\-  | \-   
590  
\-  | 488  
-  
\-  | 354  
-  
\-   
400  
425  
450  | -  
\-   
\-  | 1200  
-  
\-  | -  
\-   
\-  | 690  
\-   
\-  | -  
\-   
\-  | 552  
\-   
\-  | 400  
-  
\-   
475  
500  
530  | -  
-  
\-  | -  
1478  
\-  | -  
\-   
\-  | -  
850  
\-  | -  
-  
\-  | -  
680  
\-  | -  
493  
\-   
560  
600  
630  | -  
-  
\-  | 1652  
\-   
1844  | -  
-  
\-  | 950  
-  
1060  | -  
-  
\-  | 760  
-  
848  | 551  
-  
615   
670  
710  
750  | -  
\-   
\-  | -  
2070  
\-  | -  
-  
\-  | -  
1190  
\-  | -  
-  
\-  | -  
952  
\-  | -  
690  
\-   
800  
850   
900  | -  
\-   
\-  | 2340  
\-   
2640  | -  
\-   
\-  | 1346  
-  
1518  | -  
-  
\-  | 1076  
\-   
1214  | 780  
\-   
880   
950   
1000  | -  
\-  | \-   
2910  | -  
\-  | -  
1673  | -  
\-  | -  
1339  | -  
970   
  
Retrieved from "[https://www.electrical-installation.org/enw/index.php?title=Induction_motors&oldid=28161](https://www.electrical-installation.org/enw/index.php?title=Induction_motors&oldid=28161)"

[Categories](/enwiki/Special:Categories "Special:Categories"): 

  * [Chapter - General rules of electrical installation design](/enwiki/Category:Chapter_-_General_rules_of_electrical_installation_design "Category:Chapter - General rules of electrical installation design")
  * [Eig-content-pages](/enw/index.php?title=Category:Eig-content-pages&action=edit&redlink=1 "Category:Eig-content-pages \(page does not exist\)")

## See Also

- [[Module 4 — Single-Phase Induction Motors]]
- [[IEC Motor Testing — Map of Content]]

## Sources

- Scraped from web resources collected during [[IEC Motor Testing — Map of Content]] research
