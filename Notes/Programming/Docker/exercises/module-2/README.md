# Module 2 -- Dockerfiles: Writing Your First Image

**Learning objectives:**
- Write a Dockerfile from scratch
- Understand FROM, RUN, COPY, WORKDIR, ENTRYPOINT, CMD
- Use uv for dependency management in Dockerfiles
- Optimize layer ordering for caching
- Use .dockerignore to slim the build context
- Distinguish CMD from ENTRYPOINT
- Use build args (ARG)

**Prerequisites:** Module 1 complete. Docker installed. Basic Python knowledge.

---

## Exercise 2.1 -- Dockerfile for a Simple Python Script (Guided)

Create a new directory and enter it:

```bash
mkdir -p ~/docker-lab/ex2-1 && cd ~/docker-lab/ex2-1
```

Create a Python script called `hello.py`:

```python
import sys
print(f"Hello from Docker! Python {sys.version}")
```

Create a Dockerfile:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY hello.py .
CMD ["python", "hello.py"]
```

**Build it:**

```bash
docker build -t hello-py .
```

**Run it:**

```bash
docker run hello-py
```

**Expected output:** `Hello from Docker! Python 3.11.x...`

**Check the image size:**

```bash
docker images | grep hello-py
```

Notice how small it is (~50 MB for the slim base, ~100 bytes for your script).

**Clean up:**

```bash
docker rmi hello-py
```

---

## Exercise 2.2 -- Dockerfile with uv + FastAPI (Guided)

This mirrors your project's actual tooling.

Create:

```bash
mkdir -p ~/docker-lab/ex2-2 && cd ~/docker-lab/ex2-2
```

Create `app.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from Docker + uv!"}

@app.get("/health")
def health():
    return {"status": "ok"}
```

Create `pyproject.toml`:

```toml
[project]
name = "demo-app"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.110",
    "uvicorn[standard]>=0.27",
]
```

Create Dockerfile:

```dockerfile
FROM python:3.11-slim
WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files first (for layer caching)
COPY pyproject.toml .
RUN uv sync --frozen

# Copy application code last
COPY app.py .

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Build and run:**

```bash
docker build -t fastapi-demo .
docker run -d -p 8000:8000 --name fastapi-demo fastapi-demo
```

**Verify:**

```bash
curl localhost:8000
# Expected: {"message":"Hello from Docker + uv!"}

curl localhost:8000/health
# Expected: {"status":"ok"}
```

**Check image size:**

```bash
docker images | grep fastapi-demo
```

**Clean up:**

```bash
docker stop fastapi-demo && docker rm fastapi-demo
```

---

## Exercise 2.3 -- Optimize Layer Order (Semi-Guided)

**Your goal:** Look at the Dockerfile below and fix the layer ordering so that code changes don't bust the dependencies cache.

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY . .
RUN uv sync --frozen
CMD ["uv", "run", "python", "app.py"]
```

**Problem:** `COPY . .` happens before `RUN uv sync`. Every time any file changes (even a README), uv re-downloads every dependency.

**Hint:** Split the COPY. Copy dependency files first, run uv sync, then copy the rest.

**Add a .dockerignore file too.** What should you exclude? (Think: git, python cache, venv, env files.)

---

## Exercise 2.4 -- CMD vs ENTRYPOINT Experiment (Semi-Guided)

**Your goal:** Understand the difference between CMD and ENTRYPOINT.

Create `~/docker-lab/ex2-4/` with a Dockerfile:

```dockerfile
FROM alpine:latest
CMD ["echo", "default command"]
```

Build and run:

```bash
docker build -t cmd-test ~/docker-lab/ex2-4
docker run cmd-test
# Expected: "default command"

docker run cmd-test echo "overridden"
# Expected: "overridden" -- CMD is overridden
```

Now change CMD to ENTRYPOINT:

```dockerfile
FROM alpine:latest
ENTRYPOINT ["echo"]
CMD ["default argument"]
```

Rebuild:

```bash
docker build -t entrypoint-test ~/docker-lab/ex2-4
docker run entrypoint-test
# Expected: "default argument"

docker run entrypoint-test custom
# Expected: "custom"

docker run --entrypoint sh entrypoint-test
# Expected: drops into shell -- ENTRYPOINT is overridden
```

**Observation:** CMD is the default command (easily overridden). ENTRYPOINT provides a fixed base that CMD appends to.

---

## Exercise 2.5 -- Build Args (Guided)

Create `~/docker-lab/ex2-5/` with:

```dockerfile
FROM python:3.11-slim
ARG VERSION=unknown
RUN echo "Building version: $VERSION"
```

Build with defaults:

```bash
docker build -t args-test ~/docker-lab/ex2-5
```

Build with a custom arg:

```bash
docker build --build-arg VERSION=2.0 -t args-test ~/docker-lab/ex2-5
```

**Observation:** each build shows a different echo, but the running container has no VERSION env var (unless you also set ENV).
