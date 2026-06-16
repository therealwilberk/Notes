---
tags: [python, numpy, arrays, numerical]
aliases: ["NumPy", "NumPy Refresher", "ml-numpy"]
parent: "[[MOCs/Python — Map of Content]]"
created: 2026-06-11
status: complete
---

# NumPy

## Why NumPy

Python lists are flexible but slow. NumPy arrays are fixed-type, contiguous blocks of memory. A loop over a million elements runs in C, not Python. That's the whole game.

```python
import numpy as np
```

## The Array

An ndarray has three properties: `shape`, `dtype`, `ndim`.

```python
np.array([1, 2, 3]).shape       # (3,)
np.array([[1, 2], [3, 4]]).shape  # (2, 2)
np.array([1, 2, 3]).dtype         # int64
np.array([1.0, 2.0]).dtype        # float64
```

Shape tells you everything. `(3,)` is a 1D vector. `(100, 5)` is 100 rows, 5 columns. `(10, 224, 224, 3)` is 10 RGB images.

## Creating Arrays

You will use about four constructors regularly. The rest you can look up.

```python
np.zeros((3, 4))                  # 3x4 of zeros -- great for initialisation
np.ones((100,))                   # 100 ones -- bias terms, masks
np.arange(0, 10, 2)               # [0, 2, 4, 6, 8] -- index generation
np.linspace(0, 1, 5)              # [0, 0.25, 0.5, 0.75, 1.] -- evenly spaced
```

**Random arrays** — the modern API uses a Generator. Always seed it for reproducible pipelines.

```python
rng = np.random.default_rng(42)   # seed once, reuse
rng.normal(0, 1, size=(100, 5))   # 100x5 from standard normal
rng.uniform(0, 1, size=50)        # uniform [0, 1)
rng.integers(0, 10, size=20)      # random integers
```

**The old API** (`np.random.seed(42)` + `np.random.rand`) still works. Avoid it in new code — it mutates global state.

## Indexing

The few patterns you'll reach for repeatedly:

```python
a = np.array([10, 20, 30, 40, 50])

a[0]                              # first
a[-1]                             # last
a[1:4]                            # slice — view, not copy
a[[0, 2, 4]]                      # fancy indexing — copy, not view
```

For 2D:

```python
m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
m[1, 2]                           # row 1, col 2 → 6
m[:, 0]                           # first column — view
m[0:2, 1:3]                       # submatrix — view
```

The ML workhorse — boolean masking:

```python
data = np.array([1.2, 0.8, 2.5, -0.3, 1.7])
data[data > 1.0]                  # [1.2, 2.5, 1.7]

# Combine with &, not and
data[(data > 0) & (data < 2)]     # [1.2, 0.8, 1.7]
```

## The Axis Trap

`axis=0` means "collapse rows" — operate along the vertical direction. `axis=1` means "collapse columns" — operate horizontally.

```python
m = np.array([[1, 2, 3],
              [4, 5, 6]])

m.sum(axis=0)                     # [5, 7, 9]   — column totals
m.sum(axis=1)                     # [6, 15]     — row totals
m.mean(axis=0)                    # [2.5, 3.5, 4.5]
```

I still pause on this. The mental model: axis=0 is the first dimension in the shape tuple. `m.shape` is `(2, 3)`, so `axis=0` operates on the size-2 dimension.

## Broadcasting

Broadcasting lets NumPy operate on arrays of different shapes. It "stretches" the smaller one to match.

```python
m = np.array([[1, 2, 3], [4, 5, 6]])    # shape (2, 3)
v = np.array([10, 20, 30])              # shape (3,) — broadcasts
m + v                                    # [[11, 22, 33], [14, 25, 36]]
```

This is not magic. The rule: dimensions are compatible if they are equal or one of them is 1.

**Trap:** `(5,)` and `(5, 1)` broadcast differently.

```python
a = np.array([1, 2, 3])                # shape (3,)
a[:, np.newaxis]                        # shape (3, 1) — column vector
a[np.newaxis, :]                        # shape (1, 3) — row vector
```

**Trap:** Many sklearn models require 2D input. A column vector is `reshape(-1, 1)`. A 1D array of shape `(5,)` will fail silently or unexpectedly.

## Copy vs View — The Silent Bug

Slicing returns a view, not a copy. Modify the view and you modify the original.

```python
m = np.array([[1, 2, 3], [4, 5, 6]])
col = m[:, 0]                         # view
col[0] = 999                          # m[0, 0] is now 999
```

This cost me an hour once. Fix it:

```python
col_copy = m[:, 0].copy()             # safe
```

Fancy indexing and boolean indexing return copies. When in doubt, call `.copy()`.

## Shape Manipulation

Reshape is zero-cost — it only changes the metadata, not the data.

```python
a = np.arange(12)                     # [0..11], shape (12,)
a.reshape(3, 4)                       # 3x4
a.reshape(2, -1)                      # 2x6 — -1 infers the dimension
```

Use `-1` liberally. It computes the dimension so you don't have to.

## The ML Pipeline Pattern

The numpy operations you'll use in every ML project:

```python
# Load a CSV as numpy (realistically you'd use pandas, but bare numpy):
data = np.genfromtxt("sensor.csv", delimiter=",", skip_header=1)
X = data[:, :-1]                      # all rows, all cols except last
y = data[:, -1]                       # all rows, last col (target)

# Standardise (z-score)
mean = X.mean(axis=0)
std = X.std(axis=0)
X_scaled = (X - mean) / std           # broadcasting

# Train/test split (manual)
np.random.seed(42)
idx = np.random.permutation(len(X))
split = int(0.8 * len(X))
train_idx, test_idx = idx[:split], idx[split:]
X_train, X_test = X[train_idx], X[test_idx]
y_train, y_test = y[train_idx], y[test_idx]
```

## 80/20 Reference

```python
import numpy as np

# Create
np.array([1, 2, 3])
np.zeros((3, 4))
np.arange(5)
rng = np.random.default_rng(42)
rng.normal(0, 1, (100, 5))

# Inspect
a.shape; a.dtype; a.ndim

# Index
a[0]; a[-1]; a[1:4]; a[[0, 2]]; a[a > 2]
m[:, 0]; m[0:2, 1:3]

# Axis (the trap)
m.sum(axis=0)       # column sums
m.sum(axis=1)       # row sums

# Aggregate
a.mean(); a.std(); a.min(); a.max(); a.argmax()

# Reshape
a.reshape(-1, 1)   # column vector — you'll use this constantly

# Copy
view = m[:, 0]      # modifies original!
copy = m[:, 0].copy()

# Broadcast
m + np.array([10, 20, 30])
