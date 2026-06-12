---
tags: [docker, containers, basics]
aliases: ["Docker Module 1"]
created: 2026-06-11
parent: "[[docker|Docker MOC]]"
exercises: "[[exercises/module-1]]"
---

## Key Concepts

**Image**: read-only template (snapshot of filesystem + metadata). Like a class in OOP.

**Container**: running instance of an image. Like an object. Has its own process tree, network stack, filesystem.

**Registry**: storage for images. Docker Hub is the default. `docker pull nginx` fetches from hub.docker.com.

## Image Layer Model

Each Dockerfile instruction creates a **layer** (read-only diff of the filesystem). Layers stack:

```
ubuntu:22.04        layer 0  (base)
apt install python  layer 1
pip install flask   layer 2
COPY app.py         layer 3
```

When you run a container, Docker adds a thin **writable container layer** on top. All writes during runtime go there. This is why stopping and restarting a container loses data by default -- the writable layer is ephemeral.

**Caching**: if a layer hasn't changed, Docker reuses it from a previous build. That's why ordering matters: put layers that change less often first.

## Containers vs VMs

| | Container | VM |
|---|---|---|
| Kernel | Shares host kernel | Own full OS kernel |
| Size | MBs | GBs |
| Boot | Milliseconds | Seconds to minutes |
| Isolation | Process-level (namespaces) | Hardware-level (hypervisor) |
| Density | 100+ per host | 5-10 per host |

## Key Commands

```bash
## Run
docker run nginx                    # foreground, Ctrl+C to stop
docker run -d nginx                 # detached (background)
docker run -d --name web nginx      # name it
docker run -d -p 8080:80 nginx      # port map host:container
docker run --rm nginx               # auto-delete when stopped

## List
docker ps                           # running only
docker ps -a                        # all (including stopped)

## Interact
docker stop web                     # SIGTERM, then SIGKILL after timeout
docker start web                    # start a stopped container
docker restart web                  # restart
docker rm web                       # remove (must be stopped)
docker rm -f web                    # force remove (while running)

## Debug
docker logs web                     # stdout/stderr
docker logs -f web                  # follow (like tail -f)
docker logs --tail 50 web           # last 50 lines
docker exec -it web bash            # open interactive shell
docker exec web cat /etc/hosts      # run one command
docker inspect web                  # JSON with full config
docker inspect web | jq '.[].NetworkSettings.IPAddress'
docker stats web                    # live CPU/memory usage
docker top web                      # running processes inside

## Port mapping
docker port web                     # show port mappings
```

## Port Mapping

`-p host_port:container_port`

```bash
docker run -d -p 8080:80 nginx      # localhost:8080 -> container:80
docker run -d -p 80:80 nginx        # localhost:80 -> container:80
docker run -d -P nginx              # auto-assign port from EXPOSE
```

Docker sets up iptables NAT rules on the host. The container gets its own network namespace with an internal IP on a virtual bridge (`docker0`). The port mapping forwards traffic from the host's network stack into the container's namespace.
