---
tags: [docker, compose, multi-container]
aliases: ["Docker Module 5"]
created: 2026-06-11
parent: "[[docker|Docker MOC]]"
exercises: "[[exercises/module-5]]"
---

## Why Compose

`docker run` is fine for one container. Real apps need multiple services: MLflow server + FastAPI app + Evidently monitor. Compose defines them in one YAML file.

## Core Structure

```yaml
services:
  mlflow:
    image: ghcr.io/mlflow/mlflow:v2.15.0    # use pre-built image
    ports: ["5000:5000"]                     # host:container
    volumes:
      - mlflow_data:/mlflow/artifacts
    command: mlflow server --host 0.0.0.0
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000"]
      interval: 30s
      retries: 3

  app:
    build: .                                 # build from Dockerfile
    ports: ["8000:8000"]
    depends_on:
      mlflow:
        condition: service_healthy           # wait for MLflow to be ready
    environment:
      - MLFLOW_TRACKING_URI=http://mlflow:5000
    volumes:
      - model_cache:/app/model_cache
    mem_limit: 2g
    cpus: "1.5"

volumes:
  mlflow_data:
  mlflow_db:
  model_cache:
```

## Key Commands

```bash
docker compose up                   # start services
docker compose up --build           # rebuild + start
docker compose up -d                # start detached
docker compose down                 # stop + remove containers
docker compose down -v              # stop + remove containers + volumes (data loss!)
docker compose ps                   # status
docker compose logs -f              # follow all logs
docker compose logs -f app          # follow one service
docker compose build                # build images (without starting)
docker compose build --no-cache     # rebuild from scratch
docker compose restart app          # restart one service
docker compose exec app bash        # exec into a service container
```

## depends_on vs healthcheck

`depends_on` alone only waits for the container to start, not for the service inside to be ready:

```yaml
depends_on:
  - mlflow              # waits for container start only

# Better:
depends_on:
  mlflow:
    condition: service_healthy   # waits for healthcheck to pass
```

Without this, `app` might crash because MLflow isn't accepting connections yet.

## Restart Policies

```yaml
restart: "no"               # never restart (default)
restart: always             # always restart, even if manually stopped
restart: on-failure         # restart only on non-zero exit
restart: unless-stopped     # restart unless manually stopped (recommended)
```

## Multi-Service Logging

```bash
docker compose logs -f              # all services
docker compose logs -f --tail=100   # last 100 lines per service
docker compose logs -f app          # one service only
```

Compose prefixes each log line with the service name.

## Compose Overrides for Production

```yaml
# docker-compose.prod.yml
services:
  app:
    deploy:
      replicas: 3
    restart: always
```

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```
