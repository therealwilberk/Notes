# Job Hunt Ops — Architecture

> Discord-first job hunting command center. n8n automates, agents process, Discord surfaces everything.

## Stack

| Layer | Tool | Role |
|-------|------|------|
| Hub | Discord | Visibility, coordination, alerts, human-in-the-loop |
| Automation | n8n | Workflows, scheduling, webhooks, orchestration |
| Intelligence | FreeLLM (127.0.0.1:3001) | Per-task model selection for processing |
| Storage | Postgres (n8n internal) + flat files | Workflow state, enrichment data |

## Model Assignment (FreeLLM)

| Task | Model | Why |
|------|-------|-----|
| Job feed scanning | `openai/gpt-oss-20b:free` | Fast, cheap, good at structured extraction |
| Job validation/scoring | `google/gemma-4-31b-it:free` | Reasoning quality for filtering relevance |
| Cover letter drafts | `mistralai/mistral-large-3-675b-instruct-2512` | Best writing quality available |
| Company enrichment | `openai/gpt-oss-120b:free` | Deep research, multi-source synthesis |
| Code/scraper logic | `deepseek-ai/deepseek-v4-pro` | Code generation for scrapers |
| Vision (job screenshots) | vision→mimo-v2-omni | Existing AUX vision model |
| Compression/summarization | gemini-2.5-flash | Existing AUX compression model |

---

## Discord Server Layout

### Server Name
`Job Hunt HQ` (or whatever you vibe with)

### Channel Structure

```
📋 COMMAND CENTER
├── #dashboard          — Daily automated summary (n8n cron: 8am EAT)
├── #alerts             — Instant job matches (high-score triggers)
├── #log                — Raw n8n execution logs, errors, health checks

🎯 JOBS
├── #feed-eee           — Raw EEE job feed (auto-posted, unfiltered)
├── #feed-general       — Backup/adjacent roles (energy, power, automation)
├── #validated          — Vetted + scored jobs (agent-processed)
├── #applied            — Tracking: what was applied, when, status
├── #saved              — Bookmarks / "come back to this"

🔬 RESEARCH
├── #companies          — Enriched company profiles (from pipeline)
├── #market-intel       — Salary data, hiring trends, industry news

📝 MATERIALS
├── #cover-letters      — Draft CLs from agents, human review before send
├── #resume-versions    — Tailored resume variants per job type

🤖 AGENTS
├── #agent-status       — Agent health, FreeLLM uptime, model availability
├── #agent-playground   — Testing new workflows, prompt tuning

💬 GENERAL
├── #strategy           — Career direction, networking plays, discussions
├── #random             — Off-topic
```

### Why this layout
- **Separation of signal vs noise.** Raw feeds don't clutter validated results.
- **Human-in-the-loop at the right spots.** Cover letters and applications need your eyes. Feed scanning doesn't.
- **Scales by adding channels, not restructuring.** New job type? New feed channel. New workflow? New agent channel.

### Scaling Rules
- **New job vertical** (e.g., software roles): add `#feed-software` under JOBS
- **New data source** (e.g., scraper for specific site): add source tag to existing feed channel, or new channel if volume > 20/day
- **New agent/task type**: add channel under AGENTS
- **Team expansion** (unlikely but): role-based permissions per category

### Roles
- **You (Admin)**: full access
- **Zenicious (Bot)**: read/write to all channels, no admin
- **n8n (Webhook)**: write to feeds, alerts, log, dashboard

---

## n8n Workflows

### 1. Job Feed Scanner (Priority: NOW)
```
Trigger: Cron (every 4h)
Sources:
  - LinkedIn EEE jobs Kenya (RSS/scrape)
  - Indeed Kenya
  - BrighterMonday
  - MyJobMag
  - Glassdoor KE
Process:
  1. Fetch listings from sources
  2. Filter: EEE/Power/Energy/Automation + Entry level
  3. Deduplicate against seen jobs (Postgres)
  4. Score relevance (agent: gpt-oss-20b)
  5. Post to #feed-eee (all) and #alerts (score > 80)
Output: Discord embed per job (title, company, location, link, score)
```

### 2. Job Validator (Priority: NOW)
```
Trigger: New message in #feed-eee
Process:
  1. Extract job details from post
  2. Agent validates: real listing? company legit? actually entry-level?
  3. Score 0-100
  4. If score > 70: cross-post to #validated
  5. If score > 90: also post to #alerts with 🔥
```

### 3. Company Enrichment (Priority: NEXT)
```
Trigger: New company in #validated (not seen before)
Process:
  1. Search company (web_search)
  2. Extract: website, LinkedIn, size, sector, recent news
  3. Check if hiring (careers page)
  4. Post profile to #companies
  5. Store in enrichment DB
```

### 4. Daily Dashboard (Priority: NOW)
```
Trigger: Cron (8:00 AM EAT daily)
Process:
  1. Count: new jobs today, validated, applied
  2. Top 3 matches by score
  3. Upcoming deadlines
  4. Agent health summary
Output: Formatted embed in #dashboard
```

### 5. Cover Letter Generator (Priority: LATER)
```
Trigger: React emoji on #validated job (e.g., ✍️)
Process:
  1. Pull job details + company profile + resume
  2. Agent drafts cover letter (mistral-large)
  3. Post draft to #cover-letters
  4. React ✅ to approve → save to materials
```

### 6. JustHireMe Integration (Priority: LATER)
```
Trigger: Manual or cron
Process:
  1. Pull from JustHireMe API
  2. Cross-reference with enriched companies
  3. Surface matches
```

---

## Integration Map

```
┌─────────────┐     webhook      ┌──────────┐
│  Job Sources │ ───────────────→ │   n8n    │
│  (scrapers)  │                  │ workflows│
└─────────────┘                  └────┬─────┘
                                      │
                           ┌──────────┼──────────┐
                           │          │          │
                      ┌────▼───┐ ┌────▼───┐ ┌───▼────┐
                      │FreeLLM │ │Postgres│ │Discord │
                      │ agents │ │  (DB)  │ │  (hub) │
                      └────────┘ └────────┘ └────────┘
                                            │
                                    ┌───────┼───────┐
                                    │       │       │
                                #feed  #alerts  #dashboard
```

---

## Immediate Next Steps

### You (Wilber)
1. [ ] Create Discord server with the channel layout above
2. [ ] Create a Discord bot at discord.com/developers
   - Permissions: Send Messages, Embed Links, Read Message History, Add Reactions
   - Invite bot to server
3. [ ] Share: Bot token + Server ID + Channel IDs
4. [ ] Decide: server name, any channel renames

### Me (Zenicious)
1. [ ] Configure n8n Discord credentials (once you give me the token)
2. [ ] Build Workflow 1: Job Feed Scanner (first draft)
3. [ ] Build Workflow 4: Daily Dashboard
4. [ ] Set up FreeLLM connection from n8n (HTTP Request node → 127.0.0.1:3001)
5. [ ] Test end-to-end: cron → scrape → score → Discord post

---

## Open Questions
- BrighterMonday/MyJobMag: do they have APIs, or are we scraping? (affects n8n node type)
- LinkedIn: RSS possible, or do we need auth? (LinkedIn is aggressive about scraping)
- Resume: where's the current version stored? (needed for cover letter gen)
- JustHireMe: what's the API shape? (for later integration)
