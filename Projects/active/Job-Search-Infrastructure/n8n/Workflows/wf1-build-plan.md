---
type: project
tags:
  - n8n
  - workflow
  - build-plan
  - job-search
  - wf1
aliases:
  - "WF1 Build Plan"
  - "Job Feed Scanner Build"
parent: "[[wf1-job-feed-scanner]]"
created: 2026-05-25
status: active
---

# WF1 Build Plan — Job Feed Scanner

> [!info] Part of [[Job Hunt Ops — Map of Content]]. Feeds into [[wf1-job-feed-scanner]] spec.

Sequential build. Each step is tested before moving to the next. No skipping ahead.

## Architecture (simplified)

```
Cron (4h)
  ↓
[RSS Fetch: OpenedCareer + CareerPoint + JobWeb + Blog Nevine]
  ↓
Code Node: Parse + Normalize (unified parser)
  ↓
IF Node: EEE keyword filter
  ↓
[Output: Discord webhook POST + Notion page create]
  ↓
Execution log
```

Blog Nevine gets an extra IF node before the parser (keyword filter on title since it's mixed content).

## Tasks

### Task 1: RSS Triggers + Raw Output

**Goal:** 4 RSS triggers running, verify what n8n actually receives from each feed.

**Steps:**
1. Open n8n at `http://localhost:5678`
2. Create new workflow: "WF1 - Job Feed Scanner"
3. Add 4 RSS Feed Trigger nodes:
   - `https://openedcareer.com/feed/`
   - `https://www.careerpointkenya.co.ke/feed/`
   - `https://jobwebkenya.com/feed/`
   - `https://blog.nevine.me/feeds/posts/default?alt=rss`
4. Connect each to a "Respond to Webhook" or just run manually
5. Execute each trigger, inspect the raw JSON output

**Test checkpoint:**
- [x] Each trigger returns items (4 HTTP Request nodes, not RSS Trigger — see rationale)
- [x] n8n stores raw XML strings when responseFormat is "xml", requiring regex parsing
- [x] 66 items parsed from 4 feeds on first successful run

**Expected output per item (n8n normalizes RSS to this):**
```json
{
  "title": "...",
  "link": "...",
  "pubDate": "...",
  "description": "...",
  "content:encoded": "...",
  "category": ["...", "..."],
  "dc:creator": "...",
  "guid": "...",
  "creator": "..."
}
```

---

### Task 2: Unified Code Node Parser

**Goal:** Single Code Node that takes RSS items from any source and outputs normalized job objects.

**Steps:**
1. Add Code Node after a Merge node (combines all 4 RSS triggers)
2. Write parser based on Feed Verification Report field mappings
3. Handle:
   - JobWeb title splitting: `"Title at Company Location"` → separate fields
   - Category → Tags (array normalization)
   - Source detection from URL domain
   - HTML stripping from description
   - pubDate → ISO timestamp
4. Run workflow, inspect parser output

**Test checkpoint:**
- [x] OpenedCareer items parse correctly
- [x] CareerPoint items parse correctly
- [x] JobWeb items parse correctly (title split: "Title at Company Location")
- [x] Blog Nevine items parse correctly
- [x] All items have: `title`, `company`, `url`, `source`, `scraped_at`, `tags`, `description`
- [x] Source detection uses link OR guid fallback (fixes "unknown" for guid-only items)

**Output shape (target):**
```json
{
  "title": "Information Technology Intern",
  "company": "Save the Children",
  "location": "Nairobi",
  "url": "https://openedcareer.com/...",
  "source": "openedcareer",
  "scraped_at": "2026-05-25T09:03:39.000Z",
  "tags": ["internship", "information-technology"],
  "description": "Looking to kick-start your career...",
  "type": "full-time",
  "salary": "Not listed"
}
```

---

### Task 3: Blog Nevine Keyword Filter

**Goal:** Filter out non-job content from Blog Nevine before it hits the parser.

**Steps:**
1. Add IF Node between Blog Nevine RSS trigger and the Merge node
2. Condition: title matches `job|vacancy|vacancies|internship|hiring|recruit|career|position|apply|graduate|attachment`
3. Run workflow, check: non-job posts (health, beauty, etc.) should be filtered out
4. Count: how many items pass vs total from Blog Nevine

**Test checkpoint:**
- [x] Non-job posts filtered by keyword regex: job|vacancy|internship|hiring|recruit|career|position|apply|graduate|attachment
- [x] Job-related posts pass through
- [x] 11 of 25 Blog Nevine items pass filter (rest are lifestyle/health content)

---

### Task 4: EEE Keyword Filter

**Goal:** Filter all merged items to only EEE-relevant jobs.

**Steps:**
1. Add Code Node after the parser
2. Implement keyword filter from WF1 spec:
   - EEE keywords: electrical, electronics, power, energy, solar, automation, controls, instrumentation, scada, plc, transmission, distribution, renewable, grid, substation, transformer, circuit, protection, relay, metering, telecom, signal, embedded, power systems, high voltage, low voltage, switchgear, generator, motor, inverter
   - Entry-level keywords: graduate, junior, entry, intern, trainee, 0-2 years, 1-2 years
3. Tag entry-level matches
4. Run workflow, inspect which items pass

**Test checkpoint:**
- [x] Two-tier keyword filter: Tier 1 (unambiguous EEE terms) + Tier 2 (broad terms need Tier 1 context in title)
- [x] Entry-level jobs tagged with "entry-level"
- [x] General admin/HR/marketing filtered out
- [x] "automation" moved to Tier 2 after matching too broadly
- [x] Typical run: 1-3 matches from 66 total items

**Note:** This is where we'll see if the feeds actually have EEE content. If zero items pass, the keyword list needs widening.

---

### Task 5: Insure Raw Output to Discord

**Goal:** See what the jobs look like in Discord before adding Notion complexity.

**Steps:**
1. Create a test webhook in any Discord channel (or use #agent-playground)
2. Add Code Node to build Discord embed payload
3. Add HTTP Request Node to POST to webhook URL
4. Run workflow end-to-end
5. Check Discord: does the embed look right? Title, company, location, score placeholder, link

**Test checkpoint:**
- [x] Embeds appear in #agents-playground
- [x] Title readable, company/location correct
- [x] Links work
- [x] Source label shown
- [x] Color: teal-green (0x00b894), no score coloring yet

**Embed shape:**
```
┌─────────────────────────────────────────────┐
│ Information Technology Intern          🔗   │
│                                             │
│ Company: Save the Children                  │
│ Location: Nairobi                           │
│ Score: --/100 (not scored yet)              │
│ Source: openedcareer                        │
│ Tags: internship, it                        │
│                                             │
│ via n8n • 2026-05-25T09:03:39Z             │
└─────────────────────────────────────────────┘
```

---

### Task 6: Wire Notion

**Goal:** Write filtered jobs to Notion Jobs DB.

**Steps:**
1. Store Notion API token as n8n Credential (Header Auth)
2. Store DB ID as workflow environment variable
3. Add Code Node to build Notion page payload (from WF1 spec)
4. Add HTTP Request to POST to `https://api.notion.com/v1/pages`
5. Add rate limit wait (350ms between writes)
6. Run workflow, check Notion DB for new entries

**Test checkpoint:**
- [ ] Jobs appear in Notion DB
- [ ] All fields populated correctly (Title, URL, Source, Status, Tags, Scraped At)
- [ ] Status is "new"
- [ ] No 401/400 errors
- [ ] Rate limiting works (no 429s)

---

### Task 7: End-to-End Test

**Goal:** Full pipeline running. RSS → parse → filter → Discord + Notion.

**Steps:**
1. Run workflow manually
2. Count: items fetched → items parsed → items filtered → items posted
3. Verify Discord embeds
4. Verify Notion entries
5. Check for errors in n8n execution log

**Test checkpoint:**
- [ ] Pipeline completes without errors
- [ ] Numbers make sense (not 0 items, not 1000 items)
- [ ] No duplicates between sources
- [ ] Discord and Notion match (same jobs in both)

---

### Task 8: FreeLLM Scoring (optional, after Task 7 works)

**Goal:** Add AI scoring to the pipeline.

**Steps:**
1. Add Split In Batches node (batch size 5)
2. Add HTTP Request to FreeLLM (`host.docker.internal:3001`)
3. Implement scoring prompt from WF1 spec
4. Parse response with fallback handling
5. Update Discord embeds with real scores
6. Update Notion with score

**Test checkpoint:**
- [ ] FreeLLM responds (not 401/timeout)
- [ ] Scores are reasonable (not all 50, not all 100)
- [ ] Discord embeds show real scores
- [ ] Notion Score field populated

---

## Task Dependencies

```
Task 1 (RSS triggers)
  ↓
Task 2 (parser)     ← depends on Task 1 output
  ↓
Task 3 (Blog filter) ← can run in parallel with Task 4
Task 4 (EEE filter)  ← depends on Task 2
  ↓
Task 5 (Discord)     ← depends on Task 4
  ↓
Task 6 (Notion)      ← depends on Task 4, can parallel with Task 5
  ↓
Task 7 (e2e test)    ← depends on Tasks 5 + 6
  ↓
Task 8 (scoring)     ← depends on Task 7
```

## Decisions

- **Sequential, not parallel.** Build one layer, test it, then add the next.
- **Discord before Notion.** Visual feedback is faster than querying an API.
- **Scoring last.** The pipeline works without it. Scoring is an enhancement.
- **Blog Nevine filtered at trigger level.** Don't merge unfiltered content into the main pipeline.

## Credentials Needed

| Credential | Where to get it | Status |
|------------|----------------|--------|
| Notion API token | `~/.zshrc.local` | ✅ Working |
| Notion Jobs DB ID | `36b88eb251618167b1c2cdc68c1ff906` | ✅ Created |
| Discord test webhook | Create in #agent-playground | ⏳ Need Discord bot setup |
| FreeLLM endpoint | `http://host.docker.internal:3001/v1` | ✅ Running |

## See Also

- [[wf1-job-feed-scanner]] — full node-by-node spec
- [[Feed-Verification-Report]] — live feed test results
- [[Kenyan Job Sites — Feeds & Scraping]] — site research
- [[Job Hunt Ops — Map of Content]] — project overview

## Dropped Sources

### OpenedCareer (Cloudflare Block)
- **Status:** Dropped — Cloudflare blocks HTTP requests from n8n
- **URL:** https://openedcareer.com/feed/
- **Action:** Retest later with stealth browser or alternative approach
- **Date:** 2026-05-26
