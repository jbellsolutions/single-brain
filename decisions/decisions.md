# Decisions Log

## 2026-05-02 — Hermes Operator Role Established

**Decision:** Hermes operates as full business operator for AI Integraterz. Authority to execute without asking permission.

**Context:** Justin onboarded Hermes with access to SmartLead, Notion, Apify, ConvertKit, Retell AI, and the cold email pipeline. Directive: "Don't ask, just do."

**Scope:**
- Cold email campaign monitoring and lead loading
- Notion database management (25 DBs)
- Content pipeline oversight
- Lead scraping and enrichment
- Growth tracking and influencer mapping
- SDR fleet management (when active)
- Ads operations (pending platform selection)

---

## 2026-05-02 — Vault as Shared Brain

**Decision:** Obsidian vault at `/opt/data/obsidian-vault` follows single-brain structure. Both Hermes and OpenClaw share it. All actions logged.

**Structure:** agents/, sops/, decisions/, daily-logs/, domains/

**Sync:** Git auto-commit every 30 minutes via cron.

---

## 2026-05-02 — Platform Architecture Locked

**Decision:** 
- Telegram = command center (chat + build)
- Slack = content delivery, file uploads, review queue, notifications
- Notion = single source of truth (all data)
- Railway = Content Flywheel engine
- VPS = automation backbone
- Obsidian vault = shared brain between agents


---
Tags: [[decisions]] [[architecture]] [[ai-integraterz]]