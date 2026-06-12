# Module 4 -- Volumes & Data Persistence

**Learning objectives:**
- Create and use named volumes
- Understand data lifecycle
- Use bind mounts for development
- Set up persistent MLflow storage
- Understand the danger of `docker compose down -v`

**Prerequisites:** Modules 1-3 complete.

---

## Exercise 4.1 -- MLflow with Persistent Storage (Semi-Guided)

Run an MLflow tracking server with persistent storage:

```bash
mkdir -p ~/docker-lab/ex4-1 && cd ~/docker-lab/ex4-1
```

**Part A -- Without volumes (data loss):**

```yaml
# docker-compose.yml
services:
  mlflow:
    image: ghcr.io/mlflow/mlflow:v2.15.0
    ports: ["5000:5000"]
    command: mlflow server --host 0.0.0.0 --backend-store-uri sqlite:///mlflow.db --default-artifact-root /mlflow/artifacts
```

```bash
docker compose up -d
```

Create a test experiment:

```bash
curl -X POST "http://localhost:5000/api/2.0/mlflow/experiments/create" -H "Content-Type: application/json" -d '{"name": "test-exp"}'
```

Take down the stack:

```bash
docker compose down
```

Now bring it back up:

```bash
docker compose up -d
```

Check if the experiment still exists:

```bash
curl "http://localhost:5000/api/2.0/mlflow/experiments/list"
```

**Expected:** The experiment is gone. Data was stored in the container's writable layer, which was destroyed when the container was removed.

```bash
docker compose down
```

**Part B -- With named volumes (persistent):**

Update `docker-compose.yml`:

```yaml
services:
  mlflow:
    image: ghcr.io/mlflow/mlflow:v2.15.0
    ports: ["5000:5000"]
    volumes:
      - mlflow_db:/mlflow
      - mlflow_data:/mlflow/artifacts
    command: mlflow server --host 0.0.0.0 --backend-store-uri sqlite:///mlflow/mlflow.db --default-artifact-root /mlflow/artifacts

volumes:
  mlflow_db:
  mlflow_data:
```

```bash
docker compose up -d
```

Create another experiment:

```bash
curl -X POST "http://localhost:5000/api/2.0/mlflow/experiments/create" -H "Content-Type: application/json" -d '{"name": "persistent-exp"}'
```

Now destroy and recreate:

```bash
docker compose down
docker compose up -d
```

**Check if the experiment persists:**

```bash
curl "http://localhost:5000/api/2.0/mlflow/experiments/list"
```

**Expected:** The experiment is still there. The data was stored in the named volume, which survives `docker compose down`.

---

## Exercise 4.2 -- The Nuclear Option (Semi-Guided)

Continue from Exercise 4.1. Your MLflow still has `persistent-exp`.

Now run the destructive command:

```bash
docker compose down -v
```

**Observe the warning:** Docker doesn't warn you. It just deletes the volumes.

Bring it back up and check:

```bash
docker compose up -d
curl "http://localhost:5000/api/2.0/mlflow/experiments/list"
```

**Expected:** The experiment list is empty again. The volume was deleted.

**Lesson:** `docker compose down -v` is the nuclear option for ML projects. It destroys your experiment history, model registry, and any other data in named volumes.

---

## Exercise 4.3 -- Bind Mounts for Dev (Semi-Guided)

Bind mounts let you edit code on your host and have changes reflected instantly in the container (no rebuild needed).

```bash
mkdir -p ~/docker-lab/ex4-3 && cd ~/docker-lab/ex4-3
```

Create `app.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Bind mounts work!"}
```

Create a Dockerfile:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY pyproject.toml .
RUN uv sync --frozen
COPY app.py .
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create `pyproject.toml`:

```toml
[project]
name = "bind-mount-demo"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["fastapi>=0.110", "uvicorn[standard]>=0.27"]
```

Build the image first:

```bash
docker build -t bind-demo .
```

Now run with a bind mount instead of copying the code:

```bash
docker run -d -p 8000:8000 --name bind-demo -v $(pwd)/app.py:/app/app.py bind-demo
```

**This mounts your local app.py into the container, overriding the one baked into the image.**

Test it:

```bash
curl localhost:8000
# Expected: {"message":"Bind mounts work!"}
```

Now edit `app.py` without rebuilding -- change the message, then save. Wait a couple seconds and curl again:

```bash
curl localhost:8000
```

**Expected:** The new message is returned without any rebuild or restart. (This works because uvicorn supports hot reload, but even without it, you only need to restart the container -- no rebuild.)

**Clean up:**

```bash
docker stop bind-demo && docker rm bind-demo
```

Note: for real development, you'd use `--reload` with uvicorn and mount the entire source directory, not just one file.
