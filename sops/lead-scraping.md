# SOP: Lead Scraping & Enrichment

## Overview
Lead generation pipeline: Apify scrape → verify → personalize → SmartLead.

## Apify Setup
- Account: jbellsolutions-owner (SCALE plan)
- API key: `/opt/data/.env` → `APIFY_API_KEY`
- Best scrapers:
  - Google Maps: `compass/crawler-google-places` (385K users)
  - LinkedIn Profiles: `dev_fusion/Linkedin-Profile-Scraper` (56K users, includes emails)
  - Leads Finder: `code_crafter/leads-finder` ($1.50/1K leads with emails)

## Lead Scraping Flow
1. Define ICP: niche, geography, company size, title keywords
2. Choose scraper based on source (LinkedIn, Google Maps, Apollo alternative)
3. Run Apify actor with filters
4. Download results as CSV
5. Verify emails (ZeroBounce, NeverBounce, or similar)
6. Load into cold email pipeline OR directly to SmartLead

## Apify API
```python
import urllib.request, json

APIFY_KEY = os.environ.get('APIFY_API_KEY')

# Run an actor
req = urllib.request.Request(
    f"https://api.apify.com/v2/acts/{actor_id}/runs",
    data=json.dumps({"input": {...}}).encode(),
    headers={"Authorization": f"Bearer {APIFY_KEY}", "Content-Type": "application/json"},
    method="POST"
)

# Get results
req = urllib.request.Request(
    f"https://api.apify.com/v2/actor-runs/{run_id}/dataset/items?format=json",
    headers={"Authorization": f"Bearer {APIFY_KEY}"}
)
```

## Lead Quality Gates
- Must have: name, email, company
- Nice to have: title, LinkedIn URL, phone
- Reject: generic emails (info@, contact@, hello@)
- Reject: known bad domains (temporary email services)
