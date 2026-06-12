# Module 7 -- Production Patterns & Security

**Learning objectives:**
- Harden a Dockerfile (non-root, health checks, resource limits)
- Audit an insecure compose stack
- Run a security scan on built images
- Write production compose overrides
- Capstone: improve the real project's Docker infrastructure

**Prerequisites:** All preceding modules complete.

---

## Exercise 7.1 -- Insecure Stack Hardening Audit (Unguided)

You are given a deliberately insecure docker-compose.yml. Your task: find and fix every security issue.

```bash
mkdir -p ~/docker-lab/ex7-1 && cd ~/docker-lab/ex7-1
```

`docker-compose.yml`:

```yaml
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DB_PASSWORD=supersecret
    volumes:
      - ./data:/app/data
    restart: always

  db:
    image: postgres:latest
    environment:
      - POSTGRES_PASSWORD=password123
    ports:
      - "5432:5432"
```

`Dockerfile`:

```dockerfile
FROM python:latest
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD python app.py
```

`requirements.txt`:

```
fastapi
uvicorn
psycopg2-binary
```

`app.py`:

```python
import os
from fastapi import FastAPI

app = FastAPI()
DB_PASSWORD = os.environ["DB_PASSWORD"]

@app.get("/")
def root():
    return {"db_password": DB_PASSWORD}
```

**Find at least 8 issues.** Here's a starting list:

1. `latest` tags in FROM (unpredictable builds)
2. Running as root
3. Secret in environment variable (exposed via API!)
4. No health checks
5. No resource limits
6. Exposing database port to host
7. No .dockerignore (build context bloat)
8. `COPY . /app` before pip install (cache busting)
9. psycopg2-binary (not for production)
10. Full python image instead of slim
11. Password in compose file (should be in .env or secret store)
12. No network isolation (db is on same network as app)

**Fix each issue and verify the stack still works.**

---

## Exercise 7.2 -- Capstone: Audit and Improve Your Project (You're On Your Own)

**Your goal:** Apply everything you've learned to improve the Docker infrastructure of the real project (jua-ml).

**Step 1 -- Fetch the real files:**

```bash
# Copy the project's Dockerfile and docker-compose.yml to a working directory
cp /path/to/project/Dockerfile ~/docker-lab/capstone/
cp /path/to/project/docker-compose.yml ~/docker-lab/capstone/
```

Or create realistic versions based on your project:

**Dockerfile** (multi-stage, uv, LightGBM):
```dockerfile
FROM python:3.11-slim AS builder
RUN apt-get update && apt-get install -y libgomp1
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

FROM python:3.11-slim AS runtime
COPY --from=builder /app/.venv /app/.venv
COPY src/ /app/src/
ENV PATH="/app/.venv/bin:$PATH"
ENTRYPOINT ["python", "-m", "src.app"]
```

**docker-compose.yml** (3 services):
```yaml
services:
  mlflow:
    image: ghcr.io/mlflow/mlflow:v2.15.0
    ports: ["5000:5000"]
    volumes:
      - mlflow_db:/mlflow
      - mlflow_data:/mlflow/artifacts
    command: mlflow server --host 0.0.0.0 --backend-store-uri sqlite:///mlflow/mlflow.db --default-artifact-root /mlflow/artifacts

  app:
    build: .
    ports: ["8000:8000"]
    depends_on: [mlflow]
    environment:
      - MLFLOW_TRACKING_URI=http://mlflow:5000
    volumes:
      - model_cache:/app/model_cache

  monitor:
    build: .
    depends_on: [mlflow]
    environment:
      - MLFLOW_TRACKING_URI=http://mlflow:5000
    volumes:
      - evidently_reports:/app/reports

volumes:
  mlflow_db:
  mlflow_data:
  model_cache:
  evidently_reports:
```

**Improvement checklist:**

- [ ] Add `# syntax=docker/dockerfile:1.7` header
- [ ] Add `--mount=type=cache,target=/root/.cache/uv` to uv sync
- [ ] Add non-root user in runtime stage
- [ ] Add HEALTHCHECK to Dockerfile
- [ ] Add resource limits (`mem_limit`, `cpus`) to each compose service
- [ ] Change `depends_on` to `condition: service_healthy` where needed
- [ ] Add healthchecks to all compose services
- [ ] Add `.dockerignore` (git, venv, data, cache, pyc, parquet, csv, models)
- [ ] Create `docker-compose.prod.yml` with production overrides (more replicas for app, higher resource limits)
- [ ] Pin base image versions (not just `python:3.11-slim`, use specific like `python:3.11.9-slim`)
- [ ] Add restart policies (`unless-stopped`)

**Verify:**
```bash
docker compose up --build
docker compose ps
# All services should be running and healthy
```

---

## Before You Ship: Production Checklist

- [ ] All images use specific version tags, not `latest`
- [ ] Containers run as non-root user
- [ ] Health checks defined on every service
- [ ] Resource limits set on every service
- [ ] `.dockerignore` exists and excludes unnecessary files
- [ ] No secrets in Dockerfiles or docker-compose.yml
- [ ] Multi-stage build used, runtime image is minimal
- [ ] `docker scout` scan shows no critical CVEs
- [ ] Depends_on uses `condition: service_healthy` where needed
- [ ] Named volumes used for persistent data (not bind mounts in prod)
- [ ] Restart policy set to `unless-stopped`
- [ ] Port mappings only expose what's necessary
- [ ] Network isolation between services (if applicable)
- [ ] Production override file exists for env-specific config
