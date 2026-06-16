---
type: moc
tags: [moc, ml, data-science, refresher]
aliases: ["ML Packages MOC", "Data Science Refresher"]
created: 2026-06-11
status: in-progress
---

# ML & Data Science Packages -- Map of Content

Refresher reference for ML tools and concepts. Each file starts with an 80/20 cheat sheet, then expands into full examples and common traps. Python data tools (numpy, pandas, matplotlib) now live under [[MOCs/Python — Map of Content|Python MOC]].

## Core ML

| Tool | What it does | File | Status |
|------|-------------|------|--------|
| scikit-learn | Preprocessing, models, tuning, evaluation | [[Notes/ML/Tools/ml-sklearn\|ml-sklearn]] | Complete |
| LightGBM | Gradient-boosted trees for forecasting | [[Notes/ML/Tools/ml-lightgbm\|ml-lightgbm]] | Complete |
| MLflow | Experiment tracking + model registry | [[Notes/ML/Tools/ml-mlflow\|ml-mlflow]] | Complete |
| Pandera | DataFrame runtime schema validation | [[Notes/ML/Tools/ml-pandera\|ml-pandera]] | Complete |
| Hydra | Composable YAML configs for ML pipelines | [[Notes/ML/Tools/ml-hydra\|ml-hydra]] | Complete |

## Data & Pipeline Tooling

| Tool | What it does | File | Status |
|------|-------------|------|--------|
| Feast | Feature store (train/serve skew prevention) | [[Notes/ML/Tools/ml-feast\|ml-feast]] | Complete |
| Evidently | Data drift + model performance monitoring | [[Notes/ML/Tools/ml-evidently\|ml-evidently]] | Complete |
| DVC | Data version control + pipeline DAG orchestration | [[Notes/ML/Tools/ml-dvc\|ml-dvc]] | Complete |
| Shared Dataset | Turbofan sensor data used across examples | [[Notes/ML/Tools/ml-shared-dataset\|ml-shared-dataset]] | Complete |

## Concepts

| Note | Topic | Status |
|------|-------|--------|
| [[Notes/ML/Concepts/Class Imbalance\|Class Imbalance]] | Precision, recall, F1, ROC/AUC | Draft |
| [[Notes/ML/Concepts/Real-Time Data Transports in Machine Learning\|Data Transports]] | HTTP, Kafka, RabbitMQ, gRPC for ML | Draft |
| [[Notes/ML/Concepts/When to Use Machine Learning\|When to Use ML]] | Decision framework for ML applicability | Draft |
