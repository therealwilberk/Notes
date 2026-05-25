# Workflow 1: Job Feed Scanner — Pseudocode

> n8n workflow. Cron-triggered. Scrapes job sources, scores with FreeLLM, writes to Notion, posts to Discord.

## Trigger

```
EVERY 4 HOURS:
  start workflow
```

## Phase 1: Fetch from All Sources (parallel)

```
PARALLEL BRANCH A — RSS Sources:
  node: RSS Feed Trigger (OpenedCareer)
    url: https://openedcareer.com/feed/
    deduplicate: by guid (n8n built-in)

  node: RSS Feed Trigger (CareerPoint)
    url: https://www.careerpointkenya.co.ke/feed/
    deduplicate: by guid

  node: RSS Feed Trigger (JobWeb)
    url: https://jobwebkenya.com/feed/
    deduplicate: by guid

  node: Code — Normalize RSS items
    input: each RSS item
    output: { title, company, location, url, source, scraped_at, description_raw, type }
    logic:
      - Parse title: strip HTML entities, trim
      - Extract company: from dc:creator or description regex
      - Extract location: from description or category
      - Set source: "openedcareer" | "careerpoint" | "jobweb"
      - Set scraped_at: now() ISO
      - description_raw: item.contentSnippet or item.content
      - Default type: "full-time" (refine later)

PARALLEL BRANCH B — Careerjet API:
  node: Schedule Trigger (same 4h cron, or merge into single trigger)
    // Note: can share trigger with Branch A if using single cron + split

  node: HTTP Request
    method: GET
    url: https://search.api.careerjet.net/v4/query
    params:
      locale_code: en_KE
      keywords: "electrical OR electronics OR power OR energy OR automation OR graduate"
      location: "Kenya"
      page: 1
      pagesize: 30
      sort: date
    // Auth: API key in header if required

  node: IF — response has results
    true: continue
    false: log "Careerjet returned 0 results" → merge point (skip)

  node: Code — Normalize Careerjet items
    input: response.jobs[]
    output: same schema as RSS
    logic:
      - title: job.title
      - company: job.company
      - location: job.locations
      - url: job.url
      - source: "careerjet"
      - description_raw: job.description (HTML, strip tags)

PARALLEL BRANCH C — MyJobMag HTTP Scrape:
  node: Schedule Trigger

  node: HTTP Request
    method: GET
    url: https://www.myjobmag.co.ke/jobs-location/nairobi/1
    // Also: /jobs-location/mombasa/1 for broader coverage

  node: HTML Extract
    selectors:
      job_title: ".job-list h2 a"
      company: ".job-list .company-name"
      location: ".job-list .location"
      link: ".job-list h2 a[href]"
      date: ".job-list .date-posted"

  node: IF — extract succeeded (items.length > 0)
    true: continue
    false: log "MyJobMag scrape returned empty" → merge point

  node: Code — Normalize MyJobMag items
    output: same schema
    logic:
      - Prepend "https://www.myjobmag.co.ke" to relative links
      - source: "myjobmag"

MERGE POINT:
  node: Merge (Combine)
    mode: append
    input: all normalized items from A + B + C
```

## Phase 2: EEE Keyword Filter

```
node: Code — Filter for EEE relevance
  input: all merged items
  logic:
    keywords_eee = [
      "electrical", "electronics", "power", "energy", "solar",
      "automation", "controls", "instrumentation", "SCADA", "PLC",
      "transmission", "distribution", "renewable", "grid", "substation",
      "transformer", "circuit", "protection", "relay", "metering",
      "EEE", "telecom", "signal", "embedded", "power systems"
    ]

    keywords_entry = [
      "graduate", "junior", "entry", "intern", "trainee",
      "0-2 years", "1-2 years", "fresh", "new grad", "NYSC"
    ]

    FOR EACH item:
      text = (item.title + " " + item.description_raw).lower()

      eee_match = ANY keyword in keywords_eee found in text
      entry_match = ANY keyword in keywords_entry found in text

      IF NOT eee_match:
        DISCARD (not EEE related)
        CONTINUE

      item.tags = []
      IF entry_match: item.tags.push("entry-level")
      // More tags added after scoring

  output: filtered_items[] (only EEE-related jobs)
```

## Phase 3: Deduplicate Against Notion

```
node: HTTP Request — Query Notion Jobs DB for existing URLs
  method: POST
  url: https://api.notion.com/v1/data_sources/{jobs_data_source_id}/query
  headers:
    Authorization: Bearer {NOTION_API_TOKEN}
    Notion-Version: 2025-09-03
  body:
    filter:
      property: "URL"
      url:
        is_not_empty: true
    page_size: 100
  // NOTE: paginate if > 100 existing jobs. For now, recent 100 is enough
  // because we run every 4h, unlikely to have >100 new jobs per cycle

node: Code — Extract existing URLs
  input: notion response
  logic:
    existing_urls = Set()
    FOR EACH page in results:
      url = page.properties.URL.url
      IF url: existing_urls.add(url)

    new_items = filtered_items.filter(item => NOT existing_urls.has(item.url))

  output: new_items[]

node: IF — new_items.length > 0
  true: continue to Phase 4
  false: log "No new jobs this cycle" → end workflow (success)
```

## Phase 4: Score with FreeLLM

```
node: Code — Batch items for scoring
  input: new_items[]
  logic:
    // Batch size: 5 jobs per API call to avoid token limits
    batches = chunk(new_items, 5)
    // Store batches for sequential processing

FOR EACH batch:

  node: HTTP Request — FreeLLM scoring
    method: POST
    url: http://127.0.0.1:3001/v1/chat/completions
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

            Return ONLY valid JSON array. Each object:
            { "index": 0, "score": 85, "breakdown": {"relevance":90,"entry_level":80,"location":95,"company":70,"recency":100}, "tags": ["power","graduate","nairobi"], "summary": "one line summary" }

            Index maps to the job's position in the input array.
        - role: user
          content: |
            Score these jobs:
            1. {title} at {company} in {location} — {description_raw first 200 chars}
            2. ...

  node: IF — FreeLLM response valid
    true: continue
    false: log error, assign default score = 50, tags = ["unvalidated"]
           // Don't block the pipeline on scoring failure

  node: Code — Parse scores and merge back
    input: FreeLLM response + batch items
    logic:
      scores = JSON.parse(response)
      FOR EACH score in scores:
        batch[score.index].score = score.score
        batch[score.index].score_breakdown = score.breakdown
        batch[score.index].tags = [...batch[score.index].tags, ...score.tags]
        batch[score.index].summary = score.summary

  // Rate limit: wait 1s between batches to not hammer FreeLLM
  node: Wait — 1 second
```

## Phase 5: Write to Notion

```
FOR EACH scored item:

  node: HTTP Request — Create Notion page in Jobs DB
    method: POST
    url: https://api.notion.com/v1/pages
    headers:
      Authorization: Bearer {NOTION_API_TOKEN}
      Notion-Version: 2025-09-03
    body:
      parent: { "database_id": "{JOBS_DB_ID}" }
      properties:
        "Title": { "title": [{ "text": { "content": "{item.title}" }}] }
        "URL": { "url": "{item.url}" }
        "Score": { "number": {item.score} }
        "Status": { "status": { "id": "not-started" } }
        "Source": { "select": { "name": "{item.source}" } }
        "Tags": { "multi_select": [{item.tags.map(t => ({name: t}))}] }
        "Scraped At": { "date": { "start": "{item.scraped_at}" } }
        "Salary": { "rich_text": [{ "text": { "content": "{item.salary || 'Not listed'}" }}] }
        "Type": { "select": { "name": "{item.type}" } }

    error handling:
      IF 429 (rate limit): wait 500ms, retry (max 3)
      IF 400 (bad schema): log error with full payload, skip item
      IF 200: store notion_page_id for Discord embed

  node: Wait — 350ms (Notion rate limit: ~3 req/s)
```

## Phase 6: Check for New Companies (trigger enrichment)

```
node: Code — Extract unique companies from new items
  logic:
    companies = Set(new_items.map(i => i.company.toLowerCase().trim()))
    // Dedup: if 5 jobs from "Kenya Power", only enqueue once

    enrichment_queue = []
    FOR EACH company in companies:
      enrichment_queue.push({
        name: item.company,  // original casing
        first_seen_url: item.url,
        source: item.source
      })

    // Store as workflow static data for Workflow 2 to pick up
    // OR: write to a temp Notion page / file
    // Best approach: n8n Sub-Workflow trigger or webhook

  // OPTION A: Call Workflow 2 as sub-workflow
  node: Execute Workflow — trigger Company Enrichment
    input: enrichment_queue

  // OPTION B: Write queue to file, Workflow 2 picks up on its own cron
  // OPTION C: POST to Workflow 2 webhook trigger
```

## Phase 7: Post to Discord

```
FOR EACH scored item:

  node: IF — score >= 90
    true:
      node: HTTP Request — Post to #alerts webhook
        url: {DISCORD_WEBHOOK_ALERTS}
        body:
          embeds:
            - title: "{item.title}"
              url: "{item.url}"
              color: 16744576  // orange for 🔥 alert
              fields:
                - { name: "Company", value: "{item.company}", inline: true }
                - { name: "Location", value: "{item.location}", inline: true }
                - { name: "Score", value: "{item.score}/100 🔥", inline: true }
                - { name: "Source", value: "{item.source}", inline: true }
                - { name: "Tags", value: "{item.tags.join(', ')}", inline: true }
              footer: { text: "via n8n • {now()}" }
      // ALSO post to #feed-eee (see below)

  node: IF — score >= 70
    true:
      node: HTTP Request — Post to #feed-eee webhook (green)
        url: {DISCORD_WEBHOOK_FEED}
        body:
          embeds:
            - title: "{item.title}"
              url: "{item.url}"
              color: 3066993  // green
              fields: [same as above but score without 🔥]

  node: IF — score < 70 AND score >= 40
    true:
      node: HTTP Request — Post to #feed-eee webhook (blue)
        url: {DISCORD_WEBHOOK_FEED}
        body:
          embeds:
            - title: "{item.title}"
              url: "{item.url}"
              color: 3447003  // blue
              fields: [same]

  node: IF — score < 40
    true: log "Low-score job, not posting" → skip Discord
          // Still saved in Notion for reference
```

## Phase 8: Execution Log

```
node: Code — Build summary
  logic:
    summary = {
      total_fetched: all_items.length,
      eee_filtered: filtered_items.length,
      new_after_dedup: new_items.length,
      scored: scored_items.length,
      notion_written: notion_success_count,
      discord_posted: discord_post_count,
      alerts_sent: alert_count,  // score > 90
      errors: error_log
    }

node: HTTP Request — Post to #log webhook
  url: {DISCORD_WEBHOOK_LOG}
  body:
    embeds:
      - title: "Job Feed Scan — {now()}"
        color: {errors.length > 0 ? 15158332 : 3066993}  // red if errors, green if clean
        fields:
          - { name: "Fetched", value: "{total_fetched}", inline: true }
          - { name: "EEE Match", value: "{eee_filtered}", inline: true }
          - { name: "New", value: "{new_after_dedup}", inline: true }
          - { name: "Notion", value: "{notion_written}", inline: true }
          - { name: "Discord", value: "{discord_posted}", inline: true }
          - { name: "Alerts", value: "{alerts_sent}", inline: true }
        footer: { text: "errors: {errors.length}" }

END WORKFLOW
```

## Error Handling Summary

| Failure | Behavior |
|---------|----------|
| RSS feed down | Log warning, continue with other sources |
| Careerjet API error | Log, skip, continue |
| MyJobMag scrape empty | Log, skip, continue |
| FreeLLM timeout | Default score 50, tag "unvalidated", continue |
| FreeLLM JSON parse fail | Default score 50, tag "unvalidated", continue |
| Notion write 429 | Retry 3x with 500ms backoff |
| Notion write 400 | Log payload, skip item, continue |
| Discord webhook fail | Log, continue (don't block on notification) |
| All sources fail | Log error, post to #log, end cleanly |

## Dependencies

| Dependency | Required For | Fallback |
|------------|-------------|----------|
| FreeLLM (127.0.0.1:3001) | Scoring | Default score 50 |
| Notion API | Storage | Workflow still posts to Discord |
| Discord webhooks | Notifications | Jobs still saved in Notion |
| RSS feeds (3 sites) | Data source | Other sources continue |
| Careerjet API | Data source | Other sources continue |
| MyJobMag | Data source | Other sources continue |
