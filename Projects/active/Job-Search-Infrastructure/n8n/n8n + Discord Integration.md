---
tags:
  - n8n
  - discord
  - webhooks
  - notifications
aliases:
  - "Discord Output"
  - "n8n Discord"
parent: "[[Job Hunt Ops — Map of Content]]"
created: 2026-05-21
updated: 2026-05-25
status: active
---

# n8n + Discord Integration

> [!info] Part of [[Job Search Infrastructure — Map of Content]]

Two approaches for pushing job alerts to Discord from [[n8n Setup & Configuration]].

## Option 1: Built-in Discord Node

Simplest. n8n has a native Discord node.

```
[Job Data] → Discord Node (channel, message)
```

- Limited formatting (plain text + basic markdown)
- Good for quick setup

## Option 2: HTTP Request + Webhook (Recommended)

Richer embeds with fields, colors, and links. More control.

### Setup

1. **Discord Server** → Settings → Integrations → Webhooks → New Webhook
2. Copy the webhook URL: `https://discord.com/api/webhooks/{id}/{token}`
3. In n8n: HTTP Request node → POST to webhook URL

### Webhook Payload

```json
{
  "embeds": [{
    "title": "{{ $json.title }}",
    "url": "{{ $json.url }}",
    "color": 5814783,
    "fields": [
      {
        "name": "Company",
        "value": "{{ $json.company }}",
        "inline": true
      },
      {
        "name": "Location",
        "value": "{{ $json.location }}",
        "inline": true
      },
      {
        "name": "Source",
        "value": "{{ $json.source }}",
        "inline": true
      },
      {
        "name": "Relevance",
        "value": "{{ $json.score }}/10",
        "inline": true
      }
    ],
    "footer": {
      "text": "via n8n • {{ $json.scraped_at }}"
    }
  }]
}
```

### Color Codes

| Color | Hex | Meaning |
|-------|-----|---------|
| Green | `3066993` | High relevance (8-10) |
| Blue | `3447003` | Medium relevance (5-7) |
| Yellow | `16776960` | Low relevance (1-4) |
| Red | `15158332` | Error/warning |

## n8n Workflow: Full Pipeline

```
Schedule Trigger (every 2 hours)
  ↓
Split: [Careerjet API] + [CareerPoint RSS] + [JobWeb RSS]
  ↓
Merge (combine all new jobs)
  ↓
Code Node: Deduplicate by URL
  ↓
Code Node: Score relevance (keywords match)
  ↓
IF Node: score >= 5
  ├── YES → HTTP Request (Discord webhook) + HTTP Request (JustHireMe API)
  └── NO → Discard
```

## Discord Channel Setup

```
Server: Job Search
├── #job-alerts          ← Filtered, relevant jobs only
├── #all-listings        ← Everything (optional, for browsing)
└── #n8n-logs            ← Workflow status, errors
```

## JustHireMe Integration

When jobs hit the Discord feed, they can also POST to JustHireMe:

```javascript
// Code node after scoring
const scored_jobs = $input.all()
  .filter(item => item.json.score >= 5)
  .map(item => ({
    title: item.json.title,
    company: item.json.company,
    location: item.json.location,
    url: item.json.url,
    description: item.json.description,
    source: item.json.source,
    score: item.json.score,
    scraped_at: item.json.scraped_at
}));

// Send to JustHireMe
await fetch('http://localhost:8000/api/jobs/ingest', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ jobs: scored_jobs })
});

return scored_jobs;
```

## See Also

- [[n8n Setup & Configuration]]
- [[Kenyan Job Sites — Feeds & Scraping]]
- [[Job Search Infrastructure — Map of Content]]

## Sources

- n8n Discord node docs: https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.discord/
- Discord webhook docs: https://discord.com/developers/docs/resources/webhook
