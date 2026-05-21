---
tags:
  - job-search
  - kenya
  - scraping
  - feeds
  - n8n
aliases:
  - "KE Job Sites"
  - "Kenya Jobs"
parent: "[[Job Search Infrastructure — Map of Content]]"
created: 2026-05-21
status: researched
---

# Kenyan Job Sites — Feeds & Scraping

> [!info] Part of [[Job Search Infrastructure — Map of Content]]

Research on Kenyan job sites for automated feed collection via [[n8n Setup & Configuration]].

## Priority Matrix

| Site | RSS/API | Difficulty | Recommendation |
|------|---------|------------|----------------|
| **Careerjet Kenya** | ✅ Public API | Easy | **BEST** — Use API |
| **CareerPoint Kenya** | ✅ WordPress RSS | Easy | Use `/feed/` RSS |
| **JobWeb Kenya** | ✅ WordPress RSS | Easy | Use `/feed/` RSS |
| **MyJobMag Kenya** | ⚠️ XML Feed (verify) | Medium | Verify feed URL |
| **BrighterMonday** | ❌ | Hard | Browser scrape needed |
| **Fuzu** | ❌ | Medium | HTTP scrape |
| **LinkedIn** | ❌ | Very Hard | **SKIP** |

> [!success] No existing Telegram/Discord bots found for any of these sites. No competition.

---

## 1. BrighterMonday Kenya

- **URL:** `https://www.brightermonday.co.ke/`
- **Listings:** `https://www.brightermonday.co.ke/jobs`
- **Category:** `/jobs/{category}/{location}` (e.g., `/jobs/government/nairobi`)
- **Job page:** `/listings/{slug}-{id}`

### Filter Params
- Category via URL path
- Location via URL path
- Experience level filtering

### Anti-Scraping
> [!danger] Cloudflare protected. Requires browser-based scraping (Puppeteer/Playwright) or proxy rotation.

### Existing Scrapers
- `Victornguli/Skraped` — CLI scraper
- `kypchumba/Job-Market-Intelligence-Scraper` — full-stack
- `dkkinyua/job-listings` — Python script

---

## 2. MyJobMag Kenya

- **URL:** `https://www.myjobmag.co.ke/`
- **Location filter:** `/jobs-location/{location}/{page}` (e.g., `/jobs-location/baringo/6`)
- **Job page:** `/job/{slug}`
- **Category:** `/cp/{category-slug}` (e.g., `/cp/procurement-jobs-nairobi`)

### RSS
> [!tip] XML Feed mentioned in page footer. Likely at `https://www.myjobmag.co.ke/feed` or `/feeds/`. Verify.

### Anti-Scraping
Lighter than BrighterMonday. Standard rate limiting.

---

## 3. LinkedIn Kenya

- **Search:** `https://www.linkedin.com/jobs/search/?location=Kenya`
- **GeoId (Kenya):** `103349863`
- **GeoId (Nairobi):** `104347570`

### Filter Params
| Param | Values |
|-------|--------|
| `keywords` | Search terms |
| `geoId` | Location ID |
| `f_TPR` | `r86400` (24h), `r604800` (week) |
| `f_JT` | `F` (full-time), `P` (part-time), `C` (contract) |
| `f_WT` | `1` (on-site), `2` (remote), `3` (hybrid) |
| `start` | Pagination offset (×25) |

> [!danger] **DO NOT SCRAPE.** Aggressive anti-bot, login required, legal risk. Use RSS.app or similar aggregator instead.

---

## 4. Careerjet Kenya

- **URL:** `https://www.careerjet.co.ke/`
- **Search:** `https://www.careerjet.co.ke/search/?l=Kenya&q={keyword}`
- **Category:** `/{category}-jobs-in-kenya.html`

### API Available
> [!success] **Public API!** Best programmatic option.

- **Endpoint:** `https://search.api.careerjet.net/v4/query`
- **Params:** `locale_code`, `keywords`, `location`, `page`, `pagesize`
- **Auth:** API key (free for publishers)
- **Docs:** https://www.careerjet.com/partners/api

---

## 5. Career Point Kenya

- **URL:** `https://www.careerpointkenya.co.ke/`
- **WordPress-based**

### RSS Feeds
> [!success] WordPress RSS available by default.

- Main: `https://www.careerpointkenya.co.ke/feed/`
- RSS: `/feed/rss/`
- RSS2: `/feed/rss2/`
- Tag-specific: `/tag/{tag}/feed/`

### WordPress REST API
- Available at `/wp-json/wp/v2/`

---

## 6. JobWeb Kenya

- **URL:** `https://jobwebkenya.com/`
- **WordPress-based**

### RSS Feeds
> [!success] WordPress RSS likely available.
- `https://jobwebkenya.com/feed/`

---

## 7. Fuzu Kenya

- **URL:** `https://www.fuzu.com/kenya`
- **Listings:** `https://www.fuzu.com/kenya/job`
- **Category:** `/kenya/job/{category-slug}`
- **Pagination:** `?page={N}`

### Anti-Scraping
Standard web protection. HTTP scrape with pagination should work.

---

## Recommended n8n Workflow

```
┌─────────────────────────────────────────────────────┐
│  Phase 1: RSS + API (day 1)                        │
│  ├── Careerjet API (HTTP Request node)             │
│  ├── CareerPoint RSS (RSS Feed Trigger)            │
│  └── JobWeb RSS (RSS Feed Trigger)                 │
├─────────────────────────────────────────────────────┤
│  Phase 2: Verified feeds (day 2-3)                 │
│  └── MyJobMag XML (verify, then RSS Trigger)       │
├─────────────────────────────────────────────────────┤
│  Phase 3: Browser scraping (if needed)             │
│  └── BrighterMonday (Playwright node, last resort) │
└─────────────────────────────────────────────────────┘
```

## See Also

- [[n8n Setup & Configuration]]
- [[n8n + Discord Integration]]
- [[Job Search Infrastructure — Map of Content]]

## Sources

- Web research, 2026-05-21
- GitHub scrapers: Victornguli/Skraped, kypchumba/Job-Market-Intelligence-Scraper
