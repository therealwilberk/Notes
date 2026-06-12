---
tags: [ml, pandas, dataframe, data-wrangling]
aliases: ["pandas", "pandas Refresher"]
parent: "[[ML & Data Science Packages — Map of Content]]"
created: 2026-06-11
status: complete
---

# L2 -- pandas

## 80/20 Cheat Sheet

```python
import pandas as pd
import numpy as np

# Load & inspect
df = pd.read_csv('file.csv')
df.shape; df.dtypes; df.head(); df.tail(3)
df.info(); df.describe(); df.isnull().sum()

# Select
df['col']                                    # Series
df[['col1', 'col2']]                         # DataFrame
df.loc[0, 'col']                             # by label (inclusive)
df.iloc[0, 0]                                # by position (exclusive right)
df.iloc[:, 2]                                # all rows, third column

# Filter
df[df['col'] > value]                        # boolean
df[(df['a'] > 0) & (df['b'] < 5)]            # AND
df[(df['a'] > 0) | (df['b'] < 5)]            # OR
df[df['col'].isin(['A', 'B'])]               # in list

# Create columns
df['new'] = df['a'] / df['b']                # vectorised
df['new'] = np.where(df['a'] > 5, 'high', 'low')
df['new'] = df['col'].apply(lambda x: x + 1) # row-by-row

# Groupby
df.groupby('unit')['col'].mean()             # per-group aggregate
df.groupby('unit').agg(                      # named aggregations
    mean_temp=('temp', 'mean'),
    max_cycle=('cycle', 'max')
)
df['stat'] = df.groupby('unit')['col'].transform('mean')  # broadcast back

# Rolling (ALWAYS groupby first for panel data)
df['roll'] = df.groupby('unit')['col'].transform(
    lambda s: s.rolling(3, min_periods=1).mean()
)

# Merge
df.merge(other_df, on='key', how='left')     # SQL-style join

# Handle nulls
df.isnull().sum()
df['col'].fillna(df['col'].mean())           # fill with mean
df['col'].fillna(method='ffill')             # forward fill
df.dropna()                                  # drop rows with any NaN
df.dropna(subset=['col'])                    # drop if NaN in specific col

# Sort & rank
df.sort_values('col', ascending=False)
df['rank'] = df.groupby('unit')['cycle'].rank()

# Unique & counts
df['col'].unique(); df['col'].nunique()
df['col'].value_counts(); df['col'].value_counts(normalize=True)

# Pivot
pd.pivot_table(df, values='temp', index='unit', columns='cycle')

# Export
df.to_csv('out.csv', index=False)
```

## Creating and loading DataFrames

```python
# From dict -- key = column name, value = list
df = pd.DataFrame({
    'unit':     [1, 1, 1, 2, 2, 2],
    'cycle':    [1, 2, 3, 1, 2, 3],
    'temp':     [480.2, 481.5, 495.3, 476.8, 478.1, 479.0],
    'pressure': [14.3, 14.1, 13.8, 14.5, 14.4, 14.2],
    'vib':      [0.42, 0.45, 0.61, 0.38, 0.40, 0.41],
    'op':       ['A', 'A', 'A', 'B', 'B', 'B'],
    'label':    [0, 0, 1, 0, 0, 0],
})

# From numpy array
np_data = np.random.randn(100, 5)
df = pd.DataFrame(np_data, columns=['a', 'b', 'c', 'd', 'e'])

# From CSV
df = pd.read_csv('train.csv')
df = pd.read_csv('train.csv', parse_dates=['timestamp'], index_col='id')
df = pd.read_csv('train.csv', dtype={'unit': 'int32'})  # save memory

# Essential inspection calls -- always run these
df.shape                                      # (1000, 50) -- rows, cols
df.dtypes                                     # column types
df.info()                                     # types + non-null count + memory
df.describe()                                 # stats for numeric cols
df.head(10); df.tail(5)                       # preview
df.sample(5)                                  # random rows
df.isnull().sum()                             # missing count per column
df['unit'].nunique()                          # unique values in column
```

## .loc vs .iloc -- the confusion explained

```python
df = pd.DataFrame({'temp': [480, 481, 495], 'vib': [0.42, 0.45, 0.61]},
                   index=[10, 20, 30])        # non-default index

# .iloc -- position based, Python slice rules (exclusive right)
df.iloc[0]                                    # first row (temp=480)
df.iloc[0:2]                                  # rows at positions 0,1
df.iloc[:, 0]                                 # first column (position 0)
df.iloc[0, 1]                                 # row 0, col 1 -> 0.45

# .loc -- label based, INCLUSIVE right
df.loc[10]                                    # row with index label 10
df.loc[10:20]                                 # rows 10 AND 20 (inclusive!)
df.loc[:, 'temp']                             # column 'temp'
df.loc[10, 'vib']                             # row 10, col 'vib' -> 0.45
```

**Trap:** `.loc` includes the end index. `.iloc` excludes it. This is the most common source of off-by-one errors in pandas.

## Boolean filtering patterns

```python
# Single condition
df[df['temp'] > 485]

# Multiple conditions -- use & (not 'and'), | (not 'or'), wrap each in ()
df[(df['unit'] == 1) & (df['label'] == 1)]
df[(df['vib'] > 0.5) | (df['temp'] > 490)]

# .query() -- sometimes cleaner for complex conditions
df.query('unit == 1 and label == 1')
df.query('temp > 480 and vib > 0.5')
df.query('unit in [1, 2]')

# .isin() for list membership
df[df['unit'].isin([1, 3, 5])]
df[df['op'].isin(['A', 'C'])]

# Negative filter
df[~df['unit'].isin([2])]

# .between()
df[df['temp'].between(475, 485)]
```

## Creating and modifying columns

```python
# Vectorised operations
df['ratio'] = df['temp'] / df['pressure']
df['log_temp'] = np.log(df['temp'])
df['vib_sq'] = df['vib'] ** 2

# Conditional with np.where
df['is_alert'] = np.where(df['vib'] > 0.5, 1, 0)
df['status'] = np.where(df['temp'] > 485, 'hot',
                np.where(df['temp'] > 480, 'warm', 'normal'))

# .apply() -- when vectorised isn't possible
df['desc'] = df['vib'].apply(lambda x: 'high' if x > 0.5 else 'low')

# Multiple columns with apply
df['category'] = df.apply(
    lambda row: 'fault' if row['vib'] > 0.5 and row['temp'] > 490 else 'normal',
    axis=1                                    # axis=1 = row-wise
)

# Dropping
df.drop(columns=['log_temp', 'vib_sq'])      # returns new df
df.drop(columns=['col'], inplace=True)        # modifies in place

# Renaming
df = df.rename(columns={'temp': 'sensor_temp', 'vib': 'sensor_vib'})

# Reordering columns
df = df[['unit', 'cycle', 'temp', 'vib', 'label']]

# Type casting
df['unit'] = df['unit'].astype('int32')
df['date'] = pd.to_datetime(df['date'])
```

## groupby -- the engine of feature engineering

```python
# Basic aggregation
df.groupby('unit')['temp'].mean()             # mean per engine
df.groupby('unit')['cycle'].max()             # max cycle = total life
df.groupby('unit')['label'].sum()             # anomaly count per engine

# Multiple columns, named outputs
summary = df.groupby('unit').agg(
    mean_temp = ('temp', 'mean'),
    max_vib   = ('vib',  'max'),
    min_vib   = ('vib',  'min'),
    total_life = ('cycle', 'max'),
    anomalies = ('label', 'sum'),
)

# Same aggregation on multiple columns
df.groupby('unit')[['temp', 'vib']].agg(['mean', 'std', 'max'])

# Multiple aggs per column
stats = df.groupby('op')['temp'].agg(['count', 'mean', 'std', 'min', 'max'])

# transform() -- critical for adding per-group stats as a column
# Returns same shape as original
df['unit_max_cycle'] = df.groupby('unit')['cycle'].transform('max')
df['RUL'] = df['unit_max_cycle'] - df['cycle']

# transform with custom function
df['vib_deviation'] = df.groupby('unit')['vib'].transform(
    lambda x: x - x.mean()
)

# groupby + apply for complex logic
def add_features(group):
    group['temp_range'] = group['temp'].max() - group['temp'].min()
    group['vib_change'] = group['vib'].diff()
    return group

df = df.groupby('unit', group_keys=False).apply(add_features)
```

## Rolling windows -- essential for time series

```python
# WRONG -- rolls across engine boundaries
df['vib_roll_bad'] = df['vib'].rolling(3).mean()

# CORRECT -- roll within each engine
df['vib_roll_mean'] = (df.groupby('unit')['vib']
                       .transform(lambda s: s.rolling(3, min_periods=1).mean()))
df['vib_roll_std'] = (df.groupby('unit')['vib']
                      .transform(lambda s: s.rolling(3, min_periods=1).std()))
df['vib_roll_max'] = (df.groupby('unit')['vib']
                      .transform(lambda s: s.rolling(3, min_periods=1).max()))

# Shift for lag features
df['vib_lag1'] = df.groupby('unit')['vib'].shift(1)
df['vib_lag2'] = df.groupby('unit')['vib'].shift(2)

# Diff for change features
df['vib_diff1'] = df.groupby('unit')['vib'].diff(1)

# Expanding window (all history up to current point)
df['vib_expand_mean'] = df.groupby('unit')['vib'].transform(
    lambda s: s.expanding().mean()
)
df['vib_expand_max'] = df.groupby('unit')['vib'].transform(
    lambda s: s.expanding().max()
)
```

**Always sort by time before rolling/diff/shift.** `df.sort_values(['unit', 'cycle'])`.

## Merging and joining

```python
engine_info = pd.DataFrame({
    'unit':  [1, 2],
    'model': ['CFM56', 'GE90'],
    'year':  [2018, 2020],
})

readings = pd.DataFrame({
    'unit':  [1, 1, 1, 2, 2],
    'cycle': [1, 2, 3, 1, 2],
    'temp':  [480, 481, 495, 477, 478],
})

# Left join -- keep all readings, attach engine info
merged = readings.merge(engine_info, on='unit', how='left')

# Inner join -- only units in both
inner = readings.merge(engine_info, on='unit', how='inner')

# Merge on different column names
readings.merge(engine_info, left_on='unit', right_on='engine_id', how='left')

# Concat rows (append)
more_data = pd.DataFrame({'unit': [3, 3], 'cycle': [1, 2], 'temp': [490, 492]})
combined = pd.concat([readings, more_data], ignore_index=True)

# Concat columns
features = pd.DataFrame({'vib_roll_mean': [0.44, 0.51], 'vib_roll_std': [0.02, 0.08]})
combined_cols = pd.concat([readings, features], axis=1)
```

## Handling missing values

```python
df = pd.DataFrame({
    'unit': [1, 1, 1, 2, 2],
    'cycle': [1, 2, 3, 1, 2],
    'temp': [480.2, None, 495.3, 476.8, 478.1],
    'vib': [0.42, 0.45, None, 0.38, 0.40],
})

# Detect
df.isnull()                                  # mask
df.isnull().sum()                            # count per column
df.isnull().sum().sum()                      # total NaN count
df[df['temp'].isnull()]                      # rows with NaN in temp

# Fill strategies
df['temp'].fillna(df['temp'].mean())         # column mean
df['temp'].fillna(method='ffill')            # forward fill (last valid)
df['temp'].fillna(method='bfill')            # backward fill
df['temp'].fillna(0)                         # with constant
df['temp'].interpolate(method='linear')      # linear interpolation

# Correct for sensor data: ffill within each engine
df['temp'] = (df.sort_values(['unit', 'cycle'])
              .groupby('unit')['temp']
              .transform(lambda s: s.ffill()))

# Drop
df.dropna()                                  # row with any NaN
df.dropna(subset=['temp'])                   # rows where temp is NaN
df.dropna(thresh=2)                          # rows with at least 2 non-NaN
df.dropna(axis=1)                            # columns with any NaN
```

## Pivot tables

```python
df = pd.DataFrame({
    'unit': [1, 1, 2, 2],
    'cycle': [1, 2, 1, 2],
    'temp': [480, 481, 477, 478],
    'vib': [0.42, 0.45, 0.38, 0.40],
})

# Pivot: one value per cell (no duplicates)
df.pivot(index='cycle', columns='unit', values='temp')

# Pivot table: aggregate if duplicates exist
pd.pivot_table(df, values='temp', index='cycle', columns='unit', aggfunc='mean')

# Melt: unpivot wide to long
wide = pd.DataFrame({'unit': [1, 2], 'cycle_1': [480, 477], 'cycle_2': [481, 478]})
long = wide.melt(id_vars=['unit'], var_name='cycle', value_name='temp')
```

## Common traps

```python
# TRAP 1: SettingWithCopyWarning
unit1 = df[df['unit'] == 1]
unit1['new_col'] = 5          # WARNING -- ambiguous, might not work
# Fix:
unit1 = df[df['unit'] == 1].copy()
unit1['new_col'] = 5          # safe

# TRAP 2: Chained indexing
# Avoid: df[df['unit'] == 1]['temp'][0]
# Use:   df.loc[df['unit'] == 1, 'temp'].iloc[0]

# TRAP 3: Forgetting reset_index after filtering
subset = df[df['unit'] == 1]
subset.index                   # original indices
subset = subset.reset_index(drop=True)  # now 0, 1, 2...

# TRAP 4: Single vs double brackets
s = df['temp']                          # Series (1D)
df2 = df[['temp']]                      # DataFrame (2D) -- sklearn needs this

# TRAP 5: inplace=True issues
# Some methods return None when inplace=True. Can't chain.
# Prefer: df = df.drop(columns=['x']) over df.drop(columns=['x'], inplace=True)

# TRAP 6: apply is slow -- vectorise when possible
# Fast: df['ratio'] = df['a'] / df['b']
# Slow: df['ratio'] = df.apply(lambda r: r['a'] / r['b'], axis=1)
```
