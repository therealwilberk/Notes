#!/usr/bin/env python3
"""Parse EPRA licensed contractors PDF using pdftotext. Outputs clean JSON."""
import json
import re
import subprocess
import sys
from pathlib import Path

PDF = Path(__file__).parent.parent / "temp" / "epra-register.pdf"
OUT = Path(__file__).parent.parent / "temp" / "01-epra.json"

def parse():
    result = subprocess.run(
        ["pdftotext", "-layout", str(PDF), "-"],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode != 0:
        print(f"pdftotext failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    full_text = result.stdout
    pages = full_text.split("\f")

    companies = []
    current = None

    for page in pages:
        lines = page.split("\n")
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            # Match numbered entries: "1.    Company Name    Class X    EPRA/EC/XXXX    Location    Phone"
            m = re.match(
                r'^\s*(\d+)\.\s+(.+?)\s+(Class\s+[A-Z]-?\d?)\s+(EPRA/EC/\d+)\s+(\w[\w\s]*?)\s+'
                r'([\d/+*]+)\s+(.+?)\s+(Class\s+[A-Z]-?\d?)\s+(EPRA/EW/\d+|\d{4,6})\s*$',
                stripped
            )
            if m:
                # Save previous entry
                if current:
                    companies.append(current)

                sn, biz_name, biz_class, biz_lic, location, phone, electrician, elec_class, elec_lic = m.groups()
                biz_name = biz_name.strip()
                location = location.strip()
                phone = phone.strip()

                # Clean phone — fix masked numbers
                phone_clean = phone.replace("*", "")

                current = {
                    "company_name": biz_name,
                    "source": "epra",
                    "sector": "EPC",
                    "location": location if location else None,
                    "website": None,
                    "email": None,
                    "phone": phone_clean if phone_clean and len(phone_clean) >= 9 else None,
                    "contact_person": electrician.strip(),
                    "linkedin_url": None,
                    "raw_notes": f"EPRA {biz_class.strip()}, License {biz_lic.strip()}"
                }
                continue

            # Check for continuation lines (company name wraps, e.g. "Limited" on next line)
            if current and not re.match(r'^\s*\d+\.', stripped):
                # Might be continuation of company name or electrician name
                # Check if it looks like a company suffix
                if re.match(r'^(Limited|Ltd|Ltd\.|Enterprises|Engineering|Company|Services|Solutions|Systems|Works|Agency|Agencies|Ventures|Power|Electrical|Communications|Tech|Solar|Energy)\b', stripped, re.I):
                    current["company_name"] = current["company_name"] + " " + stripped.split()[0]
                continue

        # Save last entry of page
        if current:
            companies.append(current)
            current = None

    # Dedup
    seen = set()
    deduped = []
    for c in companies:
        key = c["company_name"].strip().lower()
        if key not in seen:
            seen.add(key)
            deduped.append(c)

    with open(OUT, "w") as f:
        json.dump(deduped, f, indent=2, ensure_ascii=False)

    print(f"Parsed {len(deduped)} companies from EPRA PDF")
    print(f"Saved to {OUT}")
    # Show sample
    for c in deduped[:3]:
        print(f"  {c['company_name']:40} | {c['location']:12} | {c['phone'] or 'no phone':15} | {c['contact_person']}")

if __name__ == "__main__":
    parse()
