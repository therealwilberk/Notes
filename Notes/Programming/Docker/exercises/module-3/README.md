# Module 3 -- Multi-Stage Builds & Image Optimization

**Learning objectives:**
- Split a naive Dockerfile into multi-stage build
- Measure image size before and after
- Use cache mounts to speed up builds
- Choose appropriate base images (slim vs alpine vs distroless)
- Handle LightGBM's libgomp dependency in containers

**Prerequisites:** Module 2 complete. Docker installed.

---

## Exercise 3.1 -- Split a Naive Dockerfile (Semi-Guided)

You have this naive Dockerfile for a Streamlit app:

```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install streamlit pandas numpy
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

**Your goal:** Split it into a multi-stage build.

1. Builder stage: install dependencies in a virtual environment
2. Runtime stage: copy only the venv and source code

**Hint:** The builder installs deps. The runtime copies the venv from builder. Use `python -m venv /venv` and `COPY --from=builder /venv /venv` + `ENV PATH=/venv/bin:$PATH`.

**Measure before and after:**

```bash
docker build -t naive -f Dockerfile.naive .
docker build -t optimized -f Dockerfile.optimized .
docker images | grep -E "naive|optimized"
```

**Expected result:** The optimized image should be significantly smaller (the builder may be 1GB+, but the runtime should be ~200MB).

---

## Exercise 3.2 -- Optimize Your Project's Dockerfile (Semi-Guided)

Your project has a Dockerfile similar to this:

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

**Task:** Add two improvements:

1. **Cache mount:** Add `--mount=type=cache,target=/root/.cache/uv` to the uv sync line. Remember the BuildKit header.
2. **Non-root user:** Add a non-root user in the runtime stage and switch to it.

**Hint:** Use `addgroup --system --gid 1001 appgroup && adduser --system --uid 1001 --ingroup appgroup appuser` then `USER appuser`. You'll need to adjust permissions on `/app` if the app writes files.

**Expected result:** Dockerfile that starts with `# syntax=docker/dockerfile:1.7`, uses cache mounts, and runs as non-root.

---

## Exercise 3.3 -- Base Image Comparison (Semi-Guided)

Build the same simple app on three different base images and compare:

```bash
mkdir -p ~/docker-lab/ex3-3 && cd ~/docker-lab/ex3-3
```

Create `app.py`:

```python
import numpy as np
print(f"numpy version: {np.__version__}")
```

Create three Dockerfiles:

- `Dockerfile.slim` -- uses `python:3.11-slim`
- `Dockerfile.alpine` -- uses `python:3.11-alpine`
- `Dockerfile.distroless` -- uses `gcr.io/distroless/python3-debian12` (you'll need to copy the venv differently)

Each should install numpy in a venv.

**Compare sizes:**

```bash
docker images | grep ex3-3
```

**Check which ones build without error.** The alpine variant may fail on numpy compilation.

---

## Exercise 3.4 -- LightGBM Docker Trap (Semi-Guided)

Create a minimal Dockerfile that imports LightGBM:

```dockerfile
FROM python:3.11-slim
RUN pip install lightgbm
RUN python -c "import lightgbm; print('OK')"
```

**Build and run:**

```bash
docker build -t lgbm-test .
```

**Expected:** It will likely fail with `OSError: libgomp.so.1: cannot open shared object file`. This is the LightGBM OpenMP trap.

**Fix:** Add `RUN apt-get update && apt-get install -y libgomp1` before the pip install line. Then rebuild.

**Note:** In a multi-stage build, install `libgomp1` in the builder stage AND the runtime stage if the runtime image also needs LightGBM (not just the built artifacts).
