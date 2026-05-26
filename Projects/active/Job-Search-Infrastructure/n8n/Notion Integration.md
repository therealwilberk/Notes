---
type: project
tags:
  - notion
  - database
  - job-search
  - integration
  - api
aliases:
  - "Notion DB"
  - "Notion Jobs"
parent: "[[Projects/active/Job-Search-Infrastructure/Job Hunt Ops — Map of Content.md]]"
created: 2026-05-25
status: setup
---

# Notion Integration

> [!info] Part of [[Job Hunt Ops — Map of Content]]

Notion is the default database for the job hunt pipeline. n8n reads/writes via HTTP Request nodes hitting the Notion API.

## Databases Needed

### 1. Jobs Database

Properties:

| Property | Type | Purpose |
|----------|------|---------|
| Title | Title | Job title |
| Company | Relation → Companies | Link to company profile |
| Location | Select | Nairobi, Remote, Kenya, etc. |
| URL | URL | Original listing link |
| Source | Select | brightermonday, myjobmag, careerjet, etc. |
| Score | Number | Relevance score (0-100) |
| Status | Select | new, validated, applied, rejected, saved |
| Salary | Rich text | Salary range if available |
| Type | Select | full-time, part-time, contract, internship |
| Tags | Multi-select | power, solar, energy, automation, graduate, etc. |
| Scraped At | Date | When the listing was found |
| Applied At | Date | When applied (if applicable) |
| Notes | Rich text | Free-form notes |

### 2. Companies Database

Properties:

| Property | Type | Purpose |
|----------|------|---------|
| Name | Title | Company name |
| Website | URL | Company website |
| LinkedIn | URL | LinkedIn page |
| Sector | Select | power_distribution, solar, automation, etc. |
| Size | Select | 1-50, 51-200, 201-1000, 1000+ |
| Location | Select | Primary location |
| Hiring Active | Checkbox | Currently hiring? |
| Careers URL | URL | Careers page |
| Jobs | Relation → Jobs | Related job listings |
| Enriched At | Date | Last enrichment run |
| Source | Select | pipeline, manual, epra |

### 3. Materials

- **CV page** — current resume, formatted in Canvas
- **Cover Letters** — database of drafted CLs linked to Jobs

## API Setup

### Integration Token

Location: `~/.zshrc.local`

```bash
export NOTION_API_TOKEN=$(grep NOTION_API_TOKEN ~/.zshrc.local | head -1 | sed "s/export NOTION_API_TOKEN=//" | tr -d "'")
```

> [!warning] Token status (2026-05-25): **401 Unauthorized**. Needs refresh at notion.so/my-integrations.

### Sharing Pages with Integration

After creating databases in Notion UI:
1. Click `...` menu on the page/database
2. Select "Connect to" → your integration name
3. Without this, API returns 404

### n8n Connection

In n8n workflows, use HTTP Request nodes:

```
Base URL: https://api.notion.com/v1
Headers:
  Authorization: Bearer {{$env.NOTION_API_TOKEN}}
  Notion-Version: 2025-09-03
  Content-Type: application/json
```

Or store the token as n8n Credential (Header Auth).

## n8n Workflow Nodes

### Write Job to Notion (after validation)

```
HTTP Request node:
  Method: POST
  URL: https://api.notion.com/v1/pages
  Body:
    parent: { "database_id": "<JOBS_DB_ID>" }
    properties:
      Title: { "title": [{ "text": { "content": "{{$json.title}}" }}] }
      Company: { "relation": [{ "id": "{{$json.company_id}}" }] }
      Score: { "number": {{$json.score}} }
      Status: { "select": { "name": "validated" }}
      URL: { "url": "{{$json.url}}" }
      Source: { "select": { "name": "{{$json.source}}" }}
      Scraped At: { "date": { "start": "{{$json.scraped_at}}" }}
```

### Query Jobs (for dashboard)

```
HTTP Request node:
  Method: POST
  URL: https://api.notion.com/v1/data_sources/{data_source_id}/query
  Body:
    filter:
      property: Status
      select:
        equals: validated
    sorts:
      - property: Score
        direction: descending
```

## Canvas (CV Formatting)

Wilber uses Notion Canvas for CV customization. Plan:
1. Store base CV as a Notion page
2. Use Canvas to style/export per-application variants
3. Link CV page from the Materials section
4. Agents can pull CV content via API for cover letter generation

## See Also

- [[n8n Setup & Configuration]]
- [[n8n + Discord Integration]]
- [[Job Hunt Ops — Map of Content]]
