---
tags:
  - n8n
  - self-hosting
  - arch-linux
  - docker
  - automation
aliases:
  - "n8n Setup"
  - "n8n Arch"
parent: "[[Job Search Infrastructure — Map of Content]]"
created: 2026-05-21
status: researched
---

# n8n Setup & Configuration

> [!info] Part of [[Job Search Infrastructure — Map of Content]]

## Installation: Docker (Recommended)

Docker over bare metal — avoids Node.js conflicts, easier updates, same experience across distros.

### Quick Start

```bash
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  -e GENERIC_TIMEZONE="Africa/Nairobi" \
  -e TZ="Africa/Nairobi" \
  --restart unless-stopped \
  docker.n8n.io/n8nio/n8n
```

### Docker Compose (Production)

```yaml
version: "3.8"

services:
  n8n:
    image: docker.n8n.io/n8nio/n8n
    container_name: n8n
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - GENERIC_TIMEZONE=Africa/Nairobi
      - TZ=Africa/Nairobi
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=<strong-password>
      - N8N_ENCRYPTION_KEY=<random-secret-key>
      - EXECUTIONS_MODE=regular
      - EXECUTIONS_DATA_PRUNE=true
      - EXECUTIONS_DATA_MAX_AGE=168
    volumes:
      - n8n_data:/home/node/.n8n
      - /etc/localtime:/etc/localtime:ro

volumes:
  n8n_data:
    driver: local
```

### With PostgreSQL (Heavy Workloads)

```yaml
version: "3.8"

services:
  n8n:
    image: docker.n8n.io/n8nio/n8n
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=n8n
      - DB_POSTGRESDB_USER=n8n
      - DB_POSTGRESDB_PASSWORD=n8n_password
      - GENERIC_TIMEZONE=Africa/Nairobi
      - TZ=Africa/Nairobi
    volumes:
      - n8n_data:/home/node/.n8n
    depends_on:
      - postgres

  postgres:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      - POSTGRES_DB=n8n
      - POSTGRES_USER=n8n
      - POSTGRES_PASSWORD=n8n_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  n8n_data:
  postgres_data:
```

## AUR Alternative (Bare Metal)

```bash
yay -S n8n
# or
paru -S n8n
```

> [!warning] AUR packages can lag behind releases. Docker is more reliable.

## Built-in Triggers

| Trigger | Use Case |
|---------|----------|
| **Schedule Trigger** | Cron/interval — run scraping every hour |
| **RSS Feed Trigger** | Auto-detect new items, built-in dedup |
| **Webhook Trigger** | Inbound HTTP — receive from JustHireMe |
| **Manual Trigger** | Ad-hoc testing |

## Workflow: Job Scraping

### Approach 1: RSS Feed (Preferred)

```
RSS Feed Trigger → Code Node (format) → Discord Webhook
```

If target sites expose RSS, this is dead simple. n8n handles deduplication automatically.

### Approach 2: HTML Scraping

```
Schedule Trigger (hourly)
  → HTTP Request (GET job listing page)
  → HTML Extract (CSS selectors)
  → Code Node (parse, dedup, format)
  → IF Node (filter by keywords)
  → HTTP Request (Discord webhook POST)
```

## CSS Selector Patterns

```javascript
// Example: Extract job cards from a listing page
// In HTML Extract node:
{
  "job_title": ".job-card h2 a",
  "company": ".job-card .company-name",
  "location": ".job-card .location",
  "link": ".job-card h2 a[href]",
  "date": ".job-card .posted-date"
}
```

## Integration with JustHireMe

```javascript
// Code node: Format jobs and send to JustHireMe API
const jobs = $input.all().map(item => ({
  title: item.json.job_title,
  company: item.json.company,
  location: item.json.location,
  url: item.json.link,
  source: "n8n",
  scraped_at: new Date().toISOString()
}));

// POST to JustHireMe webhook
await fetch('http://localhost:8000/api/jobs/ingest', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ jobs })
});

return $input.all();
```

## Key Decisions

- **Docker over AUR** — stability, updates, isolation
- **SQLite to start** — PostgreSQL only if volume grows
- **RSS first, scraping second** — less fragile
- **Hourly schedule** — not too aggressive for free tier sites

## See Also

- [[Kenyan Job Sites — Feeds & Scraping]]
- [[n8n + Discord Integration]]
- [[Job Search Infrastructure — Map of Content]]

## Sources

- n8n official docs: https://docs.n8n.io/
- n8n Docker guide: https://docs.n8n.io/hosting/installation/docker/
- Community scraping examples from n8n forums
