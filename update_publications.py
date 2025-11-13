import requests, json

ORCID = "0000-0001-9059-8250"
API_URL = f"https://pub.orcid.org/v3.0/{ORCID}/works"

headers = {
    "Accept": "application/json"
}

r = requests.get(API_URL, headers=headers)
r.raise_for_status()
data = r.json()

works = data.get("group", [])

pubs = []
for w in works:
    summary = w.get("work-summary", [])[0]
    title = summary.get("title", {}).get("title", {}).get("value", "")
    journal = summary.get("journal-title", {}).get("value", "")
    year = summary.get("publication-date", {}).get("year", {}).get("value", "")
    doi = None
    external_ids = summary.get("external-ids", {}).get("external-id", [])
    for eid in external_ids:
        if eid.get("external-id-type") == "doi":
            doi = eid.get("external-id-value")
            break
    pubs.append({
        "title": title,
        "authors": "",  # ORCID API may not list authors cleanly
        "journal": journal,
        "year": year,
        "doi": doi
    })

# sort by year descending
pubs_sorted = sorted(pubs, key=lambda x: x["year"] or "0", reverse=True)

with open("_data/publications.json", "w") as f:
    json.dump(pubs_sorted, f, indent=2)

print(f"Wrote {len(pubs_sorted)} publications")
