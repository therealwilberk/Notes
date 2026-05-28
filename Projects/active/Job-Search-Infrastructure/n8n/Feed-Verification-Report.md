---
type: project
tags: [project, job-search, n8n, feeds]
created: 2026-05-25
status: done
parent: "[[Projects/active/Job-Search-Infrastructure/Job Hunt Ops — Map of Content.md]]"
---

# Feed Verification Report

**Date:** 2026-05-25
**Verified by:** curl live check against each endpoint

## Summary

| Site                  | Endpoint    | Type     | Status     | Items | Notes                                 |
| --------------------- | ----------- | -------- | ---------- | ----- | ------------------------------------- |
| **OpenedCareer**      | `/feed/`    | RSS 2.0  | ✅ Working  | 15    | WordPress, clean XML                  |
| **CareerPoint Kenya** | `/feed/`    | RSS 2.0  | ✅ Working  | 30    | WordPress, clean XML                  |
| **JobWeb Kenya**      | `/feed/`    | RSS 2.0  | ✅ Working  | 10    | WordPress, clean XML                  |
| **Careerjet**         | `/v4/query` | JSON API | ❌ 401      | —     | Needs API key (HTTP Basic Auth)       |
| **MyJobMag**          | `/feeds/`   | HTML     | ❌ No RSS   | —     | HTML page listing categories, not XML |
| **BrighterMonday**    | `/jobs.rss` | —        | ❌ 410 Gone | —     | RSS endpoint removed                  |

| **Blog Nevine** | `/feeds/posts/default?alt=rss` | Atom→RSS | ✅ Working | 25/page | Blogger, needs keyword filter (mixed content) |

## Detailed Findings

### 1. OpenedCareer — ✅ RSS Working

- **URL:** `https://openedcareer.com/feed/`
- **Content-Type:** `application/rss+xml; charset=UTF-8`
- **Items per feed:** 15
- **Format:** Standard RSS 2.0

**Fields available per item:**

| Field | Example | Notes |
|-------|---------|-------|
| `title` | `Information Technology Intern at Save the Children` | Job title |
| `link` | `https://openedcareer.com/information-technology-intern-at-save-the-children/` | Direct URL |
| `pubDate` | `Mon, 25 May 2026 09:03:39 +0000` | RFC 2822 format |
| `category` | `Information Technology (ICT)`, `Internships` | Multiple per item |
| `dc:creator` | `ShamataElijah` | Author/poster |
| `guid` | `https://openedcareer.com/?p=45034` | Permalink ID |
| `description` | HTML excerpt | Short summary with HTML |
| `content:encoded` | Full HTML | Full job description |

**n8n mapping:** RSS Feed Trigger → Code Node (parse categories for tags, extract location from description) → Discord/Notion.

---

### 2. CareerPoint Kenya — ✅ RSS Working

- **URL:** `https://www.careerpointkenya.co.ke/feed/`
- **Content-Type:** `application/rss+xml; charset=UTF-8`
- **Items per feed:** 30
- **Format:** Standard RSS 2.0

**Fields available per item:**

| Field | Example | Notes |
|-------|---------|-------|
| `title` | `Office Assistant Job IRES` | Job title + company |
| `link` | `https://www.careerpointkenya.co.ke/2026/05/22/office-assistant-job-ires/` | Direct URL |
| `pubDate` | `Fri, 22 May 2026 13:11:31 +0000` | RFC 2822 format |
| `category` | `Administration Jobs In Kenya`, `IRES Jobs` | Multiple, includes company name as category |
| `dc:creator` | `Mercy` | Author |
| `guid` | `https://www.careerpointkenya.co.ke/?p=849840` | Permalink ID |
| `description` | HTML excerpt | Short summary |

**No `content:encoded` field.** Description is the only content. Less data than OpenedCareer.

**n8n mapping:** Same as OpenedCareer. Categories are richer (include company name), useful for auto-tagging.

---

### 3. JobWeb Kenya — ✅ RSS Working

- **URL:** `https://jobwebkenya.com/feed/`
- **Content-Type:** `application/rss+xml; charset=UTF-8`
- **Items per feed:** 10
- **Format:** Standard RSS 2.0

**Fields available per item:**

| Field | Example | Notes |
|-------|---------|-------|
| `title` | `Assistant Housekeeper at British High Commission Nairobi` | Job title + company + location |
| `link` | `https://jobwebkenya.com/jobs/assistant-housekeeper-british-high-commission-nairobi/` | Direct URL |
| `pubDate` | `Mon, 25 May 2026 07:16:13 +0000` | RFC 2822 format |
| `dc:creator` | `jobwebkenyastaff` | Always same author |
| `guid` | `https://jobwebkenya.com/?post_type=job_listing&#038;p=330125` | Custom post type |
| `description` | HTML excerpt | Short summary |
| `content:encoded` | Full HTML | Full job description |
| `site` | `56870501` | WordPress site ID (custom namespace) |

**Title format is packed:** `Title at Company Location`. Needs parsing in Code Node to split.

**n8n mapping:** RSS Feed Trigger → Code Node (split title into title/company/location, parse categories) → Discord/Notion.

---

### 4. Careerjet API — ❌ Needs API Key

- **URL:** `https://search.api.careerjet.net/v4/query`
- **HTTP Status:** 401
- **Error:** `"You did not provide an API key. You need to provide your API key via HTTP Basic Auth as username value."`

**To fix:**
1. Register at https://www.careerjet.com/partners/api
2. Get free API key (requires publisher account)
3. Use HTTP Basic Auth: `username=API_KEY, password=empty`
4. Terms require attribution/branding

**API params (from docs):**
- `locale_code`: `en_KE` for Kenya
- `keywords`: search terms
- `location`: `Kenya`, `Nairobi`, etc.
- `page`, `pagesize`: pagination

**Status:** Deferred until API key is obtained. Not blocking — 3 RSS feeds are enough for Phase 1.

---

### 5. MyJobMag Kenya — ❌ No RSS

- **URL:** `https://www.myjobmag.co.ke/feeds/`
- **HTTP Status:** 200
- **Content-Type:** `text/html; charset=UTF-8`

The `/feeds/` page is an HTML page listing job categories, not an XML feed. Confirms the original doc's assessment.

**Alternative:** HTTP scrape with CSS selectors, or check `/sitemap.xml` for URL discovery.

---

### 6. BrighterMonday — ❌ RSS Removed (410 Gone)

- **URL:** `https://www.brightermonday.co.ke/jobs.rss`
- **HTTP Status:** 410 (Gone)

The RSS endpoint has been deliberately removed. Cloudflare-protected, requires browser scraping.

---

### 7. Blog Nevine — ✅ RSS Working (filtered)

- **URL:** `https://blog.nevine.me/feeds/posts/default?alt=rss`
- **Content-Type:** `application/rss+xml` (Blogger Atom→RSS bridge)
- **Total posts:** 6,480 (25 per page, paginated)
- **Format:** RSS 2.0 via Blogger

**Fields available per item:**

| Field | Example | Notes |
|-------|---------|-------|
| `title` | `Internship \| Job Vacancies at M.P. Shah Hospital` | Sometimes prefixed with category |
| `link` | `https://blog.nevine.me/2025/06/client-relations-manager-at-mp-shah.html` | Direct URL |
| `pubDate` | `Mon, 25 May 2026 08:27:29 +0000` | RFC 2822 format |
| `category` | `Internship`, `Jobs` | Multiple, domain-namespaced |
| `description` | HTML excerpt with images | Heavier than WordPress, includes `<img>` tags |
| `author` | `noreply@blogger.com (Geoffrey Nevine)` | Author field (not dc:creator) |
| `guid` | `tag:blogger.com,1999:blog-...post-...` | Blogger-specific, stable |
| `updated` | `2026-05-25T11:27:29.280+03:00` | Atom timestamp (extra field) |
| `thumbnail` | URL | Image thumbnail (Blogger-specific) |

**Key difference from WordPress feeds:** Not a job board. General Kenyan lifestyle/career blog with 200+ categories (Jobs, Internship, career, plus health, beauty, cooking, etc.). Needs keyword filtering.

**n8n mapping:** RSS Feed Trigger → IF Node (keyword filter on title) → Code Node → Discord/Notion.

**Keyword filter (title match):** `job|vacancy|vacancies|internship|hiring|recruit|career|position|apply|graduate|attachment`

**Pagination:** Blogger supports `?max-results=25&start-index=1` for pagination. n8n RSS Trigger handles first page; cron reruns catch new posts.

---

## Phase 1 Implementation Plan (RSS-only)

**4 working feeds (3 WordPress RSS + 1 Blogger), all drop-in for n8n RSS Feed Trigger:**

```
OpenedCareer  → n8n RSS Trigger → Code Node → Discord webhook + Notion API
CareerPoint   → n8n RSS Trigger → Code Node → Discord webhook + Notion API
JobWeb        → n8n RSS Trigger → Code Node → Discord webhook + Notion API
Blog Nevine   → n8n RSS Trigger → IF (keyword filter) → Code Node → Discord webhook + Notion API
```

### Common RSS 2.0 Fields (all 3 feeds)

| Field | OpenedCareer | CareerPoint | JobWeb | Use in n8n |
|-------|:---:|:---:|:---:|------------|
| `title` | ✅ | ✅ | ✅ | Job title (parse JobWeb for company) |
| `link` | ✅ | ✅ | ✅ | URL property in Notion |
| `pubDate` | ✅ | ✅ | ✅ | Scraped At date |
| `category` | ✅ | ✅ | ❌ | Tags (multi-select) |
| `description` | ✅ | ✅ | ✅ | Short summary for Discord embed |
| `content:encoded` | ✅ | ❌ | ✅ | Full description for Notion Notes |
| `dc:creator` | ✅ | ✅ | ✅ | Metadata only |
| `guid` | ✅ | ✅ | ✅ | Dedup key |

### Code Node: Unified Parser

All 3 feeds use standard RSS 2.0. A single Code Node can handle all three with minor branching:

```javascript
// Unified RSS parser for all 3 feeds
const items = $input.all();
return items.map(item => {
  const json = item.json;
  const title = json.title || '';
  
  // JobWeb packs "Title at Company Location"
  let jobTitle = title, company = '', location = '';
  if (json.link?.includes('jobwebkenya.com')) {
    const parts = title.split(' at ');
    jobTitle = parts[0] || title;
    const remainder = parts[1] || '';
    // Try to split "Company Location"
    const locMatch = remainder.match(/(.*?)\s+(Nairobi|Mombasa|Kenya|Remote)/i);
    company = locMatch ? locMatch[1].trim() : remainder;
    location = locMatch ? locMatch[2] : '';
  }
  
  // Categories → Tags
  const categories = json.category || [];
  const tags = Array.isArray(categories) ? categories : [categories];
  
  return {
    json: {
      title: jobTitle.trim(),
      company: company.trim(),
      url: json.link,
      description: (json.description || '').replace(/<[^>]*>/g, '').substring(0, 300),
      tags: tags,
      source: json.link?.includes('openedcareer') ? 'openedcareer' 
            : json.link?.includes('careerpointkenya') ? 'careerpoint' 
            : 'jobweb',
      scraped_at: json.pubDate ? new Date(json.pubDate).toISOString() : new Date().toISOString(),
      guid: json.guid
    }
  };
});
```

### Dedup Strategy

Use `guid` as dedup key. n8n RSS Feed Trigger has built-in dedup, but for cross-feed dedup (same job on multiple sites), store `guid` in a Set or check Notion before inserting.
