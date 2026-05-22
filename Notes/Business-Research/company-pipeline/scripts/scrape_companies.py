#!/usr/bin/env python3
"""
Company Discovery Pipeline — Kenya EE/Solar/Power Companies
Scrapes 5 sources, outputs JSON to ../temp/
"""
import argparse
import json
import logging
import os
import re
import subprocess
import sys
import time
from pathlib import Path

# Auto-install deps
def ensure_deps():
    missing = []
    for mod in ['requests', 'bs4']:
        try:
            __import__(mod)
        except ImportError:
            pkg = 'beautifulsoup4' if mod == 'bs4' else mod
            missing.append(pkg)
    if missing:
        print(f"Installing missing deps: {missing}")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q'] + missing)

ensure_deps()

import requests
from bs4 import BeautifulSoup
import subprocess

# Logging
SCRIPT_DIR = Path(__file__).parent
LOG_FILE = SCRIPT_DIR / "pipeline.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
log = logging.getLogger(__name__)

TEMP_DIR = SCRIPT_DIR.parent / "temp"
TEMP_DIR.mkdir(exist_ok=True)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
]

def get_session():
    s = requests.Session()
    s.headers.update({
        "User-Agent": USER_AGENTS[0],
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    })
    return s

def fetch(url, session=None, retries=3, timeout=30):
    """Fetch URL with retry + exponential backoff."""
    s = session or get_session()
    for attempt in range(retries):
        try:
            s.headers["User-Agent"] = USER_AGENTS[attempt % len(USER_AGENTS)]
            resp = s.get(url, timeout=timeout, allow_redirects=True)
            resp.raise_for_status()
            return resp
        except Exception as e:
            log.warning(f"Attempt {attempt+1}/{retries} failed for {url}: {e}")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
    log.error(f"All {retries} attempts failed for {url}")
    return None

def save_json(data, filename):
    path = TEMP_DIR / filename
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    log.info(f"Saved {len(data)} companies to {path}")

def is_valid_output(filename):
    path = TEMP_DIR / filename
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text())
        return isinstance(data, list) and len(data) > 0
    except:
        return False

def dedup(companies):
    seen = set()
    out = []
    for c in companies:
        key = c.get("company_name", "").strip().lower()
        if key and key not in seen:
            seen.add(key)
            out.append(c)
    return out

# ─── MODULE 1: EPRA Licensed Contractors ───
def scrape_epra():
    log.info("=== Module 1: EPRA Licensed Contractors ===")
    pdf_url = "https://www.eeekenya.com/wp-content/uploads/2022/12/REGISTER-OF-LICENSED-ELECTRICAL-CONTRACTORS-AS-AT-5th-FEBRUARY-2021.pdf"
    pdf_path = TEMP_DIR / "epra-register.pdf"
    
    # Download PDF
    if not pdf_path.exists():
        log.info("Downloading EPRA PDF...")
        resp = fetch(pdf_url)
        if not resp:
            log.error("Failed to download EPRA PDF")
            return []
        pdf_path.write_bytes(resp.content)
        log.info(f"Downloaded {len(resp.content)} bytes")
    
    # Parse PDF
    log.info("Parsing EPRA PDF...")
    companies = []
    result = subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), "-"],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode != 0:
        log.error(f"pdftotext failed: {result.stderr}")
        return []
    
    full_text = result.stdout
    pages = full_text.split("\f")  # Form feed = page break
    
    for page_num, text in enumerate(pages):
        lines = text.strip().split("\n")
        
        for line in lines:
            line = line.strip()
            if not line or len(line) < 10:
                continue
            # Skip headers/footers
            if any(skip in line.lower() for skip in ["register of licensed", "page ", "class a", "class b", "class c", "no.", "name of", "license"]):
                continue
            
            # Try to extract: license_no, company_name, location, phone
            # Format varies but typically: number, name, location, phone
            parts = [p.strip() for p in re.split(r'\s{2,}|\t', line) if p.strip()]
            if len(parts) >= 2:
                company_name = parts[1] if len(parts) > 1 else parts[0]
                # Clean up
                company_name = re.sub(r'^\d+[\.\)]\s*', '', company_name).strip()
                if len(company_name) < 3:
                    continue
                
                # Extract phone if present
                phone = None
                for p in parts:
                    if re.search(r'0\d{8,9}|\+254\d{8,9}', p):
                        phone = re.search(r'(0\d{8,9}|\+254\d{8,9})', p).group()
                        break
                
                # Extract email if present
                email = None
                for p in parts:
                    if '@' in p:
                        email = p.strip()
                        break
                
                location = parts[2] if len(parts) > 2 else None
                
                companies.append({
                    "company_name": company_name,
                    "source": "epra",
                    "sector": "EPC",
                    "location": location,
                    "website": None,
                    "email": email,
                    "phone": phone,
                    "contact_person": None,
                    "linkedin_url": None,
                    "raw_notes": f"EPRA licensed contractor, page {page_num+1}"
                })
    
    companies = dedup(companies)
    log.info(f"EPRA: extracted {len(companies)} companies")
    return companies

# ─── MODULE 2: Solar Africa 2026 Exhibitors ───
def scrape_solar_africa():
    log.info("=== Module 2: Solar Africa 2026 Exhibitors ===")
    url = "https://expogr.com/solarafrica/exhibitor_list.php"
    session = get_session()
    companies = []
    
    resp = fetch(url, session)
    if not resp:
        log.error("Failed to fetch Solar Africa exhibitor list")
        return []
    
    soup = BeautifulSoup(resp.text, "html.parser")
    
    # Find exhibitor entries — look for table rows or card elements
    # Try multiple selectors
    rows = soup.find_all("tr")
    if not rows:
        rows = soup.find_all("div", class_=re.compile(r"exhibitor|company|card", re.I))
    if not rows:
        rows = soup.find_all("li")
    
    for row in rows:
        text = row.get_text(" ", strip=True)
        if len(text) < 5:
            continue
        
        # Skip header rows
        if any(skip in text.lower() for skip in ["exhibitor", "company name", "country", "product"]):
            continue
        
        # Extract link if present
        link = row.find("a")
        website = None
        company_name = text
        if link:
            href = link.get("href", "")
            if href and "http" in href:
                website = href
            link_text = link.get_text(strip=True)
            if link_text and len(link_text) > 2:
                company_name = link_text
        
        # Clean company name — take first meaningful part
        parts = [p.strip() for p in text.split("  ") if p.strip()]
        if parts:
            company_name = parts[0]
        
        if len(company_name) < 3:
            continue
        
        companies.append({
            "company_name": company_name,
            "source": "solar_africa",
            "sector": "solar",
            "location": "Kenya",
            "website": website,
            "email": None,
            "phone": None,
            "contact_person": None,
            "linkedin_url": None,
            "raw_notes": "Solar Africa 2026 exhibitor"
        })
    
    companies = dedup(companies)
    log.info(f"Solar Africa: extracted {len(companies)} companies")
    return companies

# ─── MODULE 3: ENF Solar Kenya ───
def scrape_enf_solar():
    log.info("=== Module 3: ENF Solar Kenya ===")
    # ENF Solar directory pages for Kenya
    base_url = "https://www.enfsolar.com/directory/list/1/1?country=KE"
    session = get_session()
    companies = []
    page = 1
    
    while page <= 5:  # Max 5 pages
        url = f"https://www.enfsolar.com/directory/list/1/{page}?country=KE"
        log.info(f"Fetching ENF page {page}...")
        resp = fetch(url, session)
        if not resp:
            break
        
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Find company entries
        entries = soup.find_all("div", class_=re.compile(r"company|item|row", re.I))
        if not entries:
            entries = soup.find_all("tr")
        
        if not entries:
            log.info(f"No entries found on page {page}, stopping")
            break
        
        for entry in entries:
            text = entry.get_text(" ", strip=True)
            if len(text) < 5:
                continue
            
            link = entry.find("a")
            company_name = None
            website = None
            
            if link:
                company_name = link.get_text(strip=True)
                href = link.get("href", "")
                if href and "enfsolar.com" in href:
                    # It's an ENF profile link, not company website
                    pass
            
            if not company_name:
                parts = [p.strip() for p in text.split("  ") if p.strip() and len(p.strip()) > 2]
                if parts:
                    company_name = parts[0]
            
            if not company_name or len(company_name) < 3:
                continue
            
            # Skip non-company entries
            if any(skip in company_name.lower() for skip in ["page", "next", "previous", "home", "search"]):
                continue
            
            # Extract phone/email from text
            phone = None
            email = None
            phone_match = re.search(r'(0\d{8,9}|\+254\d{8,9}|\d{3}[-\s]\d{3}[-\s]\d{4})', text)
            if phone_match:
                phone = phone_match.group()
            email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
            if email_match:
                email = email_match.group()
            
            companies.append({
                "company_name": company_name,
                "source": "enf_solar",
                "sector": "solar",
                "location": "Kenya",
                "website": website,
                "email": email,
                "phone": phone,
                "contact_person": None,
                "linkedin_url": None,
                "raw_notes": f"ENF Solar directory, page {page}"
            })
        
        # Check for next page
        next_link = soup.find("a", string=re.compile(r"next|›|»", re.I))
        if not next_link:
            break
        
        page += 1
        time.sleep(1)
    
    companies = dedup(companies)
    log.info(f"ENF Solar: extracted {len(companies)} companies")
    return companies

# ─── MODULE 4: PPRA Contract Awards ───
def scrape_ppra():
    log.info("=== Module 4: PPRA Contract Awards ===")
    url = "https://ppra.go.ke/contract-awards/"
    session = get_session()
    companies = []
    
    resp = fetch(url, session)
    if not resp:
        log.error("Failed to fetch PPRA contract awards")
        return []
    
    soup = BeautifulSoup(resp.text, "html.parser")
    
    # Find contract award entries
    entries = soup.find_all("tr")
    if not entries:
        entries = soup.find_all("div", class_=re.compile(r"contract|award|entry|row", re.I))
    if not entries:
        entries = soup.find_all("li")
    
    for entry in entries:
        text = entry.get_text(" ", strip=True)
        if len(text) < 10:
            continue
        
        # Filter for energy/electrical related
        keywords = ["solar", "electrical", "energy", "power", "transformer", "substations", 
                     "grid", "inverter", "photovoltaic", "lighting", "generator", "hv", "mv"]
        if not any(kw in text.lower() for kw in keywords):
            continue
        
        link = entry.find("a")
        company_name = None
        if link:
            company_name = link.get_text(strip=True)
        
        if not company_name:
            # Try to extract from text — usually first meaningful part
            parts = [p.strip() for p in re.split(r'\s{2,}|\t', text) if p.strip()]
            if parts:
                company_name = parts[0]
        
        if not company_name or len(company_name) < 3:
            continue
        
        companies.append({
            "company_name": company_name,
            "source": "ppra",
            "sector": "EPC",
            "location": None,
            "website": None,
            "email": None,
            "phone": None,
            "contact_person": None,
            "linkedin_url": None,
            "raw_notes": f"PPRA contract award - {text[:100]}"
        })
    
    companies = dedup(companies)
    log.info(f"PPRA: extracted {len(companies)} companies")
    return companies

# ─── MODULE 5: EEE Kenya ───
def scrape_eee_kenya():
    log.info("=== Module 5: EEE Kenya ===")
    url = "https://eeekenya.com"
    session = get_session()
    companies = []
    
    # Try main page and common contractor list pages
    urls_to_try = [
        "https://eeekenya.com",
        "https://eeekenya.com/contractors",
        "https://eeekenya.com/members",
        "https://eeekenya.com/member-directory",
        "https://eeekenya.com/about",
    ]
    
    for page_url in urls_to_try:
        resp = fetch(page_url, session)
        if not resp:
            continue
        
        soup = BeautifulSoup(resp.text, "html.parser")
        text = resp.text
        
        # Look for company names in various elements
        entries = soup.find_all("div", class_=re.compile(r"member|company|contractor|listing", re.I))
        if not entries:
            entries = soup.find_all("li")
        if not entries:
            entries = soup.find_all("tr")
        
        for entry in entries:
            entry_text = entry.get_text(" ", strip=True)
            if len(entry_text) < 5 or len(entry_text) > 500:
                continue
            
            link = entry.find("a")
            company_name = None
            website = None
            
            if link:
                company_name = link.get_text(strip=True)
                href = link.get("href", "")
                if href and "http" in href and "eeekenya" not in href:
                    website = href
            
            if not company_name:
                parts = [p.strip() for p in entry_text.split("  ") if p.strip() and len(p.strip()) > 2]
                if parts:
                    company_name = parts[0]
            
            if not company_name or len(company_name) < 3:
                continue
            
            # Skip navigation/footer items
            if any(skip in company_name.lower() for skip in ["home", "about", "contact", "menu", "copyright", "privacy"]):
                continue
            
            phone = None
            email = None
            phone_match = re.search(r'(0\d{8,9}|\+254\d{8,9})', entry_text)
            if phone_match:
                phone = phone_match.group()
            email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', entry_text)
            if email_match:
                email = email_match.group()
            
            companies.append({
                "company_name": company_name,
                "source": "eee_kenya",
                "sector": "EPC",
                "location": None,
                "website": website,
                "email": email,
                "phone": phone,
                "contact_person": None,
                "linkedin_url": None,
                "raw_notes": f"EEE Kenya listing ({page_url})"
            })
        
        if companies:
            break  # Found data, stop trying other pages
        
        time.sleep(1)
    
    companies = dedup(companies)
    log.info(f"EEE Kenya: extracted {len(companies)} companies")
    return companies

# ─── MAIN ───
SOURCES = {
    "epra": ("01-epra.json", scrape_epra),
    "solar_africa": ("02-solar-africa.json", scrape_solar_africa),
    "enf": ("03-enf-solar.json", scrape_enf_solar),
    "ppra": ("04-ppra.json", scrape_ppra),
    "eee": ("05-eee-kenya.json", scrape_eee_kenya),
}

def main():
    parser = argparse.ArgumentParser(description="Scrape Kenyan company data")
    parser.add_argument("--source", default="all", help="Source to scrape (epra/solar_africa/enf/ppra/eee/all)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be scraped without scraping")
    parser.add_argument("--force", action="store_true", help="Re-scrape even if output exists")
    args = parser.parse_args()
    
    if args.source == "all":
        targets = SOURCES
    else:
        if args.source not in SOURCES:
            print(f"Unknown source: {args.source}. Options: {', '.join(SOURCES.keys())}")
            sys.exit(1)
        targets = {args.source: SOURCES[args.source]}
    
    if args.dry_run:
        print("DRY RUN — would scrape:")
        for name, (outfile, _) in targets.items():
            exists = is_valid_output(outfile)
            status = "EXISTS (would skip)" if exists else "MISSING"
            print(f"  {name:15} → {outfile:25} [{status}]")
        return
    
    results = {}
    
    for name, (outfile, func) in targets.items():
        if not args.force and is_valid_output(outfile):
            log.info(f"Skipping {name} — {outfile} already exists with data")
            data = json.loads((TEMP_DIR / outfile).read_text())
            results[name] = {"count": len(data), "errors": 0, "skipped": True}
            continue
        
        log.info(f"Starting {name}...")
        start = time.time()
        try:
            data = func()
            save_json(data, outfile)
            elapsed = time.time() - start
            results[name] = {"count": len(data), "errors": 0, "elapsed": f"{elapsed:.1f}s"}
            log.info(f"Completed {name}: {len(data)} companies in {elapsed:.1f}s")
        except Exception as e:
            elapsed = time.time() - start
            log.error(f"Failed {name}: {e}")
            results[name] = {"count": 0, "errors": 1, "elapsed": f"{elapsed:.1f}s", "error": str(e)}
    
    # Summary table
    print("\n" + "="*60)
    print(f"{'SOURCE':15} {'COMPANIES':>10} {'STATUS':>10} {'TIME':>10}")
    print("-"*60)
    total = 0
    for name, r in results.items():
        status = "SKIPPED" if r.get("skipped") else ("ERROR" if r.get("errors") else "OK")
        count = r["count"]
        total += count
        elapsed = r.get("elapsed", "-")
        print(f"{name:15} {count:>10} {status:>10} {elapsed:>10}")
    print("-"*60)
    print(f"{'TOTAL':15} {total:>10}")
    print("="*60)

if __name__ == "__main__":
    main()
