---
tags: [ml, python, hydra, config]
aliases: ["Hydra cheatsheet"]
created: 2026-06-11
status: complete
parent: "[[MOCs/ML & Data Science Packages -- Map of Content]]"
---

## 80/20

```python
# config.yaml
defaults:
  - model: lgbm
  - data: uci
  - training: default
```

```yaml
# configs/model/lgbm.yaml
learning_rate: 0.05
num_leaves: 64
min_data_in_leaf: 20
feature_fraction: 0.8
```

```python
# train.py
import hydra
from omegaconf import DictConfig, OmegaConf

@hydra.main(version_base=None, config_path="configs", config_name="config")
def train(cfg: DictConfig) -> None:
    # Log the full config to MLflow
    config_yaml = OmegaConf.to_yaml(cfg)
    mlflow.log_param("full_config", config_yaml)

    # Access specific values
    lr = cfg.model.learning_rate
    n_sites = cfg.data.n_sites

# CLI overrides -- no code changes needed
# uv run python train.py model.learning_rate=0.1
# uv run python train.py model.learning_rate=0.1 data.n_sites=100
# uv run python train.py model=xgboost   # switch entire config group
```

## Config structure

```
configs/
├── config.yaml             # top-level: composes via defaults
├── model/
│   ├── lgbm.yaml           # LightGBM hyperparams
│   └── xgboost.yaml        # XGBoost alternative (switch via CLI)
├── data/
│   └── uci.yaml            # data pipeline params
└── training/
    └── default.yaml        # training params (splits, n_splits)
```

## CLI override patterns

| Command | Effect |
|---------|--------|
| `... model.learning_rate=0.1` | override scalar |
| `... data.n_sites=100` | override nested key |
| `... model=xgboost` | switch entire config group |
| `... -m model.learning_rate=0.01,0.05` | multi-run (sweep) |

## Traps

- **Working directory changes** -- by default Hydra changes CWD to `outputs/YYYY-MM-DD/HH-MM-SS`. Use `@hydra.main(..., version_base=None)` and consider `hydra.utils.get_original_cwd()` to reference files relative to project root.
- **`config_path` is relative to the script** -- not the project root. It's the directory _containing_ `config.yaml`.
- **OmegaConf objects are not plain dicts** -- use `OmegaConf.to_yaml()` for serialization, `OmegaConf.to_container()` for dict conversion.
- **Defaults list is order-dependent** -- later entries can override earlier ones.
- **Missing `config_path`** -- if wrong path, Hydra silently falls back with an opaque error. Double-check the relative path.
