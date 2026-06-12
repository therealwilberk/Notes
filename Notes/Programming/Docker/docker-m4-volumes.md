---
tags: [docker, volumes, persistence]
aliases: ["Docker Module 4"]
created: 2026-06-11
parent: "[[docker|Docker MOC]]"
exercises: "[[exercises/module-4]]"
---

## The Problem

Every container starts with a fresh filesystem. When it stops, data written to it is gone. Volumes persist data outside the container's ephemeral layer.

## Named Volumes vs Bind Mounts

| | Named Volume | Bind Mount |
|---|---|---|
| Managed by | Docker (`docker volume`) | You |
| Location | `/var/lib/docker/volumes/...` | Any host path you specify |
| Backup | `docker run --volumes-from` or tar | Standard file tools |
| Use case | Persistent DB data, MLflow artifacts | Dev hot-reload, config files |

```bash
docker volume create mlflow_data                  # create named volume
docker run -v mlflow_data:/mlflow/artifacts ...   # mount it

docker run -v $(pwd)/data:/data ...               # bind mount
```

## Data Lifecycle

```
docker compose up  ->  containers created  ->  write data
   (volumes created)
docker compose down  ->  containers removed  ->  volumes STILL EXIST
docker compose down -v  ->  containers removed  ->  volumes DELETED  <-- DATA LOSS
```

**`docker compose down -v` is the nuclear option.** For an MLflow project:
- SQLite database (`mlflow.db`) is gone -- all experiment history erased
- Artifact store (`/mlflow/artifacts`) is gone -- all model binaries, plots, reports erased
- Evidently reports are gone -- all drift history erased

Never run `down -v` unless you explicitly mean to wipe everything.

## Compose Volume Patterns

```yaml
services:
  mlflow:
    volumes:
      - mlflow_data:/mlflow/artifacts   # named volume (persists)
      - mlflow_db:/mlflow               # named volume for SQLite
  app:
    volumes:
      - model_cache:/app/model_cache    # model download cache
  monitor:
    volumes:
      - evidently_reports:/app/reports  # drift report storage

volumes:
  mlflow_data:
  mlflow_db:
  model_cache:
  evidently_reports:
```

## Permission Gotchas

When mounting a named volume, Docker creates it as root. If your container runs as `USER 1000`, it can't write to the volume:

```dockerfile
RUN mkdir -p /data && chown 1000:1000 /data
USER 1000
```

Or use `COPY --chown=1000` in the Dockerfile. In compose, you can't chown volumes directly -- the Dockerfile must create the directory with correct ownership.
