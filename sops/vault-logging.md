# SOP: Vault Logging Protocol

## Rule: Everything Sinks to the Vault

Every conversation, every action, every decision gets logged.

## What Gets Logged Where

### Daily Logs (`daily-logs/YYYY-MM-DD.md`)
- Morning health report (8AM cron)
- Status updates (4-hour cron)
- Any significant conversation outcomes
- Tasks completed or started
- Issues encountered

### Decisions (`decisions/decisions.md`)
- Major architectural choices
- New tool/system integrations
- Strategy changes
- Budget decisions
- Offer changes

### SOPs (`sops/`)
- New operational procedures discovered
- Updated workflows
- Troubleshooting guides learned from experience

### Domain Work (`domains/ai-integraterz/`)
- System documentation updates
- Schema changes
- Campaign performance snapshots
- Lead scrape results
- Content pipeline outputs

## Conversation Logging

After every significant Telegram or Slack conversation:
1. Summarize what was discussed/decided
2. Append to today's daily log
3. If a new SOP was discovered, create it in `sops/`
4. If a decision was made, log to `decisions/decisions.md`
5. If system state changed, update the relevant domain doc

## Auto-Sync
- Vault auto-commits every 30 minutes via cron
- Git push to `jbellsolutions/single-brain` repo
- Both Hermes and OpenClaw read from the same vault


---
Tags: [[sop]] [[vault]] [[logging]] [[protocol]]