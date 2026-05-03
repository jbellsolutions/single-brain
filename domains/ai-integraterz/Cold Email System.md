# Cold Email System

## Architecture
Multi-agent squad system built on "forge" framework.

### Pipeline (per campaign)
1. **Strategy Squad** (Opus 4.7, 3-agent council) → campaign brief
2. **Research Squad** (Haiku 4.5, parallel ×10) → per-prospect signals
3. **Copy Squad** (Sonnet 4.6 + Haiku + 4 validators) → 3-email sequences
4. **SmartLead Squad** (deterministic) → campaign in DRAFTED state

### Daemons
- **slack_agent** — polls `#cold-email-control` every 8s
- **reply_loop** — polls inbox every 60s, auto-handles OOO/unsub/spam

## Active Campaigns (May 2026)
- `recruiters-power-partner-A` — ACTIVE, 1,577 leads
- `recruiters-direct-value-A` — ACTIVE, 259 leads
- 4 more DRAFTED (B variants + capstone)

## Voice Rules
- Cold email = conversation starter, NOT a pitch
- No URLs in emails 1-3
- Word limits: 125/150/125
- 25+ banned slop phrases
- Sign off: `-- Justin`

## Lead Sources
1. CSV upload via Slack
2. SmartLead Prospector (NL query → paid fetch)
3. [[Apify]] scrapers
4. Existing campaign re-processing

See: [[00 - Operations Hub]]


---
Tags: [[ai-integraterz]] [[cold-email]] [[smartlead]] [[pipeline]]