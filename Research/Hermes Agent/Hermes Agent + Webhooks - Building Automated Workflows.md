---
title: "Hermes Agent + Webhooks: How to Actually Build Automated Workflows"
source: https://youtube.com/watch?v=WNYe5mD4fY8
type: youtube-notes
date: 2026-05-22
tags: [hermes-agent, webhooks, automation, cron-jobs, github, beehiiv, ngrok, workflows]
parent: "[[MOCs/Hermes Agent MOC.md]]"
---

# Hermes Agent + Webhooks: Building Automated Workflows

## Key Concepts
- **Webhooks = event-driven triggers** — the internet itself triggers your agent without you opening a chat
- Two directions: **World → Agent** (external service triggers Hermes) and **Agent → World** (Hermes posts to external services)
- Webhooks make Hermes feel like a **backend service**, not just a chatbot
- Any service with a webhook URL field can trigger your agent (GitHub, Stripe, Beehiiv, Shopify, Helios, cal.com, etc.)
- Combines with **cron jobs** for scheduled tasks and **scripts** for data processing

## Webhook Architecture
- **HTTP POST** with JSON payload → lands on URL you own
- Event-driven (not polling) — "doorbell vs checking the door every 5 minutes"
- Hermes flow: URL routing → signature check → template rendering → fresh agent turn → deliver response to Telegram

### Inbound (World → Agent)
- External service fires event → Hermes receives and processes
- Examples: new subscriber, payment cleared, PR opened

### Outbound (Agent → World)
- Agent produces output → posts to external endpoint
- Methods: cron jobs + curl/HTTPX, or built-in hook system (`hermes/hooks` directory)
- Hook fires on lifecycle events: session started, agent step, slash command used

## Step-by-Step Setup: Webhook Receiver

### 1. Enable Webhooks in .env
Add to `.hermes/.env`:
```bash
WEBHOOK_ENABLE=true
WEBHOOK_PORT=8644
WEBHOOK_SECRET=<generated-secret>
```
Generate secret with Python:
```python
python3 -c "import secrets; print(secrets.token_hex(16))"
```

### 2. Add Route to Config
Edit `.hermes/config.yaml`:
```yaml
platforms:
  webhook:
    enable: true
    port: 8644
    routes:
      new-subscriber:
        prompt: |
          New Beehiiv subscriber!
          Email: {{email}}
          Referral: {{referral_source}}
          Tier: {{subscription_tier}}
          Timestamp: {{timestamp}}
          Raw JSON: {{raw_json}}
          Deliver to Telegram.
```

### 3. Start ngrok Tunnel
```bash
ngrok http 8644
```
This gives you a public URL like `https://abc123.ngrok.io` pointing to your local server.

### 4. Register Webhook in External Service
- In the service's webhook settings, set:
  - **Payload URL**: `https://<ngrok-url>/webhook/<route-name>` (e.g., `/webhook/new-subscriber`)
  - **Content type**: `application/json`
  - **Secret**: same secret from .env
  - **Events**: select which events trigger

### 5. Start the Gateway
```bash
hermes gateway
```
Must be running to receive webhooks.

## Demo 1: Beehiiv Newsletter Subscribers

### Real-time Subscriber Alerts
- Route: `new-subscriber` in config.yaml
- Delivers email, referral source, tier, timestamp to Telegram on each new subscriber

### Hourly Stats Cron Job
1. Add Beehiiv API credentials to `.hermes/.env`:
   ```bash
   BEEHIIV_API_KEY=<key>
   BEEHIIV_PUBLICATION_ID=<id>
   ```
2. Create a Python script (`beehiiv_stats.py`) to pull stats via API
3. Create cron job that runs script hourly with prompt:
   - "Summarize last hour of Beehiiv activity. Lead with new subscriber count, note dominant UTM sources, flag any invalid emails."
4. Agent can cross-reference with YouTube API, X API to find when subscriber activity peaks

## Demo 2: GitHub Auto PR Review

### Setup
1. Add GitHub route to `config.yaml`:
   ```yaml
   routes:
     github-pr:
       prompt: |
         Review the pull request.
         Repository: {{repository}}
         PR number: {{pr_number}}
         Author: {{author}}
         URL: {{url}}
         Action: {{action}}
         Fetch the diff, assess correctness, suggest improvements, flag risks.
   ```
2. Generate and add webhook secret (same Python script)
3. Install **GitHub CLI** in WSL (not just Windows):
   ```bash
   sudo apt install gh
   gh auth login
   ```
4. Restart gateway after config changes
5. Keep ngrok tunnel running

### Register in GitHub
- GitHub repo → Settings → Webhooks → Add webhook
- Payload URL: `https://<ngrok-url>/webhook/github-pr`
- Content type: `application/json`
- Secret: same as config
- Events: select **Pull requests** only

### Testing
```bash
git checkout -b webhook-test
echo "test" >> README.md
git add . && git commit -m "test webhook trigger"
git push origin webhook-test
# Create PR on GitHub
```
- Agent automatically reads PR, fetches diff, writes review comment (~1 minute)
- Comments include: summary, correctness assessment, suggested improvements, risks, recommendation (approve/request changes)
- **Human should verify agent's suggestions before merging**

### Gotchas
- Gateway must be running when PR is created (first ping fails silently if not)
- Use GitHub's "Redeliver" button to retry failed webhook deliveries
- **ngrok URLs rotate on free tier restart** — must update webhook URL in GitHub if you restart ngrok

## Demo 3: Agent Enriching an App (Outbound)

### Architecture
- Agent runs cron job → processes RSS news data → posts analysis to app's API endpoint
- **No ngrok needed** for outbound — agent makes HTTP calls directly

### Setup
1. Create receiving endpoint in your app (Next.js example):
   ```typescript
   // /app/api/agent-updates/route.ts
   // Receives POST from Hermes agent
   ```
2. Add to `.hermes/.env`:
   ```bash
   AGENT_WEBHOOK_URL=https://your-app.com/api/agent-updates
   WEBHOOK_SECRET=<same-secret>
   ```
3. Add same secret as env variable in deployment (e.g., Vercel)
4. Create Python script to pull data (e.g., `poll_mentions_rss.py` for RSS feeds)
5. Create cron job:
   - Script: runs the data-pulling script
   - Prompt: instructs agent to analyze data, produce structured JSON, POST to webhook URL with secret header
   - Example prompt: "Identify top 10 keywords. Return valid JSON matching exact shape. Use terminal tool to POST to webhook URL with X-Webhook-Secret header."

### Cron Job Command
```bash
hermes cron run <task-number>
```

## Hooks System (Alternative Outbound)
- Drop files in `hermes/hooks/` directory
- Fires on lifecycle events: `session_started`, `agent_step`, `slash_command`
- Can also hook into plugins

## Tips & Gotchas
- **ngrok URLs rotate on free tier restart** — biggest pain point; update webhook URLs when restarting
- Gateway must be running BEFORE the webhook fires — check with redeliver if first attempt fails
- GitHub CLI must be installed **inside WSL**, not just on Windows host
- Secrets must match between `.hermes/.env`, `config.yaml`, and external service
- For outbound (Agent → World), you don't need ngrok — agent makes HTTP calls directly
- Combine webhooks + cron jobs + agent skills for maximum analytical power
- Always verify agent's output before acting on it (e.g., PR reviews)

## Use Case Ideas
- **GitHub**: Auto PR review, issue triage, error alerting
- **Stripe**: Payment notifications, fraud flagging, welcome messages
- **Beehiiv/Newsletter**: Subscriber alerts, hourly stats digests
- **Helios (Solana)**: On-chain wallet activity alerts → Telegram
- **cal.com**: Automatic pre-meeting briefings when meeting booked
- **Sentry**: Error triage and on-call paging
- **Shopify**: Order notifications, inventory alerts
- **Typeform/Home Assistant**: Form submissions, smart home events

## Timestamps & Chapters
- 0:00 - Intro: What can you actually do with AI agents?
- 1:19 - Webhooks explained (doorbell analogy)
- 3:09 - Two directions: World→Agent and Agent→World
- 6:08 - Demo 1: Beehiiv subscriber webhook + hourly cron
- 12:36 - Demo 2: GitHub PR auto-review
- 18:28 - Demo 3: Agent enriching an app with data analysis
- 24:44 - Running the outbound cron job

## Summary
Webhooks turn Hermes from a chatbot into a backend automation service. The setup involves enabling webhooks in `.env`, defining routes in `config.yaml`, using ngrok for a public URL, and registering the webhook in external services. Three demos covered: real-time newsletter subscriber alerts (Beehiiv), automatic GitHub PR reviews, and outbound agent-to-app data enrichment via cron jobs. Key gotcha: ngrok free tier URLs rotate on restart.
