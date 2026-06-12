---
tags: [docker, containers, devops, moc]
aliases: ["Docker MOC", "Docker Reference"]
created: 2026-06-11
status: in-progress
---

## 80/20

```bash
# Lifecycle
docker build -t my-image .            # build image from Dockerfile
docker run -d -p 8080:80 --name n1 nginx  # run detached with port mapping
docker ps                              # running containers
docker ps -a                           # all containers
docker stop n1 && docker rm n1         # stop then remove
docker logs -f n1                      # follow logs
docker exec -it n1 bash                # open shell inside running container
docker inspect n1                      # detailed config (mounts, network, env)

# Images
docker images                          # list local images
docker pull python:3.11-slim           # pull from registry
docker rmi python:3.11-slim            # remove image
docker tag my-img user/my-img:1.0      # tag for registry
docker push user/my-img:1.0            # push to registry

# Volumes
docker volume create my-vol            # create named volume
docker volume ls                       # list volumes

# Compose
docker compose up --build              # build + start all services
docker compose down                    # stop + remove containers
docker compose down -v                 # stop + remove containers AND volumes
docker compose ps                      # service status
docker compose logs -f                 # follow all service logs
docker compose build --no-cache        # rebuild from scratch

# Cleanup
docker system prune                    # remove stopped containers, dangling images
docker system prune -a                 # nuke everything unused
docker system df                       # disk usage
```

## Modules

| Module | File | Topics | Exercises |
|--------|------|--------|----------|
| 1 -- Containers | [[docker-m1-containers\|docker-m1]] | image vs container, layer model, run/exec/logs/inspect, port mapping | [[exercises/module-1\|ex1]] |
| 2 -- Dockerfiles | [[docker-m2-dockerfiles\|docker-m2]] | FROM/RUN/COPY/CMD/ENTRYPOINT, layer caching, .dockerignore, ARG, uv | [[exercises/module-2\|ex2]] |
| 3 -- Multi-Stage | [[docker-m3-multistage\|docker-m3]] | builder vs runtime, base image choices, BuildKit cache mounts, libgomp | [[exercises/module-3\|ex3]] |
| 4 -- Volumes | [[docker-m4-volumes\|docker-m4]] | named vs bind, data lifecycle, `down -v` danger, permissions | [[exercises/module-4\|ex4]] |
| 5 -- Compose | [[docker-m5-compose\|docker-m5]] | multi-service YAML, depends_on + healthcheck, restart policies, overrides | [[exercises/module-5\|ex5]] |
| 6 -- Networking | [[docker-m6-networking\|docker-m6]] | bridge, DNS, custom networks, port mapping gotchas | [[exercises/module-6\|ex6]] |
| 7 -- Production | [[docker-m7-production\|docker-m7]] | non-root, resource limits, scout, CI/CD, rootless, platform | [[exercises/module-7\|ex7]] |

## Traps

- **`docker compose down -v` destroys volumes** -- MLflow DB, artifacts, Evidently reports gone forever
- **Missing `libgomp1` in Dockerfile** -- LightGBM crashes at import in containers
- **Port conflict** -- `Error response from daemon: driver failed programming external connectivity`
- **depends_on without healthcheck** -- services start but can't connect
- **`COPY . .` without .dockerignore** -- sends venv (500MB+) every build
- **alpine + numpy/lightgbm** -- musl causes segfaults with C extensions
- **Cache mounts need BuildKit header** -- `# syntax=docker/dockerfile:1.7` must be first line
- **Distroless has no shell** -- can't `docker exec` to debug
- **Running as root in production** -- container escape vulnerability
- **No resource limits** -- one OOM kill stalls all services
- **ENTRYPOINT shell form** -- `CMD python app.py` wraps in `/bin/sh -c`, signals don't propagate
- **Build context too large** -- check size with first `docker build .`
- **Exit code 139** -- segfault, often Alpine compatibility
- **`uv sync --frozen` fails in CI** -- lock file out of sync with pyproject.toml
- **`docker compose up` doesn't rebuild** -- must use `--build` flag
