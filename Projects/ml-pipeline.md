---
tags: [ml, python, pipeline, project]
parent: "[[Projects — Map of Content]]"
status: planning
start: 2026-06-16
target: 2026-08-25
estimate: 185 hrs over 10 weeks
pace: ~19 hrs/wk (3 hrs/day, 6 days)
share: 35%
---

# ML Pipeline — Python Data Stack to E2E Pipeline

## Scope

Start from the Python data stack (numpy, pandas, matplotlib, sklearn) and build up to a working end-to-end ML pipeline in the E2E_ml codebase. Covers data ingestion, validation, feature engineering, model training, evaluation, tracking, and containerized deployment.

**Codebase:** `~/dev/repos/E2E_ml/`

**Target: 10 weeks at ~19 hrs/week** (185 hrs total)

---

## Phase Breakdown

### Phase 1 — Python Data Stack Refresher (30 hrs)

**Week 1 — numpy & pandas (15 hrs)**

- Rewrite py-numpy exercises from scratch
- Rewrite py-pandas exercises from scratch
- Master sensor dataset patterns: rolling, groupby, merge, null handling
- Write pandas exercise module

**Week 2 — matplotlib, sklearn & first pipeline (15 hrs)**

- EDA on a small dataset (sensor/titanic) — matplotlib/seaborn practice
- sklearn: train/test split, scalers, encoders, Pipeline object
- Write a barebones end-to-end ML script (no MLOps yet)
- Rewrite py-matplotlib-seaborn.md if needed

### Phase 2 — MLOps Tooling (60 hrs)

**Week 3 — MLflow (12 hrs)**

- Experiment tracking, model registry, projects
- Run 3 experiments with different params, compare in UI

**Week 4 — Validation & feature stores (20 hrs)**

- Pandera: dataframe schema validation
- Evidently: data drift and model drift reports
- Feast: feature store basics — definitions, serving

**Week 5 — DVC & Hydra (15 hrs)**

- DVC: data versioning, pipeline stages, metrics
- Hydra: hierarchical config, multi-run, composition

**Week 6 — E2E_ml architecture review (13 hrs)**

- Read docs/ directory thoroughly
- Read Agent/Guide.md and blueprints
- Map the architecture — which tools go where
- Identify what exists vs what needs building

### Phase 3 — E2E Pipeline Build (75 hrs)

**Week 7 — Data layer (18 hrs)**

- Pick a dataset (tabular, regression or classification)
- DVC data ingestion + Pandera validation
- Feature engineering pipeline
- Unit tests for transforms

**Week 8 — Training pipeline (20 hrs)**

- sklearn pipeline with Hydra config
- MLflow tracking integration
- Evidently monitoring checks
- Evaluation harness (metrics, plots, thresholds)

**Week 9 — Production pipeline (20 hrs)**

- Model registry via MLflow
- Inference script / serving endpoint
- Integration tests
- Document full pipeline flow

**Week 10 — Polish (17 hrs)**

- Run full pipeline end-to-end
- Edge cases: missing data, outliers, retraining trigger
- Project README
- Vault: document architecture decisions and traps

### Phase 4 — Docker & Deployment (20 hrs — starts final weeks)

- Docker basics: Dockerfile for training + inference
- docker-compose for full stack
- Simple API server with health checks
- Basic monitoring / logging

---

## Weekly Schedule

| Week | Phase | Hrs | Cumulative |
|------|-------|-----|------------|
| 1 | P1: numpy + pandas | 19 | 19 |
| 2 | P1: matplotlib + sklearn, pipeline draft | 19 | 38 |
| 3 | P2: MLflow | 19 | 57 |
| 4 | P2: Pandera, Evidently, Feast | 19 | 76 |
| 5 | P2: DVC + Hydra | 19 | 95 |
| 6 | P2: E2E_ml architecture review, P4 start (Docker basics) | 19 | 114 |
| 7 | P3: Data layer, P4: Docker | 19 | 133 |
| 8 | P3: Training pipeline, P4: Docker | 19 | 152 |
| 9 | P3: Production pipeline, P4: compose + API | 19 | 171 |
| 10 | P3: Polish + P4: finish deployment | 14 | 185 |

**Target end: 2026-08-25** (Week 10)
