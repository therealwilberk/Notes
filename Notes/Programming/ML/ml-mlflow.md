---
tags: [ml, python, mlflow, experiment-tracking, model-registry]
aliases: ["MLflow cheatsheet"]
created: 2026-06-11
status: complete
parent: "[[MOCs/ML & Data Science Packages -- Map of Content]]"
---

## 80/20

```python
import mlflow
from mlflow import MlflowClient

# Point to tracking server
mlflow.set_tracking_uri("http://localhost:5000")

# Create or activate experiment
mlflow.set_experiment("jua-demand-forecast")

with mlflow.start_run(run_name="lgbm-v2") as run:
    # Log params
    mlflow.log_params({"learning_rate": 0.05, "num_leaves": 64})

    # Log metrics (multiple calls per key build a time series)
    mlflow.log_metric("mape", 14.3)
    mlflow.log_metric("mape", 13.8)  # another step

    # Log artifact (plot, report, HTML)
    mlflow.log_artifact("reports/eval_report.html")

    # Log the model (LightGBM flavour)
    mlflow.lightgbm.log_model(model, "model")

# Register model from a run into the registry
run_id = run.info.run_id
model_uri = f"runs:/{run_id}/model"
mlflow.register_model(model_uri, "jua-demand-model")

# Promote stage
client = MlflowClient()
client.transition_model_version_stage(
    name="jua-demand-model",
    version=1,
    stage="Production"
)

# Load from registry (always gets whatever is in Production)
loaded = mlflow.pyfunc.load_model("models:/jua-demand-model/Production")
```

## Tracking API

| Function | Purpose |
|----------|---------|
| `set_tracking_uri(uri)` | point to MLflow server (or `env MLFLOW_TRACKING_URI`) |
| `set_experiment(name)` | create or activate experiment |
| `start_run(run_name=)` | context manager -- auto-closes on crash |
| `log_params(dict)` | log hyperparams (flat dict, no nested) |
| `log_metric(key, val)` | log a scalar (multiple calls = time series) |
| `log_artifact(path)` | save file to run's artifact store |
| `lightgbm.log_model(model, "model")` | log LGBM model as pyfunc-compatible artifact |
| `register_model(uri, name)` | register from run into registry |

## Model Registry stages

`None -> Staging -> Production -> Archived`

```python
client.transition_model_version_stage("model-name", version=2, stage="Staging")
```

Load from registry:
```python
mlflow.pyfunc.load_model("models:/model-name/Production")
mlflow.pyfunc.load_model("models:/model-name/Staging")
mlflow.pyfunc.load_model(f"models:/model-name/version/{version}")
```

## Traps

- **`log_params` does not accept nested dicts or lists** -- flatten or convert to string first.
- **Tracking URI in Docker** -- use service name instead of localhost: `MLFLOW_TRACKING_URI=http://mlflow:5000`.
- **Artifact store path in Docker** -- MLflow must have persistent volumes (`mlflow_data`, `mlflow_db`) or data is lost on container restart.
- **`MlflowClient` vs fluent API** -- `mlflow.log_param(...)` is the fluent (convenient) API. Use `MlflowClient` for registry operations.
- **Pyfunc vs native flavour** -- `mlflow.pyfunc.load_model` returns a generic wrapper. If you need the native Booster, use `mlflow.lightgbm.load_model`.
