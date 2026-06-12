---
tags: [ml, python, lightgbm, gradient-boosting]
aliases: ["LightGBM cheatsheet"]
created: 2026-06-11
status: complete
parent: "[[MOCs/ML & Data Science Packages -- Map of Content]]"
---

## 80/20

```python
import lightgbm as lgb

dtrain = lgb.Dataset(X_train, label=y_train,
                     categorical_feature=["col_a"],  # tell it which are categorical
                     free_raw_data=False)            # keep X after training
dvalid = lgb.Dataset(X_val, label=y_val, reference=dtrain)

model = lgb.train(
    params={
        "objective": "mape",       # built-in MAPE optimisation
        "metric": "mape",          # eval metric (can differ from objective)
        "learning_rate": 0.05,     # lower = slower convergence, better generalisation
        "num_leaves": 64,          # max leaves per tree
        "min_data_in_leaf": 20,    # min samples per leaf (anti-overfit)
        "feature_fraction": 0.8,   # column subsample per iteration
        "verbosity": -1,           # quiet mode
    },
    train_set=dtrain,
    valid_sets=[dtrain, dvalid],
    callbacks=[
        lgb.early_stopping(50),    # stop if val metric stalls for 50 rounds
        lgb.log_evaluation(50),    # log every 50 rounds
    ],
    num_boost_round=1000,          # ceiling -- early stopping cuts it off
)

preds      = model.predict(X_test)
importance = model.feature_importance(importance_type="gain")
model.save_model("models/model.lgb")
```

## Key parameters

| Parameter | Effect | Tuning direction |
|-----------|--------|-----------------|
| `learning_rate` | lower = slower but better generalisation | decrease if val gap widens |
| `num_leaves` | more leaves = more complex trees | decrease if train >> val |
| `min_data_in_leaf` | higher = simpler trees, noise-resistant | increase if val is noisy |
| `feature_fraction` | lower = more randomness, less overfitting | decrease if overfitting |
| `lambda_l1` / `lambda_l2` | L1/L2 regularisation on leaf weights | increase if overfitting |
| `max_depth` | hard tree depth limit (alternative to num_leaves) | set when num_leaves leads to overfit |
| `min_gain_to_split` | minimum gain for a split | increase if overfitting |
| `subsample` | row subsample per iteration | decrease if overfitting |

## Categorical features

```python
# Option 1: pass column names at Dataset creation
dtrain = lgb.Dataset(X, label=y, categorical_feature=["site_type", "month"])

# Option 2: use pandas "category" dtype
X["site_type"] = X["site_type"].astype("category")
```

Do NOT manually one-hot encode -- LightGBM handles native categoricals via the `categorical_feature` parameter. It uses a grouping-based split finder.

## Built-in objectives

| Objective | Use case |
|-----------|----------|
| `mape` | demand forecasting (MAPE-optimised) |
| `regression` | standard MSE regression |
| `regression_l1` | MAE-robust regression |
| `binary` | binary classification |
| `multiclass` | multi-class, requires `num_class` |
| `huber` | robust regression, less outlier-sensitive |

## Traps

- **Missing `libgomp1` in Docker** -- LightGBM crashes at import without OpenMP. Install via `apt-get install libgomp1` in Dockerfile.
- **`free_raw_data=True` (default)** -- after training, `X_train` is freed from `Dataset`. Set `free_raw_data=False` if you need the data reference later.
- **Categoricals must be encoded as integers** (0, 1, 2, ...) or pandas `category` dtype -- strings cause silent errors.
- **Early stopping on `dvalid`** -- always pass a validation set. Without it, you are training to full `num_boost_round` (likely overfitted).
- **`feature_fraction` and `bagging_freq`** -- `feature_fraction` works per iteration. For row subsampling you also need `bagging_freq > 0`.
- **Unbalanced data** -- use `scale_pos_weight`, `is_unbalance`, or custom weight column.
- **Seed sensitivity** -- set `random_state` for reproducibility across runs.
