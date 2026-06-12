# Module 6 -- Networking Deep Dive

**Learning objectives:**
- Understand Docker's bridge network
- Use container DNS within Compose
- Diagnose container-to-container connectivity issues
- Create and use custom networks

**Prerequisites:** Modules 1-5 complete.

---

## Exercise 6.1 -- Diagnose a Broken Network (Unguided)

You are given this docker-compose.yml. It has a bug -- the services can't reach each other.

```bash
mkdir -p ~/docker-lab/ex6-1 && cd ~/docker-lab/ex6-1
```

`docker-compose.yml`:

```yaml
services:
  app:
    image: alpine:latest
    command: sh -c "while true; do wget -q -O- http://api:5000/health || echo 'api unreachable'; sleep 2; done"
    depends_on:
      - api

  api:
    image: alpine:latest
    command: sh -c "while true; do echo -e 'HTTP/1.1 200 OK\r\n\r\n{\"status\":\"ok\"}' | nc -l -p 5000; done"
    ports:
      - "5000:5000"

  db:
    image: alpine:latest
    command: sh -c "while true; do echo -e 'HTTP/1.1 200 OK\r\n\r\n{\"db\":\"connected\"}' | nc -l -p 5432; done"
    depends_on:
      - api
```

**Your task:** Find and fix the connectivity issue. The `app` service should be able to reach `api` at `http://api:5000`.

**Hints:**
- Run `docker compose up` and observe the logs
- Check if the services are on the same network
- Try `docker compose exec app ping api`
- Try `docker compose exec app cat /etc/hosts`
- Look up the `networks` key in the Compose docs if needed

---

## Exercise 6.2 -- Custom Network Isolation (Unguided)

Extend Exercise 6.1. After fixing it, split the services into two networks:

- `frontend`: app
- `backend`: api, db

The `app` should reach `api:5000` but NOT `db:5432`. The `api` should reach `db:5432`.

**Hint:** Use the `networks` key under each service and define both networks under the top-level `networks` key.

**Verify:**

```bash
docker compose exec app wget -q -O- http://api:5000/health    # should succeed
docker compose exec app wget -q -O- http://db:5432            # should fail (different network)
docker compose exec api wget -q -O- http://db:5432            # should succeed (same network)
```

---

## Exercise 6.3 -- DNS Quirks (Unguided)

Use the compose file from Exercise 6.1 (fixed version).

Start the stack. Now exec into the `app` container and try to reach the `api` service using:
- Service name: `http://api:5000`
- Container name: `http://ex6-1_api_1:5000` (or whatever the actual name is)

**Questions to answer:**
1. Does DNS resolution via service name work?
2. Does DNS resolution via container name work?
3. What happens if you scale the `api` service to 3 replicas? `docker compose up -d --scale api=3`
4. Does `app` still resolve `api` to a single IP?

**Clean up:**

```bash
docker compose down
```
