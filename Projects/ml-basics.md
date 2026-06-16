---
tags: [python, ml, data-stack, lesson]
parent: "[[Projects — Map of Content]]"
status: planning
start: 2026-06-16
target: 2026-06-30
estimate: 42 hrs over 2 weeks
pace: ~21 hrs/week (3.5 hrs/day, 6 days)
note: increases daily ML slot from 3 to 3.5 hrs — still within 8-10 hr/day total
---

# ML Basics — Python Data Stack Refresher

## Scope

Pin down numpy, pandas, matplotlib, and sklearn sequentially on a single Kaggle dataset. End with a combined EDA → baseline model script that uses all four together. This is a prerequisite for the E2E_ml pipeline build.

**Pick one Kaggle dataset** and use it throughout. Good candidates: anything tabular, regression or classification. Stick with it the whole way — context continuity matters more than dataset quality.

**Target: 2 weeks at ~21 hrs/week** (42 hrs total)

---

## Phases

### Phase 1 — numpy (~8 hrs)

- [ ] Ndarray basics: shape, dtype, reshaping, broadcasting
- [ ] Vectorized ops: ufuncs, aggregations, masking
- [ ] Load your Kaggle data as numpy — understand raw array shapes
- [ ] Compute simple stats by slicing (min/max/mean per column)
- [ ] Write practice snippets for every `py-numpy.md` pattern

### Phase 2 — pandas (~12 hrs)

- [ ] DataFrame creation, dtypes, info(), describe()
- [ ] Select/filter patterns: loc, iloc, boolean indexing
- [ ] groupby + transform + agg — feature engineering patterns
- [ ] Rolling windows, lags, diffs
- [ ] Merge and concat
- [ ] Null handling strategies
- [ ] Write practice for every `py-pandas.md` pattern on your dataset

### Phase 3 — matplotlib & seaborn (~6 hrs)

- [ ] Matplotlib: figure/ax pattern, line, scatter, hist, subplots
- [ ] Seaborn: pairplot, heatmap, boxplot, catplot
- [ ] EDA plots for your dataset — distributions, correlations, trends
- [ ] Style clean enough to use in a report

### Phase 4 — sklearn (~10 hrs)

- [ ] train_test_split, cross_validate, GridSearchCV
- [ ] ColumnTransformer + Pipeline for mixed types
- [ ] Scalers (Standard, Robust), Encoders (OneHot, Ordinal)
- [ ] Fit a baseline model (LinearRegression / RandomForest / LogisticRegression)
- [ ] Evaluate: metrics, confusion matrix, feature importance

### Phase 5 — Combine (~6 hrs)

- [ ] One clean script: load → EDA → feature engineering → pipeline → train → evaluate
- [ ] No MLOps, no tracking — just raw sklearn
- [ ] Vault note: architecture decisions and traps discovered

---

## Weekly Schedule

| Week | Phases | Hrs |
|------|--------|-----|
| 1 | numpy (8), pandas start (12) | ~20 |
| 2 | pandas finish, matplotlib (6), sklearn (10), combine (6) | ~22 |

**Target end: 2026-06-30** (2 weeks)
