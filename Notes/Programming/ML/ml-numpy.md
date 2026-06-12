---
tags: [ml, numpy, arrays, numerical]
aliases: ["NumPy", "NumPy Refresher"]
parent: "[[ML & Data Science Packages — Map of Content]]"
created: 2026-06-11
status: complete
---

# L1 -- NumPy

## 80/20 Cheat Sheet

```python
import numpy as np

# Creating arrays
a = np.array([1, 2, 3])                     # from list
z = np.zeros((3, 4))                        # 3x4 of zeros
o = np.ones((5,))                           # [1. 1. 1. 1. 1.]
r = np.arange(0, 10, 2)                     # [0 2 4 6 8]
l = np.linspace(0, 1, 5)                    # [0. 0.25 0.5 0.75 1.]
e = np.eye(3)                               # 3x3 identity
rn = np.random.default_rng(42).normal(0, 1, (3, 3))  # 3x3 N(0,1)

# Inspecting
a.shape; a.dtype; a.ndim                    # (3,), int64, 1
a.size                                       # total elements

# Indexing
a[0]                                         # first element
a[-1]                                        # last element
a[1:3]                                       # slice
a[[0, 2]]                                    # fancy indexing
a[a > 2]                                     # boolean mask

# 2D indexing
m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
m[0, 1]                                      # row 0, col 1 -> 2
m[0]                                         # first row
m[:, 0]                                      # first column
m[0:2, 1:3]                                  # submatrix
m[m > 5]                                     # boolean mask flattens

# Aggregates
a.sum(); a.mean(); a.std(); a.min(); a.max()
a.argmax(); a.argmin()                       # index of max/min
m.sum(axis=0)                                # column sums (collapse rows)
m.sum(axis=1)                                # row sums (collapse columns)

# Math (element-wise)
a + 5; a * 2; a ** 2; np.log(a); np.sqrt(a)
np.dot(a, b)                                 # dot product
np.matmul(m1, m2)                            # matrix multiply

# Shape manipulation
m.reshape(1, 9)                              # change shape
m.reshape(-1, 3)                             # auto-infer one dim
m.flatten()                                  # to 1D
m.T                                          # transpose

# Combining
np.vstack([a, b])                            # stack rows
np.hstack([a, b])                            # stack columns
np.concatenate([m1, m2], axis=0)             # general concat

# Random
rng = np.random.default_rng(42)              # seed for reproducibility
rng.normal(0, 1, size=(100, 5))              # normal distribution
rng.uniform(0, 1, size=(100,))               # uniform
rng.integers(0, 10, size=20)                 # random integers
```

## Creating arrays

The ndarray is the core object. Three properties matter: `shape`, `dtype`, `values`.

```python
# From Python lists
np.array([1, 2, 3])                          # shape (3,)
np.array([[1, 2], [3, 4]])                   # shape (2, 2)

# Common constructors
np.zeros((2, 3))                             # all zeros, dtype float64 by default
np.ones((3,))                                # all ones
np.full((2, 2), 7)                           # all 7s
np.eye(4)                                    # identity matrix 4x4
np.arange(5)                                 # [0, 1, 2, 3, 4]
np.arange(2, 10, 3)                          # [2, 5, 8]
np.linspace(0, 1, 5)                         # 5 evenly spaced points between 0 and 1

# Random
np.random.seed(42)                           # old API, still works
np.random.rand(3, 3)                         # uniform [0,1)
np.random.randn(100)                         # standard normal

rng = np.random.default_rng(42)              # new Generator API -- preferred
rng.normal(0, 0.1, size=(5, 3))             # 5x3 from N(0, 0.1)
rng.uniform(0, 1, size=10)
rng.integers(0, 100, size=20)
```

**Trap:** `np.random.seed()` affects global state. The new `default_rng()` is isolated -- use it.

## Indexing and slicing

```python
a = np.array([10, 20, 30, 40, 50])
a[0]                                         # 10
a[-1]                                        # 50
a[1:4]                                       # [20, 30, 40]
a[[0, 2, 4]]                                 # fancy indexing: [10, 30, 50]

m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
m[1, 2]                                      # row 1, col 2 -> 6
m[:, 1]                                      # all rows, col 1 -> [2, 5, 8]
m[1, :]                                      # row 1 -> [4, 5, 6]
m[0:2, 1:3]                                  # submatrix: [[2, 3], [5, 6]]

# Boolean indexing -- THE pattern for filtering
data = np.array([1.2, 0.8, 2.5, -0.3, 1.7])
mask = data > 1.0                            # [True, False, True, False, True]
data[mask]                                   # [1.2, 2.5, 1.7]

# Combine conditions with & (not and)
data[(data > 0) & (data < 2)]                # [1.2, 0.8, 1.7]
```

## Operations and broadcasting

Element-wise by default. Broadcasting expands smaller arrays automatically.

```python
temps = np.array([480.2, 481.5, 495.3, 476.8, 478.1])

# Element-wise
temps - 480                                  # [0.2, 1.5, 15.3, -3.2, -1.9]
temps * 1.5                                  # multiply each
temps ** 2                                   # square each
np.sqrt(temps); np.log(temps); np.exp(temps)

# Aggregates
temps.mean()                                 # 482.38
temps.std()                                  # 6.45
temps.min(); temps.max()                     # 476.8, 495.3
temps.argmax()                               # 2 -- index of max value
temps.sum(); temps.cumsum()                  # cumulative sum

# axis parameter -- this trips people up
m = np.array([[1, 2, 3], [4, 5, 6]])
m.sum(axis=0)                                # [5, 7, 9] -- column sums (down rows)
m.sum(axis=1)                                # [6, 15] -- row sums (across cols)
m.mean(axis=0)                               # [2.5, 3.5, 4.5]

# Broadcasting
m = np.array([[1, 2, 3], [4, 5, 6]])         # shape (2, 3)
v = np.array([10, 20, 30])                   # shape (3,) -- broadcasts
m + v                                        # [[11, 22, 33], [14, 25, 36]]

col_means = m.mean(axis=0)                   # [2.5, 3.5, 4.5]
m - col_means                                # [[-1.5, -1.5, -1.5], [1.5, 1.5, 1.5]]
```

**Trap:** `axis=0` operates along rows (produces column results). `axis=1` operates along columns. Remember: axis=0 = "vertical", axis=1 = "horizontal".

## Shape manipulation

```python
a = np.arange(12)                            # [0..11], shape (12,)

# Reshape
a.reshape(3, 4)                              # 3x4 matrix
a.reshape(2, -1)                             # 2x6 (auto-inferred)
a.reshape(-1,)                               # flatten

# Flattening
a.ravel()                                    # flatten (returns view when possible)
a.flatten()                                  # flatten (always returns copy)
a.reshape(-1)                                # flatten

# Adding/removing dimensions
a = np.array([1, 2, 3])                      # shape (3,)
a[np.newaxis, :]                             # shape (1, 3) -- row vector
a[:, np.newaxis]                             # shape (3, 1) -- column vector
np.expand_dims(a, axis=0)                    # same as newaxis
np.squeeze(a)                                # remove dims of size 1
```

**Trap:** Shape `(5,)` is NOT the same as `(5, 1)`. Many sklearn models require 2D input. A column vector is `reshape(-1, 1)`.

## Combining arrays

```python
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6]])

np.vstack([a, b])                            # stack rows: [[1,2],[3,4],[5,6]]
np.hstack([a, b.T])                          # stack columns: [[1,2,5],[3,4,6]]
np.concatenate([a, b], axis=0)               # same as vstack
np.concatenate([a, b.T], axis=1)             # same as hstack

np.split(a, 2)                               # split into 2 equal parts
np.array_split(a, 3)                         # split into 3 (uneven allowed)
```

## Copy vs view -- critical

```python
m = np.array([[1, 2, 3], [4, 5, 6]])
col = m[:, 0]                                # VIEW, not copy
col[0] = 999                                 # ALSO modifies m!
m[0, 0]                                      # 999 -- original changed!

# Fix: explicit copy
col_copy = m[:, 0].copy()
col_copy[0] = 0                              # safe, m unaffected
```

Slicing returns views. Fancy indexing and boolean indexing return copies. When in doubt, call `.copy()`.

## Linear algebra

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

A @ B                                        # matrix multiply (Python 3.5+)
np.dot(A, B)                                 # same
np.matmul(A, B)                              # same, preferred for matrics
A.T                                          # transpose
np.linalg.inv(A)                             # inverse
np.linalg.det(A)                             # determinant
np.linalg.eig(A)                             # eigenvalues/vectors
```

## Data type traps

```python
# Integer division
ints = np.array([1, 2, 3], dtype=int)
ints / 2                                     # [0.5, 1.0, 1.5] -- float in modern numpy

# Overflow
np.array([200], dtype=np.int8)               # [-56] -- overflow, no warning

# Mixed types
np.array([1, 2.5, 3])                        # all float64
np.array([1, 'a', 2])                        # all string (U dtype)
```
