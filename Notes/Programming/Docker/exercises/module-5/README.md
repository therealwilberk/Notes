# Module 5 -- Docker Compose: Multi-Container Apps

**Learning objectives:**
- Define multi-service stacks with docker-compose.yml
- Wire services together with depends_on + health checks
- Set environment variables for service discovery
- Use named volumes across services

**Prerequisites:** Modules 1-4 complete.

---

## Exercise 5.1 -- FastAPI + MLflow Stack (Semi-Guided)

Build the core of your project's stack: a FastAPI app that connects to MLflow.

```bash
mkdir -p ~/docker-lab/ex5-1 && cd ~/docker-lab/ex5-1
```

**Part A -- Create the FastAPI app:**

`app.py`:

```python
import os
from fastapi import FastAPI
import mlflow.pyfunc

app = FastAPI()
model = None

@app.on_event("startup")
def startup():
    global model
    uri = os.environ.get("MLFLOW_TRACKING_URI", "http://localhost:5000")
    mlflow.set_tracking_uri(uri)
    app.state.mlflow_uri = uri
    print(f"MLflow URI: {uri}")

@app.get("/health")
def health():
    return {"status": "ok", "mlflow_uri": app.state.mlflow_uri}

@app.get("/")
def root():
    return {"message": "FastAPI + MLflow stack"}
```

`pyproject.toml`:

```toml
[project]
name = "ex5-1"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["fastapi>=0.110", "uvicorn[standard]>=0.27", "mlflow>=2.15"]
```

`Dockerfile`:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY pyproject.toml .
RUN uv sync --frozen
COPY app.py .
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0"]
```

**Part B -- Write docker-compose.yml:**

```yaml
services:
  mlflow:
    image: ghcr.io/mlflow/mlflow:v2.15.0
    ports: ["5000:5000"]
    volumes:
      - mlflow_db:/mlflow
      - mlflow_data:/mlflow/artifacts
    command: mlflow server --host 0.0.0.0 --backend-store-uri sqlite:///mlflow/mlflow.db --default-artifact-root /mlflow/artifacts
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000"]
      interval: 10s
      timeout: 5s
      retries: 5

  app:
    build: .
    ports: ["8000:8000"]
    environment:
      - MLFLOW_TRACKING_URI=http://mlflow:5000
    depends_on:
      mlflow:
        condition: service_healthy

volumes:
  mlflow_db:
  mlflow_data:
```

**Part C -- Run and verify:**

```bash
docker compose up --build -d
```

Check both services:

```bash
docker compose ps
curl localhost:8000/health
```

Expected: `{"status":"ok","mlflow_uri":"http://mlflow:5000"}`

Verify MLflow is reachable:

```bash
curl localhost:5000
```

**Clean up:**

```bash
docker compose down
```

---

## Exercise 5.2 -- Add Evidently Monitor (Semi-Guided)

Extend the stack from 5.1 to add an Evidently monitoring service.

```bash
cd ~/docker-lab/ex5-1
```

Your stack currently has `mlflow` and `app`. Add a third service:

```yaml
monitor:
  build: .
  depends_on:
    mlflow:
      condition: service_healthy
  environment:
    - MLFLOW_TRACKING_URI=http://mlflow:5000
  volumes:
    - evidently_reports:/app/reports
  mem_limit: 1g
  cpus: "0.5"
```

Add `evidently` to your `pyproject.toml` dependencies and rebuild.

**Add the volume to the volumes block at the bottom.**

Run the stack:

```bash
docker compose up --build -d
```

Verify all three services are running:

```bash
docker compose ps
```

Inspect the network connectivity:

```bash
docker compose exec app curl -s http://mlflow:5000
```

**Expected:** The app container can reach MLflow via the service name `mlflow`.

**Clean up:**

```bash
docker compose down
```

---

## Exercise 5.3 -- Health Check Diagnostic (Unguided)

Your compose stack works... until it doesn't. Run:

```bash
docker compose up -d
```

Now deliberately break the MLflow health check by changing its port (edit compose.yml to use a health check that connects to a port that doesn't exist). Recreate:

```bash
docker compose up -d
```

**Task:** Figure out what happens to `app`. Does it start? Is it healthy? Use `docker compose ps` and `docker compose logs app` to investigate.

**Fix:** Restore the correct health check port.

**Clean up:**

```bash
docker compose down
```

**Observation:** Without a proper health check, `depends_on: mlflow: condition: service_healthy` means `app` will never start because MLflow never reports healthy. This is a common production failure.
