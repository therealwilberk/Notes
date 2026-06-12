---
tags: [ml, python, fastapi, serving]
aliases: ["FastAPI cheatsheet"]
created: 2026-06-11
status: complete
parent: "[[MOCs/ML & Data Science Packages -- Map of Content]]"
---

## 80/20

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow.pyfunc

# Module-level model handle
model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    # Load model ONCE at startup -- not per request
    model = mlflow.pyfunc.load_model("models:/jua-demand-model/Production")
    yield
    model = None  # cleanup on shutdown

app = FastAPI(lifespan=lifespan)

# --- Request/response contracts (Pydantic) ---
class PredictRequest(BaseModel):
    site_id: str
    forecast_date: str  # "2024-06-01"
    features: dict[str, float]

class PredictResponse(BaseModel):
    site_id: str
    forecast_date: str
    predicted_kwh_24h: list[float]
    model_version: str

# --- Endpoints ---
@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "model_loaded": model is not None}

@app.post("/predict", response_model=PredictResponse)
async def predict(req: PredictRequest) -> PredictResponse:
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    ...

# Run: uvicorn src.serving.app:app --host 0.0.0.0 --port 8000
# Auto-generated docs: /docs (Swagger UI), /openapi.json (API schema)
```

## Lifecycle pattern

- **Lifespan** is the modern (FastAPI 2.0+) way to handle startup/shutdown. Replaces the old `@app.on_event("startup")` decorator.
- **Module-level `model`** is set once at startup and read by handlers. No per-request loading.

## Endpoints for an ML service

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Docker health check + model loaded indicator |
| `/predict` | POST | Return prediction(s) for given features |
| `/docs` | GET | Auto-generated Swagger UI (built-in) |
| `/openapi.json` | GET | API schema for codegen |

## Traps

- **Model loaded per request == OOM** -- always load model in lifespan, never inside the handler.
- **`model is None` check** -- FastAPI starts accepting requests before lifespan completes. Guard with 503 if model fails to load.
- **Pydantic v1 vs v2** -- the project uses Pydantic v2 (`BaseModel`, not `pydantic.BaseModel` from v1).
- **CORS for production** -- if serving to a web frontend, add `CORSMiddleware` with explicit origin allowlist.
- **Uvicorn workers** -- for multi-worker (`--workers N`), each worker has its own model loaded in memory. At N workers, you need N x model RAM.
