---
tags:
  - discord
  - bot
  - job-search
  - automation
  - webhooks
aliases:
  - "Discord Setup"
  - "Discord Bot"
parent: "[[Job Hunt Ops — Map of Content]]"
created: 2026-05-25
status: setup
---

# Discord Bot Setup

> [!info] Part of [[Job Hunt Ops — Map of Content]]

Discord is the operations hub. All job feeds, alerts, and agent output surface here.

## Channel Layout

```
📋 COMMAND CENTER
├── #dashboard          — Daily automated summary (8am EAT cron)
├── #alerts             — Instant high-score matches (score > 90)
├── #log                — n8n execution logs, errors, health

🎯 JOBS
├── #feed-eee           — Raw EEE job feed (auto-posted, unfiltered)
├── #feed-general       — Adjacent roles (energy, power, automation)
├── #validated          — Agent-scored + vetted (score > 70)
├── #applied            — Application tracking
├── #saved              — Bookmarks

🔬 RESEARCH
├── #companies          — Enriched company profiles
├── #market-intel       — Salary data, hiring trends

📝 MATERIALS
├── #cover-letters      — Agent-drafted CLs, human review
├── #resume-versions    — Tailored resume variants

🤖 AGENTS
├── #agent-status       — FreeLLM health, model availability
├── #agent-playground   — Workflow testing

💬 GENERAL
├── #strategy           — Career direction
├── #random             — Off-topic
```

## Bot Creation Checklist

### 1. Create Application
1. https://discord.com/developers/applications
2. "New Application" → name it (e.g., "JobBot")
3. "Bot" tab → "Add Bot"

### 2. Enable Intents
Under "Bot" tab:
- [x] **Message Content Intent** (CRITICAL — n8n needs to read messages)
- [ ] Server Members Intent (optional)

### 3. Generate Invite URL
OAuth2 → URL Generator:
- Scopes: `bot`, `applications.commands`
- Permissions: Send Messages, Embed Links, Attach Files, Read Message History, Add Reactions, Use Slash Commands, Manage Messages

### 4. Invite to Server
Copy generated URL → open in browser → select server → Authorize

### 5. Get Credentials
- **Bot Token**: Bot tab → "Reset Token" → copy
- **Server ID**: Right-click server → Copy Server ID (Developer Mode on)
- **Channel IDs**: Right-click each channel → Copy Channel ID

## Channel ID Template

Fill after creating channels:

```
#alerts:        
#feed-eee:      
#feed-general:  
#validated:     
#applied:       
#companies:     
#dashboard:     
#log:           
#agent-status:  
```

## n8n Integration

### Option A: Discord Node (simple)
n8n has a native Discord node. Limited formatting but quick setup.

### Option B: Webhook (recommended)
Richer embeds with fields, colors, links.

1. Discord Server → Settings → Integrations → Webhooks → New Webhook
2. Copy webhook URL
3. n8n: HTTP Request node → POST to webhook URL

### Embed Template

```json
{
  "embeds": [{
    "title": "{{$json.title}}",
    "url": "{{$json.url}}",
    "color": 3066993,
    "fields": [
      {"name": "Company", "value": "{{$json.company}}", "inline": true},
      {"name": "Location", "value": "{{$json.location}}", "inline": true},
      {"name": "Score", "value": "{{$json.score}}/100", "inline": true},
      {"name": "Source", "value": "{{$json.source}}", "inline": true}
    ],
    "footer": {"text": "via n8n • {{$json.scraped_at}}"}
  }]
}
```

### Color Codes

| Color | Hex | When |
|-------|-----|------|
| Green | `3066993` | High relevance (80-100) |
| Blue | `3447003` | Medium (50-79) |
| Yellow | `16776960` | Low (below 50) |
| Red | `15158332` | Error/warning |

## Scoring Rubric

| Factor | Weight | Criteria |
|--------|--------|----------|
| EEE Relevance | 30% | Direct EEE = 100, adjacent = 70, general eng = 40 |
| Entry Level | 25% | Graduate/junior = 100, 0-2 yrs = 80, 2-5 yrs = 40 |
| Location | 20% | Nairobi = 100, Kenya = 70, Remote = 90 |
| Company Quality | 15% | Known = 100, has website = 70, no web = 20 |
| Recency | 10% | < 3 days = 100, < 7 = 70, < 14 = 40 |

**Thresholds:**
- Score > 90: 🔥 alert in #alerts
- Score > 70: post to #validated
- Score < 70: stays in #feed-eee only
- Score < 40: log only, don't post

## Scaling

- **New job vertical**: add `#feed-{type}` under JOBS
- **New data source**: tag existing feed or new channel if > 20/day
- **New workflow**: add channel under AGENTS

## See Also

- [[n8n + Discord Integration]]
- [[n8n Setup & Configuration]]
- [[Notion Integration]]
- [[Job Hunt Ops — Map of Content]]
