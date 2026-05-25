---
tags:
  - n8n
  - workflow
  - job-search
  - automation
  - rss
  - scoring
aliases:
  - "Job Feed Scanner"
  - "WF1"
parent: "[[Job Hunt Ops — Map of Content]]"
created: 2026-05-25
status: building
---

# Workflow 1: Job Feed Scanner

> [!info] Part of [[Job Hunt Ops — Map of Content]]

n8n workflow. Cron-triggered every 4h. Scrapes EEE job sources, scores with FreeLLM, writes to Notion, posts to Discord.

## Architecture

```
Cron (4h)
  ↓
[Parallel Fetch: RSS × 4 (OpenedCareer + CareerPoint + JobWeb + Blog Nevine) + Careerjet API + MyJobMag Scrape]
  ↓
Merge + Normalize
  ↓
EEE Keyword Filter
  ↓
Deduplicate against Notion (last 48h)
  ↓
Score with FreeLLM (batched, 5 per call)
  ↓
[Parallel: Write to Notion + Post to Discord]
  ↓
Execution Log → #log
```

## Prerequisites

### Docker Compose Fix (FreeLLM access from container)

n8n runs in Docker. `127.0.0.1` inside the container is the container itself, not the host. FreeLLM runs on the host.

Add to `docker-compose.yml` under the n8n service:

```yaml
n8n:
  extra_hosts:
    - "host.docker.internal:host-gateway"
```

All FreeLLM calls from n8n use `http://host.docker.internal:3001/v1` instead of `http://127.0.0.1:3001/v1`.

### n8n Credentials

| Credential | Type | Value |
|------------|------|-------|
| Notion API | Header Auth | `Authorization: Bearer {NOTION_API_TOKEN}` |
| Discord Webhooks | Stored in workflow variables | One URL per channel |

### Environment Variables (n8n)

```
NOTION_API_TOKEN=<from ~/.zshrc.local>
NOTION_JOBS_DB_ID=<database_id>
NOTION_JOBS_DS_ID=<data_source_id>
DISCORD_WEBHOOK_FEED=<#feed-eee webhook URL>
DISCORD_WEBHOOK_ALERTS=<#alerts webhook URL>
DISCORD_WEBHOOK_LOG=<#log webhook URL>
FREELLM_URL=http://host.docker.internal:3001/v1
```

---

## Node-by-Node Specification

### 1. Schedule Trigger

```
Node: Schedule Trigger
Type: n8n-nodes-base.scheduleTrigger
Config:
  rule:
    interval:
      - field: hours
        hoursInterval: 4
```

### 2. Parallel Fetch (5 branches)

#### Branch A: OpenedCareer RSS

```
Node: HTTP Request (not RSS Trigger — see rationale below)
Type: n8n-nodes-base.httpRequest
Config:
  method: GET
  url: https://openedcareer.com/feed/
  options:
    response:
      responseFormat: xml

Why HTTP instead of RSS Trigger:
  RSS Trigger uses built-in guid dedup. If an RSS item is seen once but
  fails to write to Notion, the trigger skips it forever on next cycle.
  Using HTTP + dedup against Notion ensures no jobs are lost.

Node: Code — Parse RSS XML
Type: n8n-nodes-base.code
Input: HTTP response XML
Logic:
  const items = []; // parse RSS XML to array
  // Use xml2js or regex to extract <item> elements
  FOR EACH <item>:
    items.push({
      title: clean(item.title),           // strip HTML entities, trim, max 97 chars
      company: extractCompany(item),       // from dc:creator or description
      location: normalizeLocation(item),   // see location normalization
      url: item.link,
      source: "openedcareer",
      scraped_at: now().toISOString(),
      description_raw: item.contentSnippet?.substring(0, 200) || "",
      type: "full-time",
      salary: extractSalary(item) || "Not listed"
    })
```

#### Branch B: CareerPoint RSS

```
Node: HTTP Request
  url: https://www.careerpointkenya.co.ke/feed/

Node: Code — Parse RSS (same logic, source: "careerpoint")
```

#### Branch C: JobWeb RSS

```
Node: HTTP Request
  url: https://jobwebkenya.com/feed/

Node: Code — Parse RSS (same logic, source: "jobweb")
```

#### Branch D: Careerjet API

```
Node: HTTP Request
  method: GET
  url: https://search.api.careerjet.net/v4/query
  qs:
    locale_code: en_KE
    keywords: "electrical OR electronics OR power OR energy OR automation OR graduate engineer"
    location: "Kenya"
    page: 1
    pagesize: 30
    sort: date

Node: IF — has results
  condition: {{ $json.jobs.length > 0 }}
  false: → merge point (skip, log warning)

Node: Code — Normalize Careerjet
  source: "careerjet"
  title: job.title
  company: job.company
  location: normalizeLocation(job.locations)
  url: job.url
  description_raw: stripHtml(job.description).substring(0, 200)
  salary: job.salary || "Not listed"
```

#### Branch E: MyJobMag HTTP Scrape

```
Node: HTTP Request
  method: GET
  url: https://www.myjobmag.co.ke/jobs-location/nairobi/1

Node: HTML Extract
  selectors:
    job_title: ".job-list h2 a"
    company: ".job-list .company-name"
    location: ".job-list .location"
    link: ".job-list h2 a[href]"
    date: ".job-list .date-posted"

Node: IF — extract succeeded
  condition: {{ $json.job_title?.length > 0 }}
  false: → merge point

Node: Code — Normalize MyJobMag
  source: "myjobmag"
  prepend base URL to relative links
```

### 3. Merge

```
Node: Merge
Type: n8n-nodes-base.merge
Mode: Append
Input: all 5 branches
Output: combined_items[]
```

### 4. EEE Keyword Filter

```
Node: Code
Type: n8n-nodes-base.code
Input: combined_items[]
Logic:
  const KEYWORDS_EEE = [
    "electrical", "electronics", "power", "energy", "solar",
    "automation", "controls", "instrumentation", "scada", "plc",
    "transmission", "distribution", "renewable", "grid", "substation",
    "transformer", "circuit", "protection", "relay", "metering",
    "eee", "telecom", "signal", "embedded", "power systems",
    "high voltage", "low voltage", "switchgear", "generator",
    "motor", "inverter", "rectifier", "capacitor"
  ]

  const KEYWORDS_ENTRY = [
    "graduate", "junior", "entry", "intern", "trainee",
    "0-2 years", "1-2 years", "fresh", "new grad", "nysc"
  ]

  return items.filter(item => {
    const text = `${item.title} ${item.description_raw}`.toLowerCase()

    const eeeMatch = KEYWORDS_EEE.some(k => text.includes(k))
    if (!eeeMatch) return false

    // Tag entry-level matches
    item.tags = []
    if (KEYWORDS_ENTRY.some(k => text.includes(k))) {
      item.tags.push("entry-level")
    }

    return true
  })
```

### 5. Deduplicate Against Notion

```
Node: HTTP Request — Query recent jobs
Type: n8n-nodes-base.httpRequest
Config:
  method: POST
  url: https://api.notion.com/v1/databases/{{ $env.NOTION_JOBS_DB_ID }}/query
  headers:
    Authorization: Bearer {{ $env.NOTION_API_TOKEN }}
    Notion-Version: 2022-06-28
    Content-Type: application/json
  body:
    filter:
      and:
        - property: "Scraped At"
          date:
            on_or_after: "{{ $now.minus({ hours: 48 }).toISO() }}"
    page_size: 100

  // Filter by last 48h instead of all-time. Prevents the 100-item ceiling
  // from causing duplicate leaks after ~2 weeks.

Node: IF — has_more
  condition: {{ $json.has_more }}
  true:
    Node: HTTP Request — Page 2
      body: { start_cursor: "{{ $json.next_cursor }}" }
    // Loop if needed (unlikely with 48h filter)

Node: Code — Deduplicate
  const existingUrls = new Set()
  FOR EACH page in results:
    const url = page.properties?.URL?.url
    if (url) existingUrls.add(url)

  const newItems = items.filter(item => !existingUrls.has(item.url))

  IF newItems.length === 0:
    return [] // empty → workflow ends cleanly

  return newItems
```

### 6. Score with FreeLLM

```
Node: Split In Batches
Type: n8n-nodes-base.splitInBatches
Config:
  batchSize: 5

  // Split In Batches node loops: processes 5 items, waits for downstream,
  // then processes next 5. Much better than FOR EACH in n8n.

Node: HTTP Request — FreeLLM scoring
Type: n8n-nodes-base.httpRequest
Config:
  method: POST
  url: {{ $env.FREELLM_URL }}/chat/completions
  body:
    model: "google/gemma-4-31b-it:free"
    messages:
      - role: system
        content: |
          You are a job scoring engine for an Electrical & Electronic Engineering
          graduate in Kenya. Score each job 0-100 based on:
          - EEE Relevance (30%): direct EEE role=100, adjacent=70, general eng=40
          - Entry Level (25%): graduate/junior=100, 0-2yrs=80, 2-5yrs=40, senior=10
          - Location (20%): Nairobi=100, Kenya=70, Remote=90, East Africa=50
          - Company Quality (15%): known company=100, has website=70, no web=20
          - Recency (10%): <3 days=100, <7 days=70, <14 days=40

          Return ONLY a JSON array. No markdown, no explanation, no code fences.
          Each object: {"index":0,"score":85,"breakdown":{},"tags":[],"summary":""}
      - role: user
        content: |
          Score these jobs:
          {{ items.map((item, i) => `${i+1}. ${item.title} at ${item.company} in ${item.location} — ${item.description_raw}`).join('\n') }}

  options:
    timeout: 30000  // 30s timeout
    continueOnFail: true

  // Model fallback chain (if primary returns 429/404/timeout):
  // 1. google/gemma-4-31b-it:free
  // 2. meta-llama/llama-3.3-70b-instruct:free
  // 3. openai/gpt-oss-20b:free

Node: Code — Parse scores with fallback
  const response = $input.first().json

  // If FreeLLM failed, assign defaults
  if (response.error || response.status >= 400) {
    return items.map(item => ({
      ...item,
      score: 50,
      score_breakdown: null,
      tags: [...item.tags, "unvalidated"],
      summary: "Scoring failed — default score assigned"
    }))
  }

  // Extract JSON from response (handles markdown code fences)
  let content = response.choices[0].message.content
  const jsonMatch = content.match(/\[[\s\S]*\]/)
  if (!jsonMatch) {
    // Fallback if no JSON array found
    return items.map(item => ({
      ...item, score: 50, tags: [...item.tags, "unvalidated"],
      summary: "Score parse failed"
    }))
  }

  let scores
  try {
    scores = JSON.parse(jsonMatch[0])
  } catch (e) {
    return items.map(item => ({
      ...item, score: 50, tags: [...item.tags, "unvalidated"],
      summary: "Score JSON invalid"
    }))
  }

  // Validate and merge scores
  return items.map((item, i) => {
    const s = scores.find(sc => sc.index === i) || {}
    return {
      ...item,
      score: typeof s.score === 'number' ? Math.min(100, Math.max(0, s.score)) : 50,
      score_breakdown: s.breakdown || null,
      tags: [...new Set([...(item.tags || []), ...(s.tags || [])])],
      summary: s.summary || ""
    }
  })

Node: Wait
  seconds: 1  // Rate limit buffer between batches
```

### 7. Write to Notion (with Split In Batches)

```
Node: Split In Batches
  batchSize: 1  // Sequential writes for rate limiting

Node: Code — Build Notion payload (handles nulls)
  const item = $input.first().json

  const properties = {
    "Title": {
      "title": [{ "text": { "content": (item.title || "").substring(0, 97) } }]
    },
    "URL": { "url": item.url },
    "Score": { "number": item.score },
    "Status": { "status": { "name": "new" } },
    "Source": { "select": { "name": item.source } },
    "Tags": {
      "multi_select": (item.tags || [])
        .filter(t => t && /^[a-z0-9\-]+$/.test(t))
        .map(t => ({ name: t }))
    },
    "Scraped At": { "date": { "start": item.scraped_at } },
    "Type": { "select": { "name": item.type || "full-time" } }
  }

  // Only include optional fields if non-null
  if (item.salary && item.salary !== "Not listed") {
    properties["Salary"] = {
      "rich_text": [{ "text": { "content": item.salary } }]
    }
  }

  if (item.summary) {
    properties["Notes"] = {
      "rich_text": [{ "text": { "content": item.summary } }]
    }
  }

  return { properties, item }

Node: HTTP Request — Create Notion page
  method: POST
  url: https://api.notion.com/v1/pages
  headers:
    Authorization: Bearer {{ $env.NOTION_API_TOKEN }}
    Notion-Version: 2022-06-28
  body:
    parent: { "database_id": "{{ $env.NOTION_JOBS_DB_ID }}" }
    properties: {{ $json.properties }}
  options:
    continueOnFail: true

  // Retry on 429: exponential backoff 1s → 2s → 4s
  // On 400: log payload, skip, continue

Node: Wait
  milliseconds: 350  // Notion rate limit: ~3 req/s
```

### 8. Post to Discord

```
Node: Code — Build Discord payloads
  const item = $input.first().json.item
  const notionResponse = $input.first().json

  // Determine color and channel
  let color, webhookUrl
  if (item.score >= 90) {
    color = 16744576  // orange (alert)
    webhookUrl = $env.DISCORD_WEBHOOK_ALERTS
  } else if (item.score >= 70) {
    color = 3066993   // green (validated)
    webhookUrl = $env.DISCORD_WEBHOOK_FEED
  } else if (item.score >= 40) {
    color = 3447003   // blue (low match)
    webhookUrl = $env.DISCORD_WEBHOOK_FEED
  } else {
    return null  // Don't post jobs below 40
  }

  const embed = {
    title: item.title.substring(0, 256),  // Discord embed title limit
    url: item.url,
    color: color,
    fields: [
      { name: "Company", value: (item.company || "Unknown").substring(0, 1024), inline: true },
      { name: "Location", value: (item.location || "Unknown").substring(0, 1024), inline: true },
      { name: "Score", value: `${item.score}/100${item.score >= 90 ? " 🔥" : ""}`, inline: true },
      { name: "Source", value: item.source, inline: true }
    ],
    footer: { text: `via n8n • ${new Date().toISOString()}` }
  }

  if (item.tags?.length) {
    embed.fields.push({ name: "Tags", value: item.tags.join(", ").substring(0, 1024), inline: true })
  }

  return { webhookUrl, embed, item }

Node: IF — should post
  condition: {{ $json !== null }}
  false: skip

Node: HTTP Request — Post to Discord
  method: POST
  url: {{ $json.webhookUrl }}
  body:
    embeds: [{{ $json.embed }}]
  options:
    continueOnFail: true  // Don't crash on Discord failure

  // For score >= 90: ALSO post to #feed-eee (duplicate is intentional)
  // Use a second HTTP Request node in parallel if score >= 90
```

### 9. Execution Log

```
Node: Code — Build summary
  // Aggregate counts from all branches
  const summary = {
    total_fetched: allItems.length,
    eee_filtered: filteredItems.length,
    new_after_dedup: newItems.length,
    scored: scoredItems.length,
    notion_written: notionSuccessCount,
    discord_posted: discordPostCount,
    alerts_sent: alertCount,
    errors: errorLog
  }

Node: HTTP Request — Post to #log
  method: POST
  url: {{ $env.DISCORD_WEBHOOK_LOG }}
  body:
    embeds:
      - title: "Job Feed Scan — {{ $now.toISO() }}"
        color: {{ summary.errors.length > 0 ? 15158332 : 3066993 }}
        fields:
          - { name: "Fetched", value: "{{ summary.total_fetched }}", inline: true }
          - { name: "EEE Match", value: "{{ summary.eee_filtered }}", inline: true }
          - { name: "New", value: "{{ summary.new_after_dedup }}", inline: true }
          - { name: "Notion", value: "{{ summary.notion_written }}", inline: true }
          - { name: "Discord", value: "{{ summary.discord_posted }}", inline: true }
          - { name: "Alerts", value: "{{ summary.alerts_sent }}", inline: true }
        footer: { text: "errors: {{ summary.errors.length }}" }
  options:
    continueOnFail: true
```

---

## Helper Functions (Code Nodes)

### normalizeLocation

```javascript
function normalizeLocation(raw) {
  if (!raw) return "Unknown"
  const loc = raw.trim()
  const map = {
    "nairobi": "Nairobi", "nairobi, kenya": "Nairobi",
    "mombasa": "Mombasa", "mombasa, kenya": "Mombasa",
    "kisumu": "Kisumu", "nakuru": "Nakuru",
    "kenya": "Kenya", "remote": "Remote",
    "east africa": "East Africa"
  }
  return map[loc.toLowerCase()] || loc
}
```

### stripHtml

```javascript
function stripHtml(html) {
  if (!html) return ""
  return html.replace(/<[^>]*>/g, "").replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<").replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"').replace(/&#39;/g, "'")
    .replace(/\s+/g, " ").trim()
}
```

### extractSalary

```javascript
function extractSalary(item) {
  const text = item.contentSnippet || item.description || ""
  const match = text.match(/(?:KES|kes|Ksh|ksh)\s*[\d,]+(?:\s*[-–]\s*(?:KES|kes|Ksh|ksh)?\s*[\d,]+)?/i)
  return match ? match[0] : null
}
```

---

## Error Handling Matrix

| Failure | Node | Behavior | Impact |
|---------|------|----------|--------|
| RSS feed down | HTTP Request | continueOnFail, log warning | Other sources continue |
| Careerjet API error | HTTP Request | continueOnFail, skip | Other sources continue |
| MyJobMag empty | IF check | skip to merge | Other sources continue |
| FreeLLM timeout | HTTP Request | 30s timeout, default score 50 | Jobs still posted, tagged "unvalidated" |
| FreeLLM JSON parse fail | Code | regex extract + try/catch, default 50 | Jobs still posted |
| Notion 429 | HTTP Request | retry 1s→2s→4s backoff | Delayed but not lost |
| Notion 400 | HTTP Request | continueOnFail, log payload | Job skipped, logged |
| Discord webhook fail | HTTP Request | continueOnFail | Not lost from Notion |
| All sources fail | Code | empty array → workflow ends | Logged in #log |
| Location mismatch | Code | normalizeLocation() | Consistent Select options |
| Title > 100 chars | Code | substring(0, 97) + "..." | Clean display |
| Tags with special chars | Code | regex filter `[a-z0-9-]+` | Valid Notion options |

## Dependencies

| Dependency | Required For | Fallback |
|------------|-------------|----------|
| FreeLLM (host.docker.internal:3001) | Scoring | Default score 50, tag "unvalidated" |
| Notion API | Storage | Jobs still posted to Discord |
| Discord webhooks | Notifications | Jobs still in Notion |
| RSS feeds (3 sites) | Data | Careerjet + MyJobMag continue |
| Careerjet API | Data | RSS + MyJobMag continue |
| MyJobMag | Data | RSS + Careerjet continue |

## Triggers Company Enrichment

After Notion writes complete, extract unique company names and call [[wf2-company-enrichment]] as sub-workflow. Pass `job_notion_page_ids[]` per company so enrichment can link all related jobs.

```
Node: Code — Build enrichment queue
  const companyMap = new Map()
  FOR EACH written job:
    const key = normalizeCompanyName(job.company)
    if (!companyMap.has(key)) {
      companyMap.set(key, {
        name: job.company,
        job_notion_page_ids: [],
        source: job.source
      })
    }
    companyMap.get(key).job_notion_page_ids.push(job.notion_page_id)

  return Array.from(companyMap.values())

Node: Execute Workflow — Company Enrichment
  input: enrichment_queue
```

## See Also

- [[wf2-company-enrichment]]
- [[Kenyan Job Sites — Feeds & Scraping]]
- [[Discord Bot Setup]]
- [[Notion Integration]]
- [[Job Hunt Ops — Map of Content]]
