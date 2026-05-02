# SOP: AGI-1 Framework Operations

## Overview
AGI-1 is the self-healing, self-learning layer across all repos and agents. Everything flows through Notion and the vault.

## Daily Sync (Automated)
- **Cron runs daily** — scans all registered repos
- Pulls healing patterns, observations, insights
- Syncs to Notion (5 databases)
- Writes vault report to `domains/agi-1/daily-report-YYYY-MM-DD.md`

## How Healing Works
1. Agent encounters an error
2. Checks patterns.json for known fix (regex match)
3. If confidence ≥0.6: auto-applies fix
4. Verifies fix worked → updates confidence score
5. At ≥0.8 confidence + 5 fixes → eligible for genome promotion

## How Learning Works
1. Observations logged during sessions (instruction_ignored, repeated_error, etc.)
2. Every N sessions → learner processes observations into insights
3. Insights with ≥0.7 confidence + evidence → applied automatically
4. Changes logged in evolution.json

## How Genome Works
1. Genome is the shared knowledge bank across all repos
2. High-confidence patterns get promoted to genome
3. New repos inherit genome patterns on first `/agi-sync`
4. Low-performing patterns get demoted/removed

## Key Scripts
- Sync engine: `/opt/data/obsidian-vault/scripts/agi1_sync.py`
- Graph analyzer: `/opt/data/obsidian-vault/scripts/vault_graph_analyzer.py`

## Registered Repos
- `/tmp/ai-integraterz-cold-email` (26 patterns, 9 observations)
- `/tmp/notion-super-agent-phase-3`
- `/tmp/agi-1` (framework source)

## Adding a New Repo
1. Add path to REPO_PATHS in agi1_sync.py
2. Scaffold `.agi1/` directory (copy templates from agi-1 repo)
3. Next sync auto-discovers data
