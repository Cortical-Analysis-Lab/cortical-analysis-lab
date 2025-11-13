import requests
import json
import os
from datetime import datetime

# ============================================================
# 🧠 Cortical Analysis Lab — ORCID → publications.json updater
# ============================================================

ORCID_ID = "0000-0001-9059-8250"
ORCID_API_URL = f"https://pub.orcid.org/v3.0/{ORCID_ID}/works"
HEADERS = {"Accept": "application/json"}

print("🔍 Fetching publication data from ORCID...")

# --- Fetch data from ORCID ---
response = requests.get(ORCID_API_URL, headers=HEADERS)
if response.status_code != 200:
    raise Exception(f"Failed to fetch ORCID data (status {response.status_code})")

data = response.json()
works = data.get("group", [])
publications = []

# --- Extract publication info ---
for item in works:
    work_summary = item.get("work-summary", [{}])[0]
    title = work_summary.get("title", {}).get("title", {}).get("value", "Untitled")
    journal = work_summary.get("journal-title", {}).get("value", "")
    year = work_summary.get("publication-date", {}).get("year", {}).get("value", "")
    doi = None

    # Try to extract DOI from external identifiers
    for ext_id in work_summary.get("external-ids", {}).get("external-id", []):
        if ext_id.get("external-id-type", "").lower() == "doi":
            doi = ext_id.get("external-id-value")
            break

    publications.append({
        "title": title,
        "journal": journal,
        "year": year,
        "doi": doi
    })

# --- Sort publications (newest first) ---
publications_sorted = sorted(publications, key=lambda x: x["year"] or "", reverse=True)

# --- Save to /data/publications.json ---
os.makedirs("data", exist_ok=True)
output_path = "data/publications.json"

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(publications_sorted, f, indent=2, ensure_ascii=False)

print(f"✅ {len(publications_sorted)} publications saved to {output_path}")
print(f"🕒 Last updated: {datetime.now().isoformat(timespec='seconds')}")
