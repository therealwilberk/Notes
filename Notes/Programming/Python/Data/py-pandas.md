---
tags: [python, pandas, dataframe, data-wrangling]
aliases: ["pandas", "pandas Refresher", "ml-pandas"]
parent: "[[MOCs/Python — Map of Content]]"
created: 2026-06-11
status: complete
---

# pandas

## Why pandas

NumPy gives you arrays. Pandas gives you labeled columns, mixed dtypes, missing data, and group operations. In ML work, you load raw data into a DataFrame, clean it, engineer features with groupby/rolling/merge, then extract the numpy array for the model.

```python
import pandas as pd
import numpy as np
```

## The DataFrame

A DataFrame is a collection of Series (columns) sharing the same index. Each column has one dtype.

```python
df = pd.DataFrame({
    'unit':     [1, 1, 1, 2, 2, 2],
    'cycle':    [1, 2, 3, 1, 2, 3],
    'temp':     [480.2, 481.5, 495.3, 476.8, 478.1, 479.0],
    'vib':      [0.42, 0.45, 0.61, 0.38, 0.40, 0.41],
    'op':       ['A', 'A', 'A', 'B', 'B', 'B'],
})

df.shape                             # (6, 5)
df.dtypes                            # int64, int64, float64, float64, object
df.info()                            # types + non-null count + memory
df.describe()                        # summary stats for numeric cols
df.head(); df.tail(); df.sample(5)
```

**All datasets in this note** use turbofan sensor data: multiple engine units, each with a cycle counter, temperature, vibration, and operating mode.

## Select — The Three Patterns

```python
# Single column → Series
df['temp']

# Multiple columns → DataFrame
df[['unit', 'temp']]

# By label (inclusive) vs by position (exclusive)
df.loc[0, 'temp']                    # row label 0, column 'temp'
df.iloc[0, 0]                        # first row, first column
df.loc[0:2]                          # rows 0, 1, 2 — inclusive!
df.iloc[0:2]                         # rows 0, 1 — exclusive right
```

**Trap:** `.loc` includes the end index. `.iloc` excludes it. This off-by-one got me three times before I memorised it.

## Filter — Boolean Indexing

```python
df[df['temp'] > 485]

# Multiple conditions: use &, not 'and'. Wrap each condition in ().
df[(df['unit'] == 1) & (df['vib'] > 0.5)]

# List membership
df[df['op'].isin(['A'])]

# Negative
df[~df['unit'].isin([2])]
```

## The Silent Bug — Views vs Copies

```python
unit1 = df[df['unit'] == 1]
unit1['new_col'] = 5                 # SettingWithCopyWarning — might not work
```

This is the most common pandas trap. Filtering returns a view or a copy depending on internal state. You can't tell which. Fix it with one word:

```python
unit1 = df[df['unit'] == 1].copy()
unit1['new_col'] = 5                 # safe
```

Rule: call `.copy()` whenever you create a subset that you intend to modify.

## groupby — The Engine of Feature Engineering

groupby splits the DataFrame into groups, applies a function to each, and combines the results.

```python
# Per-group aggregate — returns a smaller DataFrame
df.groupby('unit')['temp'].mean()    # mean temp per engine
df.groupby('unit').agg(
    mean_temp=('temp', 'mean'),
    max_vib=('vib', 'max'),
    total_life=('cycle', 'max'),
)
```

The ML workhorse — `transform`. It returns the same shape as the original, so you can add per-group stats as a new column.

```python
df['unit_max_cycle'] = df.groupby('unit')['cycle'].transform('max')
df['RUL'] = df['unit_max_cycle'] - df['cycle']   # remaining useful life
df['vib_deviation'] = df.groupby('unit')['vib'].transform(
    lambda x: x - x.mean()
)
```

## Rolling Windows — Time Series Features

Always group by entity before rolling. Otherwise you roll across boundaries.

```python
# Correct: roll within each engine
df['vib_roll_mean'] = (
    df.groupby('unit')['vib']
    .transform(lambda s: s.rolling(3, min_periods=1).mean())
)

# Lag and diff
df['vib_lag1'] = df.groupby('unit')['vib'].shift(1)
df['vib_diff1'] = df.groupby('unit')['vib'].diff(1)
```

**Trap:** Always sort by time before rolling. `df.sort_values(['unit', 'cycle'])`.

## Merge — Joining Datasets

```python
engine_info = pd.DataFrame({
    'unit': [1, 2],
    'model': ['CFM56', 'GE90'],
})

# Left join: keep all readings, attach engine info where available
merged = readings.merge(engine_info, on='unit', how='left')

# Concat rows
combined = pd.concat([df1, df2], ignore_index=True)
```

## Handling Missing Values

```python
df.isnull().sum()                    # count per column

# Fill strategies
df['temp'].fillna(method='ffill')    # forward fill — use for sensor dropout
df['temp'].fillna(df['temp'].mean()) # column mean — use when sensor is optional
df['temp'].interpolate()             # linear — use for short gaps

# Correct for panel data: ffill within each group
df['temp'] = (
    df.sort_values(['unit', 'cycle'])
    .groupby('unit')['temp']
    .transform(lambda s: s.ffill())
)
```

## The Patterns You'll Use in Every ML Project

```python
# Load
df = pd.read_csv('sensor_data.csv')

# Inspect
df.info(); df.describe(); df.isnull().sum()

# Feature engineering — per-unit stats
df['max_cycle'] = df.groupby('unit')['cycle'].transform('max')
df['RUL'] = df['max_cycle'] - df['cycle']
df['vib_roll'] = df.groupby('unit')['vib'].transform(
    lambda s: s.rolling(5, min_periods=1).mean()
)

# Extract numpy for sklearn
X = df[['cycle', 'temp', 'vib', 'vib_roll']].values
y = df['label'].values
```

## 80/20 Reference

```python
import pandas as pd
import numpy as np

# Load
df = pd.read_csv('file.csv')
df.shape; df.dtypes; df.info(); df.describe()

# Select
df['col']; df[['a', 'b']]
df.loc[0, 'col']; df.iloc[0, 0]

# Filter
df[df['col'] > 5]
df[(df['a'] > 0) & (df['b'] < 5)]

# Fix SettingWithCopyWarning
subset = df[df['unit'] == 1].copy()

# Groupby
df.groupby('unit')['temp'].mean()
df.groupby('unit').agg(mean_temp=('temp', 'mean'))
df['stat'] = df.groupby('unit')['col'].transform('mean')

# Rolling (always groupby first)
df['roll'] = df.groupby('unit')['col'].transform(
    lambda s: s.rolling(3, min_periods=1).mean()
)

# Merge
df.merge(other, on='key', how='left')

# Nulls
df.isnull().sum()
df['col'].fillna(method='ffill')

# Export
df.to_csv('out.csv', index=False)
```
