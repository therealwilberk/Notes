---
type: moc
tags: [moc, ml, data-science, python, refresher]
aliases: ["ML Packages MOC", "Data Science Refresher"]
created: 2026-06-11
status: in-progress
---

# ML & Data Science Packages -- Map of Content

Refresher reference for the core Python data science stack. Each file starts with an 80/20 cheat sheet, then expands into full examples and common traps. Shared dataset documented in [[ml-shared-dataset|ml-shared-dataset]].

## The Stack

| # | Library | Use | Status |
|---|---------|-----|--------|
| L1 | [[ml-numpy|NumPy]] | Arrays, math, broadcasting, reshaping | Complete |
| L2 | [[ml-pandas|pandas]] | Data wrangling, groupby, rolling, merge | Complete |
| L3 | [[ml-sklearn|scikit-learn]] | Preprocessing, models, tuning, evaluation | Complete |
| L4 | [[ml-matplotlib-seaborn|matplotlib / seaborn]] | Plots, EDA, heatmaps, subplots | Complete |

## Project Tooling

| Tool | What it does | File | Status |
|------|-------------|------|--------|
| uv | Python project manager (pip+poetry+venv replacement) | [[ml-uv\|ml-uv]] | Complete |
| LightGBM | Gradient-boosted trees for forecasting | [[ml-lightgbm\|ml-lightgbm]] | Complete |
| MLflow | Experiment tracking + model registry | [[ml-mlflow\|ml-mlflow]] | Complete |
| Feast | Feature store (train/serve skew prevention) | [[ml-feast\|ml-feast]] | Complete |
| Pandera | DataFrame runtime schema validation | [[ml-pandera\|ml-pandera]] | Complete |
| FastAPI | Async model serving with auto-docs | [[ml-fastapi\|ml-fastapi]] | Complete |
| Hydra | Composable YAML configs for ML pipelines | [[ml-hydra\|ml-hydra]] | Complete |
| Evidently | Data drift + model performance monitoring | [[ml-evidently\|ml-evidently]] | Complete |
| DVC | Data version control + pipeline DAG orchestration | [[ml-dvc\|ml-dvc]] | Complete |
| Dev tools | ruff, mypy, pre-commit, nbstripout, pytest, loguru | [[ml-dev-tools\|ml-dev-tools]] | Complete |
