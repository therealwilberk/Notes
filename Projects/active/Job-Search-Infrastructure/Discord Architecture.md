---
tags:
  - discord
  - architecture
  - bots
  - webhooks
  - permissions
  - job-search
aliases:
  - "Discord Architecture"
  - "Bot Architecture"
parent: "[[Job Hunt Ops — Map of Content]]"
created: 2026-05-25
status: active
---

# Discord Architecture

> [!info] Part of [[Job Hunt Ops — Map of Content]]

Two-connection model: one bot for interactive operations, webhooks for automated posting.

## Connection Model

| Connection | Purpose | Protocol | Token Management |
|------------|---------|----------|-----------------|
| **Zenicious** (bot) | Interactive: read, react, respond, manage | Bot token + gateway | One token, Message Content Intent required |
| **n8n** (webhooks) | Automated: feeds, alerts, dashboard, logs | HTTP POST per channel | One webhook URL per channel |

### Why Two, Not One

- **Isolation**: n8n webhook breaks → bot still works. Bot token rotates → feeds keep flowing
- **Permissions surface**: n8n only needs write. Bot needs read + write + react + manage
- **Rate limits**: Separate rate limit buckets. 5 workflows posting simultaneously won't throttle the bot
- **Simplicity**: Webhooks are just URLs. No OAuth dance, no intents, no gateway management for n8n

### Why Webhooks for n8n, Not a Bot

- n8n has zero interest in reading Discord. It only writes.
- Webhook = HTTP POST to a URL. n8n's HTTP Request node handles this natively.
- One webhook per channel = isolated failure domain
- New workflow = create webhook, paste URL. No bot permission updates needed.

## Scaling: What Happens When Workflows Multiply

```
Workflow 1 (Job Feed)     → POST to #feed-eee webhook
Workflow 2 (Validator)    → POST to #validated webhook  
Workflow 3 (Dashboard)    → POST to #dashboard webhook
Workflow 4 (Enrichment)   → POST to #companies webhook
Workflow 5 (Cover Letter) → POST to #cover-letters webhook
...
Workflow N                → POST to #channel-N webhook
```

Each workflow targets its own webhook URL. Zero conflicts. Independent failure domains.

**Adding a new workflow:**
1. Create webhook in target channel (Discord UI → Integrations → Webhooks)
2. Copy webhook URL
3. Paste into n8n HTTP Request node
4. Done. No bot config changes.

**Adding a new channel:**
1. Create channel
2. Create webhook in it
3. Update MOC with channel purpose
4. Wire workflow

## Permissions Matrix

### Zenicious (Bot)

| Channel | Read | Send | Embed | React | Manage | Notes |
|---------|------|------|-------|-------|--------|-------|
| #dashboard | ✅ | ✅ | ✅ | ✅ | ✅ | Pin daily summaries |
| #alerts | ✅ | ✅ | ✅ | ✅ | ❌ | React to confirm seen |
| #log | ✅ | ❌ | ❌ | ❌ | ❌ | Monitor only |
| #feed-eee | ✅ | ✅ | ✅ | ✅ | ❌ | React for cover letter trigger |
| #feed-general | ✅ | ✅ | ✅ | ✅ | ❌ | |
| #validated | ✅ | ✅ | ✅ | ✅ | ✅ | Pin top matches |
| #applied | ✅ | ✅ | ✅ | ✅ | ❌ | |
| #saved | ✅ | ✅ | ✅ | ✅ | ❌ | |
| #companies | ✅ | ✅ | ✅ | ✅ | ❌ | |
| #market-intel | ✅ | ✅ | ✅ | ❌ | ❌ | |
| #cover-letters | ✅ | ✅ | ✅ | ✅ | ❌ | React ✅ to approve |
| #resume-versions | ✅ | ✅ | ✅ | ❌ | ❌ | |
| #agent-status | ✅ | ✅ | ✅ | ❌ | ❌ | |
| #agent-playground | ✅ | ✅ | ✅ | ✅ | ❌ | |
| #strategy | ✅ | ✅ | ❌ | ✅ | ❌ | |
| #random | ✅ | ✅ | ❌ | ✅ | ❌ | |

### n8n (Webhooks)

| Channel | Webhook | Workflows |
|---------|---------|-----------|
| #feed-eee | ✅ | Job Feed Scanner |
| #feed-general | ✅ | Job Feed Scanner (general) |
| #alerts | ✅ | Job Feed Scanner (high-score) |
| #dashboard | ✅ | Daily Dashboard |
| #log | ✅ | All workflows (execution log) |
| #agent-status | ✅ | Health check cron |
| #validated | ✅ | Job Validator |
| #companies | ✅ | Company Enrichment |

## Rate Limits

- Discord webhook rate limit: ~5 requests/second per webhook
- Discord bot rate limit: 50 requests/second (shared across all channels)
- n8n posting at 4h intervals = nowhere near limits
- If feed volume spikes, batch posts (group 5 jobs per embed instead of 1 per embed)

## Failure Modes

| Failure | Impact | Recovery |
|---------|--------|----------|
| Webhook URL rotated | One channel stops receiving | Regenerate webhook URL in Discord, update n8n |
| Bot token revoked | Bot can't read/react | Regenerate token, update Zenicious config |
| n8n down | No automated posts | Bot still works. Restart n8n container |
| FreeLLM down | No scoring/enrichment | Jobs still post raw. Agent alerts in #agent-status |
| Rate limited | Posts delayed | Auto-retry. If persistent, batch posts |

## See Also

- [[Discord Bot Setup]]
- [[n8n + Discord Integration]]
- [[Notion Integration]]
- [[Job Hunt Ops — Map of Content]]
