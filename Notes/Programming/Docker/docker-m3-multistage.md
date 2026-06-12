---
tags: [docker, multi-stage, optimization]
aliases: ["Docker Module 3"]
created: 2026-06-11
parent: "[[docker|Docker MOC]]"
exercises: "[[exercises/module-3]]"
---

## Why Multi-Stage

A naive Dockerfile drags build tools (compilers, pip, uv itself, gcc) into the final image -- easily 1GB+ for a Python ML app. Multi-stage separates **build** from **runtime**:

```dockerfile
# === BUILDER stage: heavy tools live here ===
FROM python:3.11-slim AS builder
RUN apt-get update && apt-get install -y libgomp1  # LightGBM needs OpenMP
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# === RUNTIME stage: only what's needed to run ===
FROM python:3.11-slim AS runtime
COPY --from=builder /app/.venv /app/.venv     # copy only the venv
COPY src/ /app/src/
ENV PATH="/app/.venv/bin:$PATH"
ENTRYPOINT ["python", "-m", "src.app"]
```

Final image: ~300 MB instead of 1.2 GB. No gcc, no uv, no build cache.

## Base Image Choices

| Image | Size | Shell | Package Mgr | Use Case |
|-------|------|-------|-------------|----------|
| `ubuntu:22.04` | 77 MB | bash | apt | dev/debug |
| `python:3.11-slim` | 50 MB | bash | apt (minimal) | production, Python |
| `python:3.11-alpine` | 18 MB | sh | apk | small footprint, but musl caveats |
| `gcr.io/distroless/python3` | ~25 MB | none | none | max security (no shell) |
| `scratch` | 0 MB | none | none | static binaries (Go, Rust) |

**Alpine caveat**: uses musl libc, not glibc. Can cause segfaults with numpy, LightGBM, and other C-extension-heavy packages. When in doubt, use `-slim`.

## Cache Mounts (BuildKit)

```dockerfile
# syntax=docker/dockerfile:1.7
FROM python:3.11-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen
```

The `--mount=type=cache` persists `/root/.cache/uv` across builds. Without it, every build re-downloads every package from scratch. Cuts build time from 5 minutes to 30 seconds.

## .dockerignore (critical)

```dockerignore
.git
.gitignore
__pycache__/
*.pyc
.venv/
.env
data/
*.parquet
*.csv
*.zip
models/
.DS_Store
Dockerfile
docker-compose*.yml
```

Each line is a glob. Without this, `COPY . .` sends gigabytes of data to the Docker daemon for every build.

## Traps

- **`libgomp1` for LightGBM** -- crashes with "cannot open shared object file" if OpenMP is missing. Always `apt-get install -y libgomp1` in the builder stage.
- **`--mount=type=cache` requires BuildKit** -- the `# syntax=docker/dockerfile:1.7` header must be the first line. Without it, `--mount` silently fails or errors.
- **Distroless has no shell** -- no `bash`, `sh`, `curl`, `ps`. Can't exec in and debug. Use for hardened production but keep a slim image for dev.
- **Alpine + numpy** -- numpy wheels are `manylinux`, not `musllinux` on some architectures. May fall back to source compilation, taking 20+ minutes.
