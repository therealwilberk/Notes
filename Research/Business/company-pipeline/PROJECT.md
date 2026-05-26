---
type: research
tags: [business, kenya, pipeline, company-discovery, automation]
created: 2026-05-22
status: in-progress
parent: "[[MOCs/Business-Research-MOC.md]]"
---

# Company Discovery Pipeline
> Modular project: sieve real EE/solar/power companies in Kenya from multiple sources

## Status: STRUCTURE SETUP — NOT EXECUTED YET

## Context (Read This First)
Wilber is doing outbound job outreach. LinkedIn network exhausted — same companies, same people. Needs fresh company discovery OUTSIDE LinkedIn. Hunter.io/Skrapp.io don't work in Kenya.

**Goal:** Discover 500-800+ EE/solar/power/automation companies from non-LinkedIn sources. Filter out dead/fake/duplicate entries. Store clean data in Notion.

**Wilber's background:** EE grad MUT 2025, KenGen Olkaria + Kiambere (SCADA, HV, fault diagnostics), Python, solar-diesel optimization.

**Outreach playbook:** Already exists in Notion Job Search HQ — `35a88eb2-5161-80c5-9fe2-fbb2b18d079a` (playbook), `36488eb2-5161-8078-9ecf-f3ce340d52cf` (scripts). Don't recreate — this pipeline feeds INTO that system.

## Pipeline Architecture

```
Stage 1: SEARCH (parallel agents, each hits one source)
   → Write raw results to temp files (JSON)
   
Stage 2: ENRICHMENT (single agent)
   → Read all temp files
   → Deduplicate, validate, cross-reference
   → Write clean output to enriched/

Stage 3: NOTION WRITE (single agent or manual)
   → Read enriched output
   → Create pages in Notion database
   → Skip duplicates (check company_name exists)
```

## Data Sources (6 modules)

### Module 1: EPRA Licensed Contractors
- **Source:** PDF at `eeekenya.com/wp-content/uploads/2022/12/REGISTER-OF-LICENSED-ELECTRICAL-CONTRACTORS-AS-AT-5th-FEBRUARY-2021.pdf`
- **What:** 300+ companies with emails, phones, license numbers
- **Output:** `temp/01-epra.json`
- **Agent instruction:** Download PDF, extract company names, contact info, license class. Output JSON array.

### Module 2: Solar Africa 2026 Exhibitors
- **Source:** `expogr.com/solarafrica/exhibitor_list.php`
- **What:** 179 solar companies exhibiting at Solar Africa 2026
- **Output:** `temp/02-solar-africa.json`
- **Agent instruction:** Scrape exhibitor list. Extract company name, website, description, location.

### Module 3: ENF Solar Kenya
- **Source:** ENF Solar directory (search Kenya)
- **What:** Solar installers/developers with contacts
- **Output:** `temp/03-enf-solar.json`
- **Agent instruction:** Search ENF Solar for Kenya-based companies. Extract name, website, phone, email, location.

### Module 4: PPRA Contract Awards
- **Source:** `ppra.go.ke/contract-awards/`
- **What:** Companies winning government energy/electrical tenders
- **Output:** `temp/04-ppra.json`
- **Agent instruction:** Search/filter for electrical, solar, energy contracts. Extract company name, contract value, directors if available.

### Module 5: EEE Kenya Contractors
- **Source:** `eeekenya.com`
- **What:** Electrical engineering contractors with contacts
- **Output:** `temp/05-eee-kenya.json`
- **Agent instruction:** Scrape contractor listings. Extract company name, contact, location, specialization.

### Module 6: Google Maps Discovery
- **Source:** Google Maps searches
- **Searches:**
  - "solar installer Nairobi"
  - "electrical contractor Kenya"
  - "SCADA automation company Nairobi"
  - "power systems engineering Kenya"
  - "solar EPC company Kenya"
- **Output:** `temp/06-google-maps.json`
- **Agent instruction:** Search Google Maps, extract company name, address, phone, website, rating.

## Temp File Schema (all modules output this format)

```json
[
  {
    "company_name": "Example Solar Ltd",
    "source": "solar_africa_2026",
    "sector": "solar",
    "location": "Nairobi",
    "website": "https://example.com",
    "email": "info@example.com",
    "phone": "+254700000000",
    "contact_person": null,
    "linkedin_url": null,
    "raw_notes": "Exhibitor at Solar Africa 2026"
  }
]
```

## Notion Database Schema

**Database:** Company Pipeline (to be created in Job Search HQ workspace)

| Property | Type | Notes |
|---|---|---|
| Company Name | title | |
| Source | select | epra / solar_africa / enf / ppra / eee / google_maps |
| Sector | multi_select | solar / power_gen / automation / EPC / industrial |
| Location | select | Nairobi / Mombasa / Kisumu / Nakuru / Other |
| Website | url | |
| Email | email | |
| Phone | phone_number | |
| LinkedIn | url | |
| Contact Person | rich_text | |
| Status | select | new / verified / contacted / dead |
| Notes | rich_text | |

**Notion IDs:**
- Job Search HQ page: `35988eb2-5161-8004-988e-f5a8794c90c3`
- Company Pipeline database_id: `24bcf230-518f-4d40-8816-f7021342af55`
- Company Pipeline data_source_id: `3e77b704-4431-4705-99ab-18ef8eb01bb4`
- Token: `~/.zshrc` (export before ntn calls)

## File Locations
- Pipeline dir: `~/Documents/Text/Notes/Business-Research/company-pipeline/`
- Temp files: `company-pipeline/temp/`
- Enriched output: `company-pipeline/enriched/`
- Source playbook: `~/Documents/Text/Notes/Business-Research/05-company-discovery-playbook.md`
- Outreach playbook: Notion `35a88eb2-5161-80c5-9fe2-fbb2b18d079a`

## Execution Order
1. Create Notion database (one-time setup)
2. Run modules 1-6 in parallel (3 at a time, max concurrent)
3. Run enrichment agent (dedup + validate)
4. Write to Notion
5. Wilber reviews, marks status, starts outreach

## Agent Template (for search modules)

When executing, each agent receives:
```
CONTEXT: You are extracting companies from [SOURCE]. Output valid JSON to [OUTPUT_FILE].
SCHEMA: [{ company_name, source, sector, location, website, email, phone, contact_person, linkedin_url, raw_notes }]
RULES: 
- Only real, existing companies. Skip if unsure.
- Set sector based on what they do (solar/power_gen/automation/EPC/industrial).
- If no email/phone, set null — don't guess.
- Write output to the specified file.
```
