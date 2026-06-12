---
tags: [docker, security, production, ci-cd]
aliases: ["Docker Module 7"]
created: 2026-06-11
parent: "[[docker|Docker MOC]]"
exercises: "[[exercises/module-7]]"
---

## Non-Root User

By default, containers run as root. If the app is compromised, the attacker has root inside the container.

```dockerfile
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --ingroup appgroup appuser

USER appuser

RUN mkdir -p /app/model_cache && chown appuser:appgroup /app/model_cache
```

## Resource Limits

Without limits, one container can starve the host:

```yaml
services:
  app:
    mem_limit: 2g           # hard limit (OOM-kill if exceeded)
    mem_reservation: 1g     # soft reservation
    cpus: "1.5"             # max 1.5 CPU cores
```

**LightGBM OOM trap**: training on a large dataset can consume 10+ GB. If `mem_limit` is too low, the container gets OOM-killed mid-training.

## Health Checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1
```

Docker marks the container as `healthy` or `unhealthy`. Compose can wait for healthy before starting dependents.

## Image Vulnerability Scanning

```bash
docker scout cves my-image:latest     # list all CVEs
docker scout quickview my-image       # summary
docker scout recommendations my-image # fix suggestions
```

Scout is built into Docker Desktop and Docker CLI. Integrate into CI via `docker/scout-action`.

## CI/CD Pattern

```yaml
# .github/workflows/build.yml
- name: Build and push
  uses: docker/build-push-action@v5
  with:
    push: true
    tags: user/app:latest
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

## Rootless Mode

Runs the daemon as a non-root user:

```bash
dockerd-rootless-setuptool.sh install
export DOCKER_HOST=unix:///run/user/1000/docker.sock
```

Tradeoff: cannot bind to privileged ports (< 1024), some network features limited.

## Compose Production Override

```yaml
# docker-compose.prod.yml
services:
  app:
    build:
      args:
        ENV: prod
    deploy:
      replicas: 3
    restart: always
    mem_limit: 4g
```

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Platform / Architecture

```bash
docker build --platform linux/amd64 .
docker build --platform linux/amd64,linux/arm64 .
```

ML caveat: many base images don't have ARM wheels for numpy/lightgbm. Building on Apple Silicon may fall back to source compilation.
