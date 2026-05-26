---
type: project
tags:
  - n8n
  - workflow
  - enrichment
  - company
  - job-search
  - notion
aliases:
  - "Company Enrichment"
  - "WF2"
parent: "[[Projects/active/Job-Search-Infrastructure/Job Hunt Ops — Map of Content.md]]"
created: 2026-05-25
status: ready-to-build
---

# Workflow 2: Company Enrichment

> [!info] Part of [[Job Hunt Ops — Map of Content]]

n8n workflow. Triggered by sub-workflow call from [[wf1-job-feed-scanner]] (primary) or 12h cron (fallback). Enriches company profiles in Notion and posts new discoveries to Discord.

## Architecture

```
Trigger: Sub-workflow call from WF1 (primary)
       : 12h cron (fallback catch-all)
  ↓
Check Companies DB for existing companies
  ↓
Link existing companies to new jobs (relation update)
  ↓
Enrich new companies via FreeLLM
  ↓
Write to Companies DB + Link to Jobs DB
  ↓
Post new companies to #companies Discord
  ↓
Execution Log → #log
```

## Triggers

### Primary: Sub-Workflow Call from WF1

```
Input: enrichment_queue[] = [{
  name: "Kenya Power",
  job_notion_page_ids: ["page-id-1", "page-id-2", "page-id-3"],
  source: "careerjet"
}]

// WF1 passes ALL job page IDs per company, not just the first one.
// This ensures every related job gets the Company relation set.
```

### Fallback: 12h Cron

```
Node: Schedule Trigger
  interval: every 12 hours

Node: HTTP Request — Query Jobs with empty Company relation
  method: POST
  url: https://api.notion.com/v1/databases/{{ $env.NOTION_JOBS_DB_ID }}/query
  body:
    filter:
      and:
        - property: "Company"
          relation:
            is_empty: true
        - property: "Scraped At"
          date:
            on_or_after: "{{ $now.minus({ days: 7 }).toISO() }}"
    page_size: 100

Node: Code — Build enrichment queue
  const companyMap = new Map()
  FOR EACH job page:
    const name = job.properties?.["Title"]?.title?.[0]?.text?.content
    const company = extractCompanyFromTitle(name) || "Unknown"
    const key = normalizeCompanyName(company)

    if (!companyMap.has(key)) {
      companyMap.set(key, { name: company, job_notion_page_ids: [], source: "fallback" })
    }
    companyMap.get(key).job_notion_page_ids.push(job.id)

  return Array.from(companyMap.values())
```

---

## Node-by-Node Specification

### 1. Check Companies DB (Dedup)

```
Node: HTTP Request — Query existing companies
  method: POST
  url: https://api.notion.com/v1/databases/{{ $env.NOTION_COMPANIES_DB_ID }}/query
  headers:
    Authorization: Bearer {{ $env.NOTION_API_TOKEN }}
    Notion-Version: 2022-06-28
  body:
    page_size: 100
  options:
    continueOnFail: true

Node: Code — Split into existing vs new
  const existingCompanies = new Map()
  FOR EACH page in results:
    const name = page.properties?.Name?.title?.[0]?.text?.content
    if (name) {
      existingCompanies.set(normalizeCompanyName(name), page.id)
    }

  const existing = []  // companies already in DB
  const toEnrich = []  // companies needing enrichment

  FOR EACH company in enrichment_queue:
    const key = normalizeCompanyName(company.name)
    if (existingCompanies.has(key)) {
      existing.push({
        ...company,
        notion_page_id: existingCompanies.get(key)
      })
    } else {
      toEnrich.push(company)
    }

  return { existing, toEnrich }
```

### 2. Link Existing Companies to Jobs

```
// For companies that already exist, just update the job's Company relation.
// No enrichment needed.

Node: Split In Batches
  batchSize: 1
  items: {{ $json.existing }}

Node: Code — Build relation update for ALL job pages
  const company = $input.first().json
  // company.job_notion_page_ids is an array of all related job page IDs

  return company.job_notion_page_ids.map(jobId => ({
    job_page_id: jobId,
    company_page_id: company.notion_page_id
  }))

Node: Split In Batches (inner)
  batchSize: 1

Node: HTTP Request — Update job's Company relation
  method: PATCH
  url: https://api.notion.com/v1/pages/{{ $json.job_page_id }}
  headers:
    Authorization: Bearer {{ $env.NOTION_API_TOKEN }}
    Notion-Version: 2022-06-28
  body:
    properties:
      "Company":
        relation:
          - id: "{{ $json.company_page_id }}"
  options:
    continueOnFail: true

Node: Wait
  milliseconds: 350
```

### 3. Enrich New Companies

```
Node: Split In Batches
  batchSize: 1
  items: {{ $json.toEnrich }}

  // Sequential: each company gets full attention from FreeLLM
  // 10 companies × ~5s per FreeLLM call = ~50s total. Within n8n timeout.

Node: HTTP Request — FreeLLM company research
  method: POST
  url: {{ $env.FREELLM_URL }}/chat/completions
  body:
    model: "openai/gpt-oss-120b:free"
    messages:
      - role: system
        content: |
          You are a company research agent for a Kenyan job search database.
          Given a company name, find reliable information.

          Return ONLY valid JSON (no markdown, no code fences, no explanation):
          {
            "name": "Official Company Name",
            "website": "https://..." or null,
            "linkedin": "https://linkedin.com/company/..." or null,
            "sector": "power_distribution|solar|automation|electronics|energy|construction|consulting|manufacturing|telecom|other",
            "size": "1-50|51-200|201-1000|1000+|unknown",
            "location": "City, Country" or null,
            "description": "One-line description" or null,
            "hiring_active": true or false,
            "careers_url": "https://..." or null,
            "confidence": "high|medium|low"
          }

          Rules:
          - If you cannot find reliable info, use null. Do NOT guess URLs.
          - Only include URLs you are confident exist.
          - Sector must be one of the listed options. Use "other" if none fit.
          - Confidence: high = verified info found, medium = partial, low = minimal/no info.

      - role: user
        content: |
          Company: {{ $json.name }}
          Found on: {{ $json.source }} (Kenyan job listing site)
          Research this company and return their profile.

  options:
    timeout: 30000
    continueOnFail: true

  // Model fallback chain:
  // 1. openai/gpt-oss-120b:free
  // 2. google/gemma-4-31b-it:free
  // 3. meta-llama/llama-3.3-70b-instruct:free

Node: Code — Parse and validate profile
  const response = $input.first().json
  const company = $input.first().json._company  // from previous node

  // FreeLLM failed
  if (response.error || response.status >= 400) {
    return {
      name: company.name,
      website: null, linkedin: null, sector: "other",
      size: "unknown", location: null, description: null,
      hiring_active: false, careers_url: null,
      confidence: "failed",
      job_notion_page_ids: company.job_notion_page_ids
    }
  }

  // Extract JSON from response
  let content = response.choices[0].message.content
  const jsonMatch = content.match(/\{[\s\S]*\}/)
  if (!jsonMatch) {
    return { name: company.name, confidence: "failed", ... }
  }

  let profile
  try { profile = JSON.parse(jsonMatch[0]) }
  catch { return { name: company.name, confidence: "failed", ... } }

  // Validate URLs — strip hallucinated ones
  if (profile.website && !profile.website.match(/^https?:\/\//)) profile.website = null
  if (profile.linkedin && !profile.linkedin.includes("linkedin.com")) profile.linkedin = null
  if (profile.careers_url && !profile.careers_url.match(/^https?:\/\//)) profile.careers_url = null

  // Normalize company name
  profile.name = profile.name || company.name

  // Pass through job IDs for relation linking
  profile.job_notion_page_ids = company.job_notion_page_ids
  profile._source_company_name = company.name

  return profile
```

### 4. Write to Companies DB

```
Node: Code — Build Notion payload (handles nulls)
  const profile = $input.first().json

  const properties = {
    "Name": { "title": [{ "text": { "content": profile.name.substring(0, 97) } }] },
    "Sector": { "select": { "name": profile.sector || "other" } },
    "Size": { "select": { "name": profile.size || "unknown" } },
    "Hiring Active": { "checkbox": !!profile.hiring_active },
    "Enriched At": { "date": { "start": new Date().toISOString() } },
    "Source": { "select": { "name": profile.confidence === "failed" ? "needs-enrichment" : "pipeline" } }
  }

  // Only include non-null optional fields
  if (profile.website) properties["Website"] = { "url": profile.website }
  if (profile.linkedin) properties["LinkedIn"] = { "url": profile.linkedin }
  if (profile.careers_url) properties["Careers URL"] = { "url": profile.careers_url }
  if (profile.location) {
    properties["Location"] = { "rich_text": [{ "text": { "content": profile.location } }] }
  }
  if (profile.description) {
    properties["Description"] = { "rich_text": [{ "text": { "content": profile.description } }] }
  }

  return { properties, profile }

Node: HTTP Request — Create company page
  method: POST
  url: https://api.notion.com/v1/pages
  headers:
    Authorization: Bearer {{ $env.NOTION_API_TOKEN }}
    Notion-Version: 2022-06-28
  body:
    parent: { "database_id": "{{ $env.NOTION_COMPANIES_DB_ID }}" }
    properties: {{ $json.properties }}
  options:
    continueOnFail: true

  // Retry on 429: 1s → 2s → 4s

Node: Wait
  milliseconds: 350

Node: Set — Store company page ID
  company_page_id: {{ $json.id }}
  profile: {{ $('Code — Build Notion payload').item.json.profile }}
```

### 5. Link New Company to All Related Jobs

```
Node: Code — Build job link list
  const profile = $input.first().json.profile
  const companyPageId = $input.first().json.company_page_id

  return profile.job_notion_page_ids.map(jobId => ({
    job_page_id: jobId,
    company_page_id: companyPageId
  }))

Node: Split In Batches
  batchSize: 1

Node: HTTP Request — Update each job's Company relation
  method: PATCH
  url: https://api.notion.com/v1/pages/{{ $json.job_page_id }}
  body:
    properties:
      "Company":
        relation:
          - id: "{{ $json.company_page_id }}"
  options:
    continueOnFail: true

Node: Wait
  milliseconds: 350
```

### 6. Post to Discord

```
Node: Code — Build Discord embed
  const profile = $input.first().json.profile

  // Skip failed enrichments (posted as "needs manual lookup")
  const isLowConfidence = profile.confidence === "low" || profile.confidence === "failed"

  const embed = {
    title: isLowConfidence
      ? `${profile.name} — needs manual lookup`
      : profile.name,
    url: profile.website || profile.linkedin || null,
    color: isLowConfidence ? 16776960 : 3066993,  // yellow : green
    description: profile.description || "No description available",
    fields: [
      { name: "Sector", value: profile.sector || "Unknown", inline: true },
      { name: "Size", value: profile.size || "Unknown", inline: true },
      { name: "Location", value: profile.location || "Unknown", inline: true },
      { name: "Hiring", value: profile.hiring_active ? "✅" : "❌", inline: true },
      { name: "Website", value: profile.website || "Not found", inline: true },
      { name: "Confidence", value: profile.confidence || "unknown", inline: true }
    ],
    footer: { text: `enrichment pipeline • ${new Date().toISOString()}` }
  }

  return { embed }

Node: HTTP Request — Post to #companies webhook
  method: POST
  url: {{ $env.DISCORD_WEBHOOK_COMPANIES }}
  body:
    embeds: [{{ $json.embed }}]
  options:
    continueOnFail: true
```

### 7. Execution Log

```
Node: Code — Build summary
  const summary = {
    received: enrichment_queue.length,
    already_exists: existingCount,
    enriched: enrichmentSuccessCount,
    failed: enrichmentFailCount,
    jobs_linked: jobsLinkedCount,
    discord_posted: discordPostCount,
    errors: errorLog
  }

Node: HTTP Request — Post to #log
  method: POST
  url: {{ $env.DISCORD_WEBHOOK_LOG }}
  body:
    embeds:
      - title: "Company Enrichment — {{ $now.toISO() }}"
        color: {{ summary.errors.length > 0 ? 15158332 : 3066993 }}
        fields:
          - { name: "Received", value: "{{ summary.received }}", inline: true }
          - { name: "Existing", value: "{{ summary.already_exists }}", inline: true }
          - { name: "Enriched", value: "{{ summary.enriched }}", inline: true }
          - { name: "Failed", value: "{{ summary.failed }}", inline: true }
          - { name: "Jobs Linked", value: "{{ summary.jobs_linked }}", inline: true }
        footer: { text: "errors: {{ summary.errors.length }}" }
  options:
    continueOnFail: true
```

---

## Helper Functions

### normalizeCompanyName

```javascript
function normalizeCompanyName(name) {
  if (!name) return "unknown"
  return name
    .toLowerCase()
    .trim()
    .replace(/\b(ltd|limited|inc|incorporated|co\.|corp|corporation|plc|llc)\b/gi, "")
    .replace(/^the\s+/i, "")
    .replace(/\s+/g, " ")
    .trim()
  // "Kenya Power Ltd" → "kenya power"
  // "The Kenya Power Limited" → "kenya power"
  // Prevents duplicate company entries for same entity
}
```

---

## Error Handling Matrix

| Failure | Node | Behavior | Impact |
|---------|------|----------|--------|
| FreeLLM timeout | HTTP Request | 30s timeout, minimal record | Company created with name only, tagged "needs-enrichment" |
| FreeLLM hallucinated URL | Code — validate | Strip non-http URLs | Clean data in Notion |
| FreeLLM JSON parse fail | Code — regex extract | Try regex, fallback to minimal | Company created with name only |
| Notion 429 | HTTP Request | Retry 1s→2s→4s | Delayed, not lost |
| Notion 400 (null values) | Code — conditional | Only include non-null props | Clean writes |
| Notion 400 (bad schema) | HTTP Request | continueOnFail, log | Company skipped |
| Discord webhook fail | HTTP Request | continueOnFail | Company still in Notion |
| Empty enrichment queue | Code | Return empty, end cleanly | No-op cycle |
| Duplicate company race condition | normalizeCompanyName | Same name → same key | Deduped in Phase 1 |

## Dependencies

| Dependency | Required For | Fallback |
|------------|-------------|----------|
| FreeLLM (gpt-oss-120b) | Company research | Minimal record, "needs-enrichment" |
| Notion API | Storage + linking | Skip, retry on next WF1 trigger |
| Discord webhooks | Notifications | Silent, data still in Notion |
| WF1 trigger | Primary trigger | 12h cron fallback |

## Interaction with WF1

```
WF1 Phase 6                     WF2
    │                            │
    ├── sub-workflow call ──────→├── Phase 1: check existing
    │   (enrichment_queue)       ├── Phase 2: link existing
    │                            ├── Phase 3-5: enrich new + link
    │                            ├── Phase 6: post to Discord
    │   ◄── completion ─────────├── done
    │
    │  (WF1 does NOT wait for WF2)
    │  (Jobs posted to Discord immediately)
    │  (Company relations updated async)
```

## Cron Fallback Design

The 12h cron catches:
- Jobs added manually to Notion (not through WF1)
- Jobs where WF2 failed mid-run
- Jobs where the Company relation was accidentally removed

It queries Jobs DB for empty Company relations from the last 7 days, builds the queue, and runs the same enrichment logic.

## See Also

- [[wf1-job-feed-scanner]]
- [[Data Enrichment Pipeline]]
- [[Notion Integration]]
- [[Discord Bot Setup]]
- [[Job Hunt Ops — Map of Content]]
