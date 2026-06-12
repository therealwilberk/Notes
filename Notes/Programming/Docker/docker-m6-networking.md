---
tags: [docker, networking, dns]
aliases: ["Docker Module 6"]
created: 2026-06-11
parent: "[[docker|Docker MOC]]"
exercises: "[[exercises/module-6]]"
---

## The Default Bridge Network

When Docker starts, it creates a virtual bridge (`docker0`). Every container gets:
- Its own network namespace
- A virtual ethernet interface (veth) plugged into the bridge
- An IP on the bridge's subnet (typically 172.17.0.0/16)

```
Container A (172.17.0.2)  <->  docker0 bridge  <->  host network  <->  outside
Container B (172.17.0.3)  <->  docker0 bridge  <->  host network  <->  outside
```

Containers on the same bridge can reach each other by IP. But IPs are assigned at startup and can change.

## Container DNS in Compose

Compose creates a dedicated network per project. Containers are reachable by **service name**, not IP:

```yaml
services:
  mlflow:
    ...
  app:
    environment:
      - MLFLOW_TRACKING_URI=http://mlflow:5000   # uses service name, not IP
```

Docker's embedded DNS resolves `mlflow` to the container's IP. This is why `app` uses `http://mlflow:5000` -- DNS-resolved within the compose network.

## Health Checks (Critical Detail)

`depends_on` with `condition: service_healthy` requires a `healthcheck` defined on the target service:

```yaml
mlflow:
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:5000"]
    interval: 30s
    timeout: 10s
    retries: 3
    start_period: 10s   # wait this long before first check
```

Without the healthcheck on `mlflow`, `condition: service_healthy` waits forever because the service never reports as healthy.

## Custom Networks

Create separate networks for different concerns:

```yaml
networks:
  backend:
  monitoring:

services:
  mlflow:
    networks: [backend]
  app:
    networks: [backend]
  monitor:
    networks: [monitoring]
```

## Port Mapping Gotchas

- **Port conflict**: `Error: driver failed programming external connectivity` -- something else is using the host port. Change the host side: `"5001:5000"`
- **Binding scope**: `"0.0.0.0:5000:5000"` externally accessible; `"127.0.0.1:5000:5000"` localhost only
- **Ephemeral range**: `docker run -P` (auto-assign) uses ports 32768-60999
