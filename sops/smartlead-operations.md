# SOP: SmartLead Campaign Operations

## Overview
SmartLead is the cold email sending platform. Campaigns are managed via CLI + MCP.

## Daily Monitoring (8AM ET cron)
1. Pull campaign stats: `smartlead campaigns list --format json`
2. Check inbox: `smartlead inbox unread --format json`
3. Sync to Notion Cold Email Campaigns DB
4. Alert on: bounce rate >5%, unread replies >12h old, campaigns running low on leads

## Loading New Leads
1. Receive CSV (Slack upload) or scrape via Apify
2. Validate: required fields = name, email, company, title
3. Verify emails (ZeroBounce or similar)
4. Run through cold email pipeline (Strategy → Research → Copy → SmartLead Squad)
5. Campaign lands in DRAFTED → operator reviews → schedule

## Reply Handling
- Auto-handled: OOO, unsubscribe, spam
- Human approval required: positive replies, objections, questions
- All replies post to Slack `#cold-email-replies`

## Voice Rules
- No URLs in emails 1-3
- Word limits: 125/150/125 per email
- 25+ banned slop phrases
- Sign off: `-- Justin`
- Three offers: Power-Partner, Direct-Value, Capstone

## Key Commands
```bash
export PATH=/opt/data/home/.local/bin:$PATH
export SMARTLEAD_API_KEY=<from /opt/data/.env>

smartlead campaigns list [--format json]
smartlead inbox unread [--format json]
smartlead leads list --campaign-id <ID>
smartlead leads export --campaign-id <ID> --output leads.csv
smartlead analytics overview --from YYYY-MM-DD --to YYYY-MM-DD
```


---
Tags: [[sop]] [[smartlead]] [[cold-email]] [[monitoring]]