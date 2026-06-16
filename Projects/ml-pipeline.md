---
tags: [ml, python, pipeline, project]
parent: "[[Projects -- Map of Content]]"
status: planning
start: 2026-06-16
target: 2026-09-01
estimate: 11 weeks @ ~12 hrs/wk
---

# ML Pipeline — Python Data Stack to E2E Pipeline

## Scope

Start from the Python data stack (numpy, pandas, matplotlib, sklearn) and build up to a working end-to-end ML pipeline in the E2E_ml codebase. This covers data ingestion, validation, feature engineering, model training, evaluation, tracking, and deployment fundamentals.

**Codebase:** `~/dev/repos/E2E_ml/`

**Total: ~11 weeks at ~12 hrs/week** (~132 hrs)

---

## Phase Breakdown

### Phase 1 — Python Data Stack Refresher (Weeks 1-2, ~24 hrs)

Solidify the fundamentals before touching pipelines.

**Week 1 — numpy & pandas**

- [ ] Rewrite py-numpy.md exercises from scratch (teaching style)
- [ ] Rewrite py-pandas.md exercises from scratch (teaching style)
- [ ] Complete the sensor dataset patterns (rolling, groupby, merge, nulls)
- [ ] Do the pandas exercise module (when you write it)

**Week 2 — matplotlib, sklearn & basics**

- [ ] Practice matplotlib through EDA on a small dataset (titanic, iris, or sensor)
- [ ] sklearn basics: train/test split, scalers, encoders, pipelines
- [ ] Write a barebones ML script end-to-end (no MLOps)
- [ ] Rewrite py-matplotlib-seaborn.md if needed

**Deliverable:** A single clean notebook/script that loads data, explores, engineers features, trains a model, evaluates it

---

### Phase 2 — MLOps Tooling (Weeks 3-6, ~48 hrs)

Learn the tools that E2E_ml uses or will use.

**Week 3 — Experiment tracking**

- [ ] MLflow: tracking, registry, projects
- [ ] Run 3 experiments with different params, compare in UI

**Week 4 — Data & validation**

- [ ] Pandera: schema validation for dataframes
- [ ] Evidently: data drift, model drift reports
- [ ] Feast: feature store basics

**Week 5 — Pipeline orchestration**

- [ ] DVC: data versioning, pipelines
- [ ] Hydra: config management

**Week 6 — Production patterns**

- [ ] Shared dataset patterns (ml-shared-dataset.md)
- [ ] Review E2E_ml docs/ directory to understand the architecture
- [ ] Read the Agent/Guide.md

**Deliverable:** Each tool has a runnable example. You can explain what each one does and when to use it.

---

### Phase 3 — E2E Pipeline Build (Weeks 7-10, ~48 hrs)

This is the main event. Build the E2E_ml pipeline around a real dataset.

**Week 7 — Data layer**

- [ ] Pick a dataset (tabular, regression or classification)
- [ ] Set up data ingestion with DVC + Pandera validation
- [ ] Feature engineering with feast or manual feature store
- [ ] Write unit tests for data transforms

**Week 8 — Training pipeline**

- [ ] Build sklearn pipeline with Hydra config
- [ ] Integrate MLflow tracking
- [ ] Add Evidently monitoring checks
- [ ] Add evaluation harness (metrics, plots, thresholds)

**Week 9 — Production pipeline**

- [ ] Add model registry (MLflow)
- [ ] Create inference script / serving endpoint
- [ ] Write integration tests
- [ ] Document the full pipeline flow

**Week 10 — Polish & validation**

- [ ] Run the full pipeline end-to-end
- [ ] Check edge cases (missing data, outliers, retraining)
- [ ] Write the project README
- [ ] Vault: document architecture decisions and traps

**Deliverable:** Working E2E pipeline with tests, docs, and tracking

---

### Phase 4 — Docker & Deployment (Weeks 10-11, ~12 hrs)

Containerize and serve.

- [ ] Docker basics: Dockerfile for training + inference
- [ ] docker-compose for the full stack (if applicable)
- [ ] Simple API server for predictions
- [ ] Health checks, logging, basic monitoring

**Deliverable:** Containerized pipeline that can be deployed

---

## Weekly Distribution

| Week | Phase | Hours |
|------|-------|-------|
| 1    | P1: numpy + pandas | 12 |
| 2    | P1: matplotlib + sklearn | 12 |
| 3    | P2: MLflow | 12 |
| 4    | P2: Pandera + Evidently + Feast | 12 |
| 5    | P2: DVC + Hydra | 12 |
| 6    | P2: Production patterns + E2E_ml review | 12 |
| 7    | P3: Data layer | 12 |
| 8    | P3: Training pipeline | 12 |
| 9    | P3: Production pipeline | 12 |
| 10   | P3: Polish + P4 start | 12 |
| 11   | P4: Docker + deployment | 12 |

**End date target: 2026-09-01**
