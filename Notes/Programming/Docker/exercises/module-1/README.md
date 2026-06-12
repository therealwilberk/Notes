# Module 1 -- Containers: What & Why

**Learning objectives:**
- Run your first container
- Understand image vs container
- Map ports between host and container
- List, stop, remove containers
- Exec into a running container
- View logs and inspect configuration

**Prerequisites:** Docker installed, `docker --version` works

---

## Exercise 1.1 -- Hello, Container

Run Docker's hello-world image:

```bash
docker run hello-world
```

**Expected output:** A welcome message explaining that your Docker installation is working correctly. The container prints the message and exits.

When a container exits, it stops. It still exists on disk until you remove it. Check:

```bash
docker ps -a
```

Look for the `hello-world` container with status `Exited (0)`.

---

## Exercise 1.2 -- Run Nginx and Visit It

Run an nginx web server:

```bash
docker run -d -p 8080:80 --name my-nginx nginx
```

**What each flag does:**
- `-d` -- detached (run in background)
- `-p 8080:80` -- map host port 8080 to container port 80
- `--name my-nginx` -- name the container so you don't need the ID

Verify it's running:

```bash
docker ps
```

Open http://localhost:8080 in your browser, or use curl:

```bash
curl localhost:8080
```

**Expected output:** HTML from nginx's welcome page.

Now inspect the container:

```bash
docker inspect my-nginx | grep IPAddress
```

You should see the container's internal IP on the Docker bridge network (something like `172.17.0.2`).

---

## Exercise 1.3 -- Logs, Exec, and Cleanup

View nginx logs:

```bash
docker logs my-nginx          # show all logs
docker logs -f my-nginx       # follow mode (Ctrl+C to exit)
```

Generate some traffic (in another terminal or after stopping logs):

```bash
curl localhost:8080
curl localhost:8080/does-not-exist
```

Now check logs again -- you should see the HTTP request lines.

Exec into the running container:

```bash
docker exec -it my-nginx bash
```

Inside the container, look around:

```bash
ls /usr/share/nginx/html/
cat /etc/hosts
exit
```

Now stop and remove the container:

```bash
docker stop my-nginx
docker rm my-nginx
```

Verify it's gone:

```bash
docker ps -a | grep my-nginx
```

---

## Exercise 1.4 -- Port Conflict

Run two nginx containers with the same host port:

```bash
docker run -d -p 8080:80 --name nginx-a nginx
docker run -d -p 8080:80 --name nginx-b nginx    # this will fail
```

**Expected output:** An error like:
```
docker: Error response from daemon: driver failed programming external connectivity...
```

This happens because port 8080 on the host is already taken by `nginx-a`. Fix: use a different host port.

First remove the failed container:

```bash
docker rm nginx-b   # or docker rm -f nginx-b if it's still hanging
```

Now run the second container on a different port:

```bash
docker run -d -p 8081:80 --name nginx-b nginx
```

Verify both are reachable:

```bash
curl localhost:8080   # nginx-a
curl localhost:8081   # nginx-b
```

**Clean up both:**

```bash
docker stop nginx-a nginx-b && docker rm nginx-a nginx-b
```

---

## Exercise 1.5 -- Stats and Top

Run a container with some load activity:

```bash
docker run -d --name stress-test alpine sh -c "while true; do echo 'working'; done"
```

Watch its resource usage:

```bash
docker stats stress-test
```

Press Ctrl+C to exit stats. Now see its processes:

```bash
docker top stress-test
```

**Clean up:**

```bash
docker stop stress-test && docker rm stress-test
```

---

## Recap

Commands learned: `docker run`, `docker ps`, `docker ps -a`, `docker logs`, `docker exec`, `docker inspect`, `docker stop`, `docker rm`, `docker stats`, `docker top`, `curl`

Concept: image (blueprint) vs container (running instance), port mapping (host:container), container lifecycle (created -> running -> stopped -> removed), bridge network with internal IPs.
