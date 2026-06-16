---
tags: [ml, python, dvc, data-versioning, pipeline]
aliases: ["DVC cheatsheet"]
created: 2026-06-11
status: complete
parent: "[[MOCs/ML & Data Science Packages -- Map of Content]]"
---

## 80/20

```bash
# Pipeline orchestration
dvc repro                  # run only stale stages (hash comparison)
dvc repro --force          # re-run everything
dvc repro ingest           # run single stage + dependents
dvc dag                    # ASCII pipeline DAG
dvc status                 # which stages are stale
dvc params diff            # param changes between git revisions

# Data tracking (git for data)
dvc add data/raw/dataset.zip    # -> .dvc/cache/ + .dvc pointer file
dvc checkout                    # materialise cached files
dvc pull                        # download from remote + materialise
dvc push                        # upload local cache to remote

# Setup
dvc init                        # initialise DVC in repo
dvc remote add myremote s3://my-bucket/dvc
```

## dvc.yaml stage definition

```yaml
stages:
  ingest:
    cmd: python src/data/ingestion.py
    deps:
      - src/data/ingestion.py
      - data/raw/household_power_consumption.zip
    outs:
      - data/processed/jua.parquet
    params:
      - configs/data/uci.yaml:
          - sample_rate
          - n_sites

  features:
    cmd: python src/features/engineering.py
    deps:
      - src/features/engineering.py
      - data/processed/jua.parquet
    outs:
      - data/features/site_features.parquet
```

Each stage declares **four pillars of staleness** -- if any hash changes, DVC re-runs it:

- `deps` -- code + input data
- `outs` -- output files (hashes stored in `dvc.lock`)
- `params` -- config values from YAML files (per-key granularity)
- `metrics` -- model performance metrics (optional)

## Everyday workflow

```bash
# 1. Pull latest data
git pull && dvc pull

# 2. Make changes, then reproduce only stale stages
dvc repro

# 3. After changes pass, push data
dvc push

# 4. On a fresh clone
git clone <repo> && cd <repo> && dvc pull
```

## Traps

- **`dvc.lock` is auto-generated** -- never edit it manually. Always regenerate via `dvc repro`.
- **Data files are replaced with `.dvc` pointer files** -- after `dvc add`, the original file moves to `.dvc/cache/`. The `.dvc` file (YAML with MD5) is what you commit to Git.
- **`dvc checkout` after `git checkout`** -- if you switch branches, your working directory has the `.dvc` files but not the actual data. Run `dvc checkout` to materialise.
- **Remote storage required for sharing** -- `dvc push` uploads to configured remote. Without a remote, `dvc pull` on another machine fails.
- **Params granularity is per-key** -- `params` in `dvc.yaml` is a list of specific keys. A change to any listed key triggers re-run. A change to an unlisted key in the same file does NOT.
