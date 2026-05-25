# Workflow 2: Company Enrichment — Pseudocode

> n8n workflow. Triggered by new company detection (sub-workflow call or cron). Enriches company profiles and writes to Notion.

## Trigger

```
OPTION A: Sub-workflow call from Workflow 1
  input: enrichment_queue[] = [{ name, first_seen_url, source }]

OPTION B: Cron (every 12h, lower priority)
  1. Query Jobs DB: all jobs where Company relation is empty
  2. Extract unique company names
  3. Cross-reference with Companies DB: skip if already enriched
  4. Build enrichment_queue

// Using Option A (sub-workflow) for real-time enrichment
// Option B as fallback catch-all
```

## Phase 1: Check Companies DB (Dedup)

```
node: HTTP Request — Query Companies DB for existing companies
  method: POST
  url: https://api.notion.com/v1/data_sources/{companies_data_source_id}/query
  headers:
    Authorization: Bearer {NOTION_API_TOKEN}
    Notion-Version: 2025-09-03
  body:
    filter:
      property: "Name"
      title:
        is_not_empty: true
    page_size: 100

node: Code — Build existing companies set
  logic:
    existing_companies = Map()  // normalized name → notion page id
    FOR EACH page in results:
      name = page.properties.Name.title[0].text.content
      existing_companies.set(name.toLowerCase().trim(), page.id)

    new_companies = []
    already_enriched = []

    FOR EACH company in enrichment_queue:
      normalized = company.name.toLowerCase().trim()
      IF existing_companies.has(normalized):
        already_enriched.push({
          ...company,
          notion_page_id: existing_companies.get(normalized)
        })
      ELSE:
        new_companies.push(company)

  output: new_companies[] (need enrichment), already_enriched[] (just link)

  // Store counts for execution log
  static: { skipped: already_enriched.length, to_enrich: new_companies.length }
```

## Phase 2: Link Existing Companies to Jobs

```
// For companies that already exist in Companies DB,
// we still need to update the Job's Company relation

FOR EACH company in already_enriched:

  node: HTTP Request — Find the job page by URL
    method: POST
    url: https://api.notion.com/v1/data_sources/{jobs_data_source_id}/query
    body:
      filter:
        property: "URL"
        url:
          equals: "{company.first_seen_url}"

  node: HTTP Request — Update job's Company relation
    method: PATCH
    url: https://api.notion.com/v1/pages/{job_page_id}
    body:
      properties:
        "Company": { "relation": [{ "id": "{company.notion_page_id}" }] }

  node: Wait — 350ms (Notion rate limit)
```

## Phase 3: Enrich New Companies

```
FOR EACH company in new_companies:

  node: HTTP Request — FreeLLM company research
    method: POST
    url: http://127.0.0.1:3001/v1/chat/completions
    body:
      model: "openai/gpt-oss-120b:free"
      messages:
        - role: system
          content: |
            You are a company research agent. Given a company name and context,
            find and extract company information for a job search database.

            Return ONLY valid JSON:
            {
              "name": "Official Company Name",
              "website": "https://...",
              "linkedin": "https://linkedin.com/company/...",
              "sector": "power_distribution|solar|automation|electronics|energy|construction|consulting|manufacturing|telecom|other",
              "size": "1-50|51-200|201-1000|1000+|unknown",
              "location": "City, Country",
              "description": "One-line description",
              "hiring_active": true,
              "careers_url": "https://...",
              "confidence": "high|medium|low"
            }

            If you cannot find reliable info for a field, use null.
            Do NOT guess or fabricate URLs. Only include URLs you are confident about.
            The sector must be one of the listed options. Use "other" if none fit.

        - role: user
          content: |
            Research this company:
            Name: {company.name}
            Found on: {company.source} (job listing site)
            Context: appeared in a job listing for "{company.first_seen_url}"

    error handling:
      IF FreeLLM timeout or error:
        Create minimal company record with just the name
        Tag as "needs-enrichment"
        Continue

  node: Code — Parse FreeLLM response
    logic:
      TRY:
        profile = JSON.parse(response)
      CATCH:
        profile = {
          name: company.name,
          website: null,
          sector: "other",
          confidence: "failed"
        }
        log error

      // Validate: don't trust hallucinated URLs
      IF profile.website AND NOT profile.website.startsWith("http"):
        profile.website = null
      IF profile.linkedin AND NOT "linkedin.com" in profile.linkedin:
        profile.linkedin = null

  node: HTTP Request — Create company in Notion Companies DB
    method: POST
    url: https://api.notion.com/v1/pages
    body:
      parent: { "database_id": "{COMPANIES_DB_ID}" }
      properties:
        "Name": { "title": [{ "text": { "content": "{profile.name}" }}] }
        "Website": { "url": "{profile.website}" }
        "LinkedIn": { "url": "{profile.linkedin}" }
        "Sector": { "select": { "name": "{profile.sector}" } }
        "Size": { "select": { "name": "{profile.size}" } }
        "Location": { "rich_text": [{ "text": { "content": "{profile.location}" }}] }
        "Description": { "rich_text": [{ "text": { "content": "{profile.description}" }}] }
        "Hiring Active": { "checkbox": {profile.hiring_active} }
        "Careers URL": { "url": "{profile.careers_url}" }
        "Enriched At": { "date": { "start": "{now()}" } }
        "Source": { "select": { "name": "pipeline" } }

    error handling:
      IF 429: retry 3x with 500ms backoff
      IF 400: log, skip, continue

  node: Wait — 350ms

  // Store the new company page ID
  node: Set — company_notion_id = response.id

  node: HTTP Request — Update job's Company relation
    method: PATCH
    url: https://api.notion.com/v1/pages/{job_page_id}
    body:
      properties:
        "Company": { "relation": [{ "id": "{company_notion_id}" }] }

  node: Wait — 350ms
```

## Phase 4: Post to Discord

```
// Only post NEW companies (not already-enriched ones)

FOR EACH company in new_companies (where enrichment succeeded):

  node: IF — profile.confidence == "high"
    true:
      node: HTTP Request — Post to #companies webhook
        url: {DISCORD_WEBHOOK_COMPANIES}
        body:
          embeds:
            - title: "{profile.name}"
              url: "{profile.website || profile.linkedin}"
              color: 3066993  // green = high confidence
              description: "{profile.description}"
              fields:
                - { name: "Sector", value: "{profile.sector}", inline: true }
                - { name: "Size", value: "{profile.size}", inline: true }
                - { name: "Location", value: "{profile.location}", inline: true }
                - { name: "Hiring", value: "{profile.hiring_active ? '✅' : '❌'}", inline: true }
                - { name: "Website", value: "{profile.website || 'Not found'}", inline: true }
              footer: { text: "confidence: {profile.confidence} • via enrichment pipeline" }

  node: IF — profile.confidence == "low" OR profile.confidence == "failed"
    true:
      node: HTTP Request — Post to #companies webhook (yellow)
        body:
          embeds:
            - title: "{company.name} — needs manual lookup"
              color: 16776960  // yellow = low confidence
              description: "Auto-enrichment couldn't find reliable data."
              footer: { text: "check manually and update in Notion" }
```

## Phase 5: Execution Log

```
node: Code — Build summary
  logic:
    summary = {
      received: enrichment_queue.length,
      already_exists: already_enriched.length,
      enriched: enrichment_success_count,
      failed: enrichment_fail_count,
      notion_written: notion_success_count,
      discord_posted: discord_post_count,
      errors: error_log
    }

node: HTTP Request — Post to #log webhook
  body:
    embeds:
      - title: "Company Enrichment — {now()}"
        color: {errors.length > 0 ? 15158332 : 3066993}
        fields:
          - { name: "Received", value: "{received}", inline: true }
          - { name: "Existing", value: "{already_exists}", inline: true }
          - { name: "Enriched", value: "{enriched}", inline: true }
          - { name: "Failed", value: "{failed}", inline: true }
          - { name: "Discord", value: "{discord_posted}", inline: true }

END WORKFLOW
```

## Error Handling Summary

| Failure | Behavior |
|---------|----------|
| FreeLLM timeout | Create minimal record, tag "needs-enrichment", continue |
| FreeLLM hallucinated URL | Validate URLs, strip suspicious ones, continue |
| Notion write 429 | Retry 3x with 500ms backoff |
| Notion write 400 | Log payload, skip, continue |
| Discord webhook fail | Log, continue |
| Empty enrichment queue | Log "nothing to enrich", end cleanly |
| Company name ambiguity | Use FreeLLM's best guess, tag "low-confidence" |

## Dependencies

| Dependency | Required For | Fallback |
|------------|-------------|----------|
| FreeLLM (gpt-oss-120b) | Company research | Minimal record, tag "needs-enrichment" |
| Notion API | Storage + linking | Skip, retry next cycle |
| Discord webhooks | Notifications | Silent, data still in Notion |
| Workflow 1 | Trigger (sub-workflow call) | Cron fallback every 12h |

## Interaction with Workflow 1

```
Workflow 1                          Workflow 2
    │                                   │
    ├── Phase 6: ──sub-workflow call──→  ├── Phase 1: check existing
    │   extract companies                ├── Phase 3: enrich new
    │                                   ├── Phase 4: post to Discord
    │   ◄─── completion ────────────────├── Phase 5: done
    │
    ├── Phase 7: continue posting to Discord
    └── Phase 8: execution log
```

Workflow 1 does NOT wait for Workflow 2 to complete.
Enrichment is async — jobs get posted immediately, companies get enriched in parallel.
The Company relation on the Job gets updated after enrichment completes.

## Cron Fallback (Option B)

```
Schedule: every 12h
  1. Query Jobs DB where Company relation is empty
  2. Get unique company names
  3. Query Companies DB to find which already exist
  4. Build enrichment_queue for missing ones
  5. Run Phase 3-5 as above

Purpose: catches any jobs that slipped through without enrichment
         (e.g., Workflow 2 failed mid-run, or manual jobs added to Notion)
```
