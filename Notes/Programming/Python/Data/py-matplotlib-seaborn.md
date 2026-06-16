---
tags: [python, ml, visualization, matplotlib, seaborn, eda]
aliases: ["matplotlib", "seaborn", "plotting", "ml-matplotlib-seaborn"]
parent: "[[MOCs/Python — Map of Content]]"
created: 2026-06-11
status: complete
---

# L4 -- matplotlib & seaborn

## 80/20 Cheat Sheet

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Single plot -- the pattern
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(x, y, color='steelblue', linewidth=1.5, label='series')
ax.scatter(x, y, color='red', s=30)
ax.axhline(y=0.5, color='gray', linestyle='--')
ax.set_xlabel('X axis'); ax.set_ylabel('Y axis')
ax.set_title('Plot Title')
ax.legend(); ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('plot.png', dpi=150, bbox_inches='tight')
plt.show()

# Multiple subplots
fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
axes[0].plot(x, y1)
axes[1].plot(x, y2)
plt.tight_layout()

# Seaborn quick plots
sns.lineplot(data=df, x='cycle', y='temp', hue='unit')
sns.histplot(data=df, x='temp', hue='unit', bins=30)
sns.boxplot(data=df, x='unit', y='temp')
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0)
sns.pairplot(df, hue='label')
sns.kdeplot(data=df, x='temp', hue='unit', fill=True)
```

## matplotlib -- the two layers

**Figure** = the whole canvas. **Axes** = individual subplot panels within the canvas.

```python
import matplotlib.pyplot as plt
import numpy as np

# Single plot
cycles = np.arange(1, 51)
vibration = 0.4 + 0.005 * cycles + np.random.normal(0, 0.02, 50)

fig, ax = plt.subplots(figsize=(10, 4))

ax.plot(cycles, vibration, color='steelblue', linewidth=1.5, label='Vibration')
ax.axhline(y=0.6, color='red', linestyle='--', linewidth=1, label='Threshold')
ax.scatter([40, 45, 50], vibration[[39, 44, 49]],
           color='red', s=60, zorder=5, label='Alert')

ax.set_xlabel('Cycle')
ax.set_ylabel('Vibration (mm/s)')
ax.set_title('Engine 1 -- Vibration Trend')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('vibration.png', dpi=150, bbox_inches='tight')
plt.show()
```

## Multiple subplots

`plt.subplots(rows, cols)` returns `axes` as a numpy array. Flatten to iterate.

```python
cycles = np.arange(1, 51)
rng = np.random.default_rng(42)
temp = 480 + 0.1 * cycles + rng.normal(0, 2, 50)
pressure = 14.5 - 0.01 * cycles + rng.normal(0, 0.1, 50)
vib = 0.4 + 0.005 * cycles + rng.normal(0, 0.02, 50)

sensors = [temp, pressure, vib]
names = ['Temperature (C)', 'Pressure (bar)', 'Vibration (mm/s)']
colors = ['coral', 'teal', 'steelblue']

fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

for ax, sensor, name, color in zip(axes, sensors, names, colors):
    ax.plot(cycles, sensor, color=color, linewidth=1.2)
    ax.set_ylabel(name)
    ax.grid(True, alpha=0.3)

axes[-1].set_xlabel('Cycle')
fig.suptitle('Engine 1 -- All Sensor Readings', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('all_sensors.png', dpi=150)
plt.show()
```

## Plot types -- quick reference

```python
fig, ax = plt.subplots(figsize=(10, 5))

# Line
ax.plot(x, y)                                # line
ax.plot(x, y, 'o')                           # markers only
ax.plot(x, y, 'ro--')                        # red dashed with dots

# Scatter
ax.scatter(x, y, c=colors, s=sizes, alpha=0.6)

# Bar
ax.bar(categories, values)
ax.barh(categories, values)                  # horizontal

# Histogram
ax.hist(values, bins=30, alpha=0.7, edgecolor='black')
ax.hist(values, bins=30, density=True)       # normalized

# Boxplot
ax.boxplot([group1, group2], labels=['A', 'B'])

# Fill between
ax.fill_between(x, y_lower, y_upper, alpha=0.2)

# Vertical/horizontal lines
ax.axvline(x=42, color='red', linestyle='--')
ax.axhline(y=0.5, color='gray', linewidth=0.5)
```

**Trap:** `ax.hist` is for raw data distribution. `ax.bar` is for pre-computed values.

## Customization

```python
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, y)

# Colors
# Basic: 'red', 'blue', 'green', 'black', 'white'
# Named: 'steelblue', 'coral', 'teal', 'crimson', 'forestgreen'
# Hex:   '#ff5733'
# RGB:   (0.1, 0.5, 0.8)

# Styles
# '-', '--', '-.', ':', 'None', ' '
# Markers: 'o', 's', '^', 'D', 'v', 'x', '+'

# Axis limits
ax.set_xlim(0, 100); ax.set_ylim(-1, 1)
ax.set_xscale('log'); ax.set_yscale('log')

# Text
ax.text(x, y, 'label', fontsize=10, ha='center')
ax.annotate('peak', xy=(50, 0.6), xytext=(60, 0.8),
            arrowprops=dict(arrowstyle='->'))

# Ticks
ax.set_xticks([0, 25, 50, 75, 100])
ax.set_xticklabels(['0', '25', '50', '75', '100'], rotation=45)

# Grid
ax.grid(True, which='both', alpha=0.3)

# Legend outside
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
```

## seaborn -- statistical plots from DataFrames

Seaborn's main advantage: takes DataFrames directly with column names. Three lines for a publication-quality plot.

```python
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)
df = pd.DataFrame({
    'unit': [1]*50 + [2]*50,
    'cycle': list(range(1, 51))*2,
    'vib': np.concatenate([
        0.4 + 0.005*np.arange(50) + rng.normal(0, 0.02, 50),   # engine 1
        0.38 + 0.001*np.arange(50) + rng.normal(0, 0.02, 50)   # engine 2
    ]),
    'temp': np.concatenate([
        480 + 0.1*np.arange(50) + rng.normal(0, 2, 50),
        477 + 0.02*np.arange(50) + rng.normal(0, 2, 50),
    ]),
    'label': [0]*45 + [1]*5 + [0]*50
})

# Line plot (with confidence bands)
sns.lineplot(data=df, x='cycle', y='vib', hue='unit')
plt.show()

# Distribution
sns.histplot(data=df, x='vib', hue='unit', bins=20, alpha=0.6)
sns.kdeplot(data=df, x='vib', hue='unit', fill=True)

# Boxplot
sns.boxplot(data=df, x='unit', y='vib')

# Violin (boxplot + density)
sns.violinplot(data=df, x='unit', y='vib')

# Correlation heatmap
fig, ax = plt.subplots(figsize=(6, 5))
corr = df[['vib', 'temp', 'cycle', 'label']].corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm',
            center=0, square=True, ax=ax)
ax.set_title('Correlation Matrix')
plt.tight_layout()

# Pairplot (all numeric columns against each other)
sns.pairplot(df, hue='label', corner=True)

# Count plot (for categorical)
sns.countplot(data=df, x='label')
sns.countplot(data=df, x='unit', hue='label')
```

## seaborn themes and styles

```python
# Global style (call once at top of script)
sns.set_theme(style='darkgrid')
# styles: 'darkgrid', 'whitegrid', 'dark', 'white', 'ticks'

# Context (affects font sizes)
sns.set_context('paper')                     # small fonts
sns.set_context('notebook')                  # default
sns.set_context('talk')                      # larger (presentations)
sns.set_context('poster')                    # largest

# Color palettes
sns.set_palette('husl')
sns.set_palette('Set2')
sns.set_palette('colorblind')
sns.set_palette('Blues')                     # sequential
sns.color_palette('coolwarm', as_cmap=True)  # diverging
```

**Note:** As of matplotlib 3.6+, seaborn styles shipped in matplotlib are deprecated. Use `sns.set_theme()` directly instead of `plt.style.use('seaborn')`.

## Common plots for ML workflows

```python
# Confusion matrix heatmap
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_true, y_pred)
fig, ax = plt.subplots(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
            xticklabels=['normal', 'anomaly'],
            yticklabels=['normal', 'anomaly'])
ax.set_xlabel('Predicted'); ax.set_ylabel('Actual')
ax.set_title('Confusion Matrix')

# Feature importance
importances = rf.feature_importances_
features = ['temp', 'pressure', 'vib']
fig, ax = plt.subplots(figsize=(8, 4))
ax.barh(features, importances, color='steelblue')
ax.set_xlabel('Importance'); ax.set_title('Feature Importances')
plt.tight_layout()

# ROC curve
from sklearn.metrics import roc_curve
fpr, tpr, _ = roc_curve(y_true, y_prob)
fig, ax = plt.subplots(figsize=(6, 5))
ax.plot(fpr, tpr, linewidth=2, label=f'ROC (AUC={roc_auc:.3f})')
ax.plot([0, 1], [0, 1], 'k--', alpha=0.5)
ax.set_xlabel('False Positive Rate'); ax.set_ylabel('True Positive Rate')
ax.set_title('ROC Curve'); ax.legend(); ax.grid(True, alpha=0.3)
plt.tight_layout()

# Precision-Recall curve
from sklearn.metrics import precision_recall_curve
prec, rec, _ = precision_recall_curve(y_true, y_prob)
fig, ax = plt.subplots(figsize=(6, 5))
ax.plot(rec, prec, linewidth=2, label=f'PR (AUC={pr_auc:.3f})')
ax.set_xlabel('Recall'); ax.set_ylabel('Precision')
ax.set_title('Precision-Recall Curve'); ax.legend()
ax.grid(True, alpha=0.3)

# Time series with anomaly highlights
fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(df['cycle'], df['vib'], color='steelblue', label='Vibration')
anomalies = df[df['label'] == 1]
ax.scatter(anomalies['cycle'], anomalies['vib'],
           color='red', s=50, label='Anomaly', zorder=5)
ax.legend(); ax.set_xlabel('Cycle'); ax.set_ylabel('Vibration')
ax.set_title('Vibration with Anomaly Highlights')
```

## Styling for publications/dashboards

```python
# Consistent style
sns.set_theme(style='whitegrid', context='paper')
plt.rcParams.update({
    'font.size': 11,
    'axes.titlesize': 12,
    'axes.labelsize': 11,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})

# Colorblind-friendly palette
sns.set_palette('colorblind')
```

## Common traps

```python
# TRAP 1: savefig BEFORE show -- show clears the figure
plt.plot(x, y)
plt.savefig('plot.png')    # save FIRST
plt.show()                 # then show

# TRAP 2: Forgetting tight_layout() -- labels get cut off
plt.tight_layout()          # call before savefig
plt.savefig('plot.png')     # after tight_layout

# TRAP 3: Multiple figures -- close unused ones
fig1, ax1 = plt.subplots()
# ... do stuff ...
fig2, ax2 = plt.subplots()  # fig1 still open, memory accumulates
plt.close(fig1)             # close when done

# TRAP 4: seaborn style + matplotlib customisation mismatch
sns.set_theme(style='darkgrid')
# Now all matplotlib calls also use seaborn style -- consistent

# TRAP 5: plt.subplots(3, 1) returns axes as [ax1, ax2, ax3] (1D for 1 row/col)
# plt.subplots(2, 2) returns axes as [[ax1, ax2], [ax3, ax4]] (2D)
# Use axes.flatten() to handle uniformly

# TRAP 6: Scatter with many points is slow -- use rasterization
ax.scatter(x, y, rasterized=True)

# TRAP 7: Heatmap on large correlation matrix
# Don't show all features. Select a subset for readability.
```
