---
tags: [ml, pipeline, project]
parent: "[[Projects — Map of Content]]"
status: planning
start: 2026-06-30
target: 2026-08-25
estimate: 135 hrs over 8 weeks
pace: ~17 hrs/week (mixed with ml-basics early weeks)
share: sequenced after ml-basics
---

# ML Pipeline — E2E_ml Implementation

## Scope

Build the E2E_ml project from documentation to working code. The docs (`docs/`) and agent blueprints (`Agent/`) at `~/dev/repos/E2E_ml/` define the full spec: ingest → validate → features → train → evaluate → serve → monitor, using DVC, Pandera, Feast, LightGBM, MLflow, FastAPI, and Evidently.

This phase starts after the Python data stack refresher (ml-basics) is done. For the first 2 weeks, it shares the daily ML slot with ml-basics — lighter load here until basics finish.

**Source:** `~/dev/repos/E2E_ml/` (docs + blueprints)

**Target: 8 weeks at ~17 hrs/week** (135 hrs total) — lighter first 2 weeks while ml-basics runs

---

## Phase Breakdown

### Phase 1 — Project Setup (Week 1, ~12 hrs)

Get the repository ready for implementation.

- [ ] Review all Agent/ blueprints and docs/ pages thoroughly
- [ ] Create src/ package structure (ingest, validate, features, train, evaluate, serve, monitor)
- [ ] Set up pyproject.toml with all dependencies
- [ ] Create directories: configs/, tests/, data/, models/, notebooks/, reports/, logs/
- [ ] .pre-commit-config.yaml with ruff + mypy + nbstripout
- [ ] .env.example
- [ ] Makefile with common commands
- [ ] First uv sync — lockfile clean

### Phase 2 — Data Layer (Week 2, ~15 hrs)

- [ ] Download UCI dataset (or your chosen dataset)
- [ ] DVC init + data ingestion script (raw → parquet)
- [ ] Pandera schemas for raw and processed data
- [ ] DVC pipeline stage: ingest → validate
- [ ] Smoke test: dvc repro runs end-to-end

### Phase 3 — Feature Engineering (Week 3, ~18 hrs)

- [ ] Feature design per docs (lag features, rolling stats, time features, site_type encoding)
- [ ] Feature engineering module with unit tests
- [ ] Feast setup: feature_store.yaml, FeatureViews, feature definitions
- [ ] DVC pipeline stage: engineer features
- [ ] Point-in-time correctness check (no leakage)

### Phase 4 — Training Pipeline (Week 4, ~20 hrs)

- [ ] Hydra config directory: config.yaml with dataset, features, model, training sections
- [ ] LightGBM training script with MLflow autologging
- [ ] TimeSeriesSplit cross-validation
- [ ] Hyperparameter search (Optuna or GridSearch)
- [ ] DVC pipeline stage: train
- [ ] Verify: 3 experiments run, compare in MLflow UI

### Phase 5 — Evaluation & Model Selection (Week 5, ~15 hrs)

- [ ] Offline evaluation: MAPE by slice (site_type, time period)
- [ ] Threshold gates: overall < 15%, per-site < 25%, Q4 < 20%
- [ ] MLflow model registry: register champion model
- [ ] Shadow deployment script (champion vs challenger comparison)
- [ ] Evaluation report generation

### Phase 6 — Serving (Week 6, ~18 hrs)

- [ ] FastAPI app: /predict endpoint with Pydantic schemas
- [ ] Load model from MLflow registry (Production stage)
- [ ] Dockerfile for serving (multi-stage: build → run)
- [ ] docker-compose: MLflow tracking server + app
- [ ] Integration test: request → prediction
- [ ] Health checks, logging (loguru)

### Phase 7 — CI/CD & Testing (Week 7, ~17 hrs)

- [ ] Unit tests for each module (pytest, 70%+ coverage)
- [ ] GitHub Actions: PR workflow (lint + test + smoke infer)
- [ ] GitHub Actions: Training workflow (full pipeline + gate + registry promotion)
- [ ] Makefile targets: test, lint, train, serve, all

### Phase 8 — Monitoring & Polish (Week 8, ~20 hrs)

- [ ] Evidently drift detection: feature drift (PSI) + performance
- [ ] Retraining loop: 3-trigger system (time/PSI/perf), non-inferiority gate
- [ ] Demo: run full pipeline, make a prediction, check monitoring
- [ ] Project README with architecture diagram
- [ ] Vault: document architecture decisions, tool choices, traps

---

## Weekly Schedule

| Week | Phase | Hrs | Note |
|------|-------|-----|------|
| 1 | P1: Project setup | 12 | Light — ml-basics still running |
| 2 | P2: Data layer | 15 | ml-basics finishes ~mid-week |
| 3 | P3: Feature engineering | 18 | |
| 4 | P4: Training pipeline | 20 | Heaviest phase |
| 5 | P5: Evaluation | 15 | |
| 6 | P6: Serving | 18 | |
| 7 | P7: CI/CD | 17 | |
| 8 | P8: Monitoring + polish | 20 | |

**Target end: 2026-08-25** (8 weeks from start, ml-basics first 2 weeks overlap)
