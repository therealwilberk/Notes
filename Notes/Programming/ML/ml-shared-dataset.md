---
tags: [ml, dataset, turbofan, reference]
aliases: ["Shared Dataset", "Turbofan Sensor Data"]
parent: "[[ML & Data Science Packages — Map of Content]]"
created: 2026-06-11
status: complete
---

# The Shared Dataset

I use this same simulated turbofan sensor dataset across every library example. Saves me from re-explaining the data every time.

## Schema

```
unit | cycle | sensor_temp | sensor_pressure | sensor_vibration | op_setting | label
-----|-------|-------------|-----------------|------------------|------------|------
  1  |   1   |    480.2    |      14.3       |       0.42       |     A      |   0
  1  |   2   |    481.5    |      14.1       |       0.45       |     A      |   0
  1  |   3   |    495.3    |      13.8       |       0.61       |     A      |   1  <-- anomaly
  2  |   1   |    476.8    |      14.5       |       0.38       |     B      |   0
  2  |   2   |    478.1    |      14.4       |       0.40       |     B      |   0
  2  |   3   |    479.0    |      14.2       |       0.41       |     B      |   0
```

- **unit** -- engine ID (1, 2, 3...)
- **cycle** -- time step within that engine's run
- **sensor_temp / sensor_pressure / sensor_vibration** -- three sensor readings
- **op_setting** -- operating condition (A or B)
- **label** -- 0 = normal, 1 = anomaly

## As a numpy array

```python
import numpy as np

sensors = np.array([
    [480.2, 14.3, 0.42],     # unit 1, cycle 1 -- normal
    [481.5, 14.1, 0.45],     # unit 1, cycle 2 -- normal
    [495.3, 13.8, 0.61],     # unit 1, cycle 3 -- anomaly (temp spike + vib spike)
    [476.8, 14.5, 0.38],     # unit 2, cycle 1 -- normal
    [478.1, 14.4, 0.40],     # unit 2, cycle 2 -- normal
    [479.0, 14.2, 0.41],     # unit 2, cycle 3 -- normal
])

labels = np.array([0, 0, 1, 0, 0, 0])
```

## As a pandas DataFrame

```python
import pandas as pd

df = pd.DataFrame({
    'unit':              [1, 1, 1, 2, 2, 2],
    'cycle':             [1, 2, 3, 1, 2, 3],
    'sensor_temp':       [480.2, 481.5, 495.3, 476.8, 478.1, 479.0],
    'sensor_pressure':   [14.3,  14.1,  13.8,  14.5,  14.4,  14.2],
    'sensor_vibration':  [0.42,  0.45,  0.61,  0.38,  0.40,  0.41],
    'op_setting':        ['A',   'A',   'A',   'B',   'B',   'B'],
    'label':             [0,     0,     1,     0,     0,     0],
})
```

Each library file may create a bigger version with more synthetic data, but the column layout stays the same.
