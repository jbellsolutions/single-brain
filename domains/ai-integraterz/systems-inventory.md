# Systems Inventory — AI Integraterz

**Generated:** 2026-05-02
**All API keys stored in:** `/opt/data/.env`

---

## Notion
- **Access:** Python urllib.request (curl not installed)
- **API Version:** 2022-06-28
- **Key env var:** `NOTION_API_KEY`
- **Operations Hub:** `3493fa00-4c9d-8105-8a4e-ccdb8f4700c9`
- **Databases:** 25 total (see [[notion-schema]] for full property schemas)
- **Helper script:** `/opt/data/skills/productivity/notion/scripts/notion_api.py`

## SmartLead
- **CLI Path:** `/opt/data/home/.local/bin/smartlead`
- **MCP:** Configured in `/opt/data/config.yaml` (needs gateway restart to activate)
- **Key env var:** `SMARTLEAD_API_KEY`
- **Campaigns:** 17 total, 2 active (see [[smartlead-state]])
- **Mailboxes:** ~100 across ~29 domains
- **Cold Email Repo:** `/tmp/ai-integraterz-cold-email` (GitHub: `jbellsolutions/ai-integraterz-cold-email`)

## Apify
- **Access:** REST API via Python urllib.request
- **Key env var:** `APIFY_API_KEY`
- **Account:** jbellsolutions-owner
- **Plan:** SCALE
- **Best Scrapers:**
  - Google Maps: `compass/crawler-google-places` (385K users)
  - LinkedIn Profiles: `dev_fusion/Linkedin-Profile-Scraper` (56K users, includes emails)
  - Leads Finder: `code_crafter/leads-finder` ($1.50/1K leads)

## ConvertKit (Kit)
- **Access:** REST API
- **Key env var:** `CONVERTKIT_API_KEY`
- **Tags:** 12
- **Sequences:** 10
- **Broadcasts:** 7
- **Skill:** `convertkit` (Hermes skill)

## Retell AI
- **Access:** REST API
- **Key env var:** `RETELL_API_KEY`
- **Agents:** 21 (SMS Sales, Dental Outbound, Lead Qualification, etc.)
- **Phone Numbers:** 4
- **Skill:** `retell-ai` (Hermes skill)

## Content Flywheel
- **Hosting:** Railway (3 services: Worker, Browser-Runner, Dashboard)
- **Database:** Supabase
- **Queue:** Redis
- **Repo:** `jbellsolutions/ai-guy-flywheel`
- **Tools:** yt-dlp, ffmpeg (Shorts clipping), Unipile (LinkedIn/X), Typefully (X publishing)
- **Writing model:** Sonnet 4.5
- **Publishing:** Browser Use for non-API platforms (Substack, Facebook)

## GitHub
- **Account:** jbellsolutions
- **SSH Key:** ed25519 at `/opt/data/.ssh/`
- **Key repos:**
  - `ai-integraterz-cold-email` — Cold email pipeline
  - `ai-guy-flywheel` — Content Flywheel
  - `notion-super-agent-phase-3` — Notion automation
  - `single-brain` — Shared vault + agent orchestration

## VPS (This Machine)
- **Role:** Automation backbone — Hermes, cron jobs, scripts
- **Timezone:** US Eastern (EDT/EST)
- **Key paths:**
  - `/opt/data/.env` — All API keys
  - `/opt/data/config.yaml` — Hermes config
  - `/opt/data/skills/` — Hermes skills
  - `/opt/data/obsidian-vault/` — Shared brain vault
  - `/tmp/ai-integraterz-cold-email/` — Cold email repo
  - `/tmp/notion-super-agent-phase-3/` — Notion repo

## Cron Jobs

| Job | ID | Schedule | Delivers To |
|---|---|---|---|
| SmartLead → Notion Daily Sync | `13dd6ded3007` | Daily 8AM ET | Telegram + vault |
| Ops Checklist Reminder | `752557ddcabf` | Every 4h | Telegram + vault |
| Vault Auto-Sync | `a643d0095232` | Every 30min | Local (git commit/push) |

## Platform Roles

| Platform | Role |
|---|---|
| Telegram | Command center — Justin + Hermes build here |
| Slack | Content delivery, file uploads, review queue, notifications |
| Notion | Single source of truth — all 25 databases |
| Obsidian Vault | Shared brain between agents (git-synced) |
| Railway | Content Flywheel engine |
| VPS | Automation backbone |


---
Tags: [[ai-integraterz]] [[systems]] [[inventory]] [[api-keys]]