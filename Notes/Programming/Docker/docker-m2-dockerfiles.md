---
tags: [docker, dockerfile, images]
aliases: ["Docker Module 2"]
created: 2026-06-11
parent: "[[docker|Docker MOC]]"
exercises: "[[exercises/module-2]]"
---

## Instructions Reference

| Instruction | Purpose | Layer? |
|-------------|---------|--------|
| `FROM image` | Base image | Yes |
| `RUN command` | Execute during build | Yes |
| `COPY src dst` | Copy files from build context | Yes |
| `ADD src dst` | Copy + tar extraction + URL support | Yes |
| `WORKDIR /path` | Set working directory (creates if missing) | No (metadata) |
| `ENV KEY=val` | Environment variable at build + runtime | No (metadata) |
| `ARG NAME` | Build-time variable (not in final image) | No (metadata) |
| `EXPOSE port` | Document which port the container listens on | No (metadata) |
| `CMD ["cmd", "arg"]` | Default command (can be overridden) | No (metadata) |
| `ENTRYPOINT ["cmd"]` | Fixed command (hard to override) | No (metadata) |
| `USER uid` | Switch to non-root user | No (metadata) |
| `HEALTHCHECK CMD` | Check if container is healthy | No (metadata) |
| `LABEL key=val` | Metadata (maintainer, version, etc) | No (metadata) |

## CMD vs ENTRYPOINT

Both define the startup command. The interaction is the first footgun:

```
ENTRYPOINT ["python"]       # fixed
CMD ["app.py"]              # default argument (overridable)
# -> runs: python app.py

# Override CMD:
docker run myimg other.py   # runs: python other.py

# Override ENTRYPOINT:
docker run --entrypoint bash myimg   # runs: bash
```

**Shell form** vs **exec form**:

```dockerfile
CMD python app.py            # shell: /bin/sh -c "python app.py"
CMD ["python", "app.py"]     # exec: direct (preferred, SIGTERM goes to your app)
```

Shell form spawns a shell process. Ctrl+C (SIGTERM) goes to the shell, not your app. Exec form sends signals directly to your app process.

## Layer Caching Rules

1. Each instruction creates a layer cache entry keyed by the instruction text + its inputs
2. If the cache matches, Docker skips re-execution
3. If a layer **changes**, all subsequent layers are **invalidated** and rebuilt

**Good order** (least-changing first):
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml uv.lock ./     # deps change rarely
RUN uv sync --frozen               # cached until deps change
COPY src/ ./src/                    # code changes often, last
```

**Bad order** (code change busts everything):
```dockerfile
COPY . .                           # any file change busts cache
RUN uv sync --frozen               # re-downloads everything every time
```

## Build Context

The directory you pass to `docker build .` -- everything in it is sent to the Docker daemon. Without `.dockerignore`, sending a 2GB data directory makes builds agonizingly slow.

Always create `.dockerignore`:
```
.git
__pycache__
*.pyc
.env
.venv
data/
*.parquet
*.csv
.DS_Store
```

## ARG / Build Args

```dockerfile
ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim
ARG ENV=dev
RUN echo "Building for $ENV"
```

```bash
docker build --build-arg PYTHON_VERSION=3.12 --build-arg ENV=prod .
```

ARG values are only available during build, not in the running container. They don't create layers.

## Complete Example (uv + FastAPI)

```dockerfile
FROM python:3.11-slim
WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY src/ ./src/

EXPOSE 8000
CMD ["uv", "run", "python", "-m", "src.app"]
```
