# SOP: Notion Operations Hub

## Overview
Notion is the single source of truth. 25 databases under the Operations Hub page.

## Database Tiers (write in dependency order)
1. **Tier 1 (primaries):** Team Members, Community Members, Clients, Projects, Competitors, Newsletter Archive
2. **Tier 2 (extracts):** AI Updates, Content Ideas, EOD Reports, Leads, Influencers
3. **Tier 3 (events):** Meetings, Tasks, Invoices, Time Entries, Updates Log, Cold Email Campaigns, Outreach Activities
4. **Tier 4 (snapshots):** Calendar Daily Brief, Intel Briefings, Agent Logs, Growth Stats

## Write Rules
- Always query before creating (dedup by title/date/key)
- Never delete rows — soft-delete only (archive or set Status)
- Rich text cap: ~2000 chars in properties, overflow to page body
- Rate limit: max 3 requests/sec
- Batch 50 items with 1s pause between batches

## API Access
```python
import urllib.request, json, os
# curl is NOT installed — use Python urllib.request
# Notion API version: 2022-06-28
# Helper script: /opt/data/skills/productivity/notion/scripts/notion_api.py
```

## Operations Hub Page ID
`3493fa00-4c9d-8105-8a4e-ccdb8f4700c9`

## Key Database IDs
See `/vault/agents/HERMES.md` for full list.
