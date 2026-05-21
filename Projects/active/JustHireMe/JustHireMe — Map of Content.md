---
tags:
  - moc
  - project
  - justhireme
  - fastapi
  - python
aliases:
  - "JustHireMe"
  - "JHM"
created: 2026-05-21
status: planning
---

# JustHireMe — Map of Content

> **AI-powered job matching + tailored application generation.**
> Python/FastAPI backend. Receives scraped jobs from [[Job Search Infrastructure — Map of Content|n8n]], scores them against your resume, generates tailored applications.

## Scope

| Area | Status | Notes |
|---|---|---|
| API design | Not started | Endpoints: ingest, match, tailor |
| Resume parsing | Not started | PDF → structured data |
| Scoring engine | Not started | Keyword + semantic matching |
| Application gen | Not started | LLM-tailored cover letters |
| n8n integration | Not started | Webhook from n8n workflows |

## Decisions

- **2026-05-21:** Project scaffold created (empty)

## Progress

- [ ] Define API contract (ingest, match, generate)
- [ ] Implement job ingestion endpoint
- [ ] Implement resume parser
- [ ] Implement scoring engine
- [ ] Implement application generator
- [ ] Connect to n8n webhook
