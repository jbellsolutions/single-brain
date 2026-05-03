#!/usr/bin/env python3
"""
AGI-1 Sync Engine — Pulls healing/learning data from repos → Notion + Obsidian vault.

Scans registered repos for .claude/ or .agi1/ directories,
reads healing patterns, observations, insights, and genome data,
then syncs to Notion databases and writes a vault report.

Usage:
    PYTHONPATH=/opt/data/home/.local/lib/python python3 agi1_sync.py [--report-only]

Environment:
    NOTION_API_KEY — from /opt/data/.env
    OBSIDIAN_VAULT_PATH — defaults to /opt/data/obsidian-vault
"""

import json
import os
import sys
import glob
import urllib.request
import urllib.error
import time
from datetime import datetime, timezone
from pathlib import Path

# ──────────────────────────────────────────────
# Config
# ──────────────────────────────────────────────
VAULT_PATH = os.environ.get('OBSIDIAN_VAULT_PATH', '/opt/data/obsidian-vault')

# Notion DB IDs
NOTION_DBS = {
    "healing_patterns":      "3543fa00-4c9d-8137-b4d5-f59e9acf6d23",
    "learning_observations": "3543fa00-4c9d-81a6-9d08-fe6eb642d045",
    "learning_insights":     "3543fa00-4c9d-817d-9557-cf322fa44ba0",
    "genome_changelog":      "3543fa00-4c9d-8156-a614-e83a0fe1f022",
    "agent_health":          "3543fa00-4c9d-81e2-914d-c25a1d11f6bd",
}

# Repos to scan (add more as you onboard repos)
REPO_PATHS = [
    "/tmp/ai-integraterz-cold-email",
    "/tmp/notion-super-agent-phase-3",
    "/tmp/agi-1",
]

# Also scan home dirs for genome
GENOME_PATHS = [
    os.path.expanduser("~/.claude/agi-1-genome"),
    "/opt/data/.claude/agi-1-genome",
]

def load_env():
    env = {}
    with open('/opt/data/.env') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                env[k.strip()] = v.strip()
    return env

def notion_api(key, method, endpoint, body=None):
    url = f"https://api.notion.com{endpoint}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": f"Bearer {key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    })
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err = json.loads(e.read()) if e.fp else {}
        return {"error": True, "status": e.code, "message": err.get("message", str(e))}

# ──────────────────────────────────────────────
# Scanners
# ──────────────────────────────────────────────

def scan_repo_healing(repo_path):
    """Scan a repo for healing data."""
    patterns = []
    history = []
    
    for subdir in ['.claude/healing', '.agi1/healing']:
        patterns_file = os.path.join(repo_path, subdir, 'patterns.json')
        history_file = os.path.join(repo_path, subdir, 'history.json')
        
        if os.path.exists(patterns_file):
            with open(patterns_file) as f:
                data = json.load(f)
                patterns.extend(data.get('patterns', []))
        
        if os.path.exists(history_file):
            with open(history_file) as f:
                data = json.load(f)
                history.extend(data.get('entries', data.get('history', [])))
    
    return patterns, history

def scan_repo_learning(repo_path):
    """Scan a repo for learning data."""
    observations = []
    insights = []
    
    for subdir in ['.claude/learning', '.agi1/learning']:
        obs_file = os.path.join(repo_path, subdir, 'observations.json')
        ins_file = os.path.join(repo_path, subdir, 'insights.json')
        
        if os.path.exists(obs_file):
            with open(obs_file) as f:
                data = json.load(f)
                observations.extend(data.get('observations', []))
        
        if os.path.exists(ins_file):
            with open(ins_file) as f:
                data = json.load(f)
                insights.extend(data.get('insights', []))
    
    return observations, insights

def scan_genome():
    """Scan for genome data."""
    for gpath in GENOME_PATHS:
        genome_file = os.path.join(gpath, 'genome.json')
        if os.path.exists(genome_file):
            with open(genome_file) as f:
                return json.load(f)
    return None

def scan_repo_health(repo_path):
    """Get health metrics for a repo."""
    repo_name = os.path.basename(repo_path)
    patterns, history = scan_repo_healing(repo_path)
    observations, insights = scan_repo_learning(repo_path)
    
    # Count today's activity
    today = datetime.now().strftime('%Y-%m-%d')
    today_heals = sum(1 for h in history if h.get('timestamp', '').startswith(today))
    today_obs = sum(1 for o in observations if o.get('timestamp', '').startswith(today))
    
    # Heal success rate
    total_fixes = sum(p.get('times_fixed', 0) for p in patterns)
    total_seen = sum(p.get('times_seen', 0) for p in patterns)
    success_rate = total_fixes / max(total_seen, 1)
    
    # Genome-ready patterns
    genome_ready = sum(1 for p in patterns 
                       if p.get('confidence', 0) >= 0.8 and p.get('times_fixed', 0) >= 5)
    
    # Check for state.json (session count)
    session_count = 0
    for state_path in ['.agent/state.json', '.claude/state.json', '.agi1/state.json']:
        full_path = os.path.join(repo_path, state_path)
        if os.path.exists(full_path):
            with open(full_path) as f:
                state = json.load(f)
                session_count = state.get('session_count', 0)
                break
    
    return {
        "repo": repo_name,
        "patterns_active": len(patterns),
        "heals_today": today_heals,
        "heal_success_rate": success_rate,
        "observations_today": today_obs,
        "insights_generated": len(insights),
        "genome_contributions": genome_ready,
        "session_count": session_count,
    }

# ──────────────────────────────────────────────
# Notion Sync
# ──────────────────────────────────────────────

def sync_health_to_notion(notion_key, health_data, repo_name):
    """Write daily health row to Notion."""
    today = datetime.now().strftime('%Y-%m-%d')
    
    props = {
        "Report": {"title": [{"text": {"content": f"{repo_name} — {today}"}}]},
        "Repo": {"rich_text": [{"text": {"content": repo_name}}]},
        "Date": {"date": {"start": today}},
        "Patterns Active": {"number": health_data.get("patterns_active", 0)},
        "Heals Today": {"number": health_data.get("heals_today", 0)},
        "Heal Success Rate": {"number": health_data.get("heal_success_rate", 0)},
        "Observations Today": {"number": health_data.get("observations_today", 0)},
        "Insights Generated": {"number": health_data.get("insights_generated", 0)},
        "Genome Contributions": {"number": health_data.get("genome_contributions", 0)},
        "Session Count": {"number": health_data.get("session_count", 0)},
        "Status": {"select": {"name": "Healthy"}},
    }
    
    result = notion_api(notion_key, "POST", "/v1/pages", {
        "parent": {"database_id": NOTION_DBS["agent_health"]},
        "properties": props
    })
    return not result.get("error")

def sync_new_observations_to_notion(notion_key, observations, repo_name):
    """Sync unprocessed observations to Notion."""
    count = 0
    for obs in observations:
        if obs.get('synced_to_notion'):
            continue
        
        props = {
            "Observation": {"title": [{"text": {"content": obs.get('subject', obs.get('id', 'unknown'))[:100]}}]},
            "Repo": {"rich_text": [{"text": {"content": repo_name}}]},
            "Evidence": {"rich_text": [{"text": {"content": obs.get('evidence', '')[:2000]}}]},
            "Processed": {"checkbox": False},
        }
        
        obs_type = obs.get('type', '')
        valid_types = ['instruction_ignored', 'repeated_error', 'skill_unused', 'skill_popular',
                       'agent_failure', 'test_regression', 'pattern_promoted', 'pattern_failed',
                       'correction', 'error', 'session_milestone', 'research_result', 'skill_performance']
        if obs_type in valid_types:
            props["Type"] = {"select": {"name": obs_type}}
        
        if obs.get('timestamp'):
            try:
                props["Date"] = {"date": {"start": obs['timestamp'][:10]}}
            except:
                pass
        
        result = notion_api(notion_key, "POST", "/v1/pages", {
            "parent": {"database_id": NOTION_DBS["learning_observations"]},
            "properties": props
        })
        
        if not result.get("error"):
            count += 1
            obs['synced_to_notion'] = True
        
        time.sleep(0.35)
    
    return count

# ──────────────────────────────────────────────
# Vault Report
# ──────────────────────────────────────────────

def write_vault_report(all_health, genome):
    """Write AGI-1 daily report to vault."""
    today = datetime.now().strftime('%Y-%m-%d')
    now = datetime.now().strftime('%H:%M ET')
    
    report = f"# AGI-1 Daily Report — {today}\n\n"
    report += f"**Generated:** {now}\n\n"
    
    # Genome status
    if genome:
        report += "## Genome Status\n\n"
        stats = genome.get('stats', {})
        report += f"- **Version:** {genome.get('version', 'unknown')}\n"
        report += f"- **Repos touched:** {stats.get('repos_touched', 0)}\n"
        report += f"- **Total patterns:** {stats.get('total_patterns_contributed', 0)}\n"
        report += f"- **Total instructions:** {stats.get('total_instructions_contributed', 0)}\n\n"
    
    # Per-repo health
    report += "## Agent/Repo Health\n\n"
    report += "| Repo | Patterns | Heals Today | Success Rate | Observations | Insights | Genome Ready |\n"
    report += "|---|---|---|---|---|---|---|\n"
    
    total_patterns = 0
    total_heals = 0
    total_obs = 0
    total_insights = 0
    total_genome = 0
    
    for health in all_health:
        report += f"| {health['repo']} | {health['patterns_active']} | {health['heals_today']} | "
        report += f"{health['heal_success_rate']:.0%} | {health['observations_today']} | "
        report += f"{health['insights_generated']} | {health['genome_contributions']} |\n"
        
        total_patterns += health['patterns_active']
        total_heals += health['heals_today']
        total_obs += health['observations_today']
        total_insights += health['insights_generated']
        total_genome += health['genome_contributions']
    
    report += f"| **TOTAL** | **{total_patterns}** | **{total_heals}** | — | "
    report += f"**{total_obs}** | **{total_insights}** | **{total_genome}** |\n\n"
    
    # Flywheel metrics
    report += "## Flywheel Metrics\n\n"
    report += f"- **Total repos scanned:** {len(all_health)}\n"
    report += f"- **Total healing patterns:** {total_patterns}\n"
    report += f"- **Genome-ready patterns:** {total_genome}\n"
    report += f"- **Learning observations today:** {total_obs}\n"
    report += f"- **Insights generated:** {total_insights}\n\n"
    
    # Write to vault
    os.makedirs(f"{VAULT_PATH}/domains/agi-1", exist_ok=True)
    report_path = f"{VAULT_PATH}/domains/agi-1/daily-report-{today}.md"
    with open(report_path, 'w') as f:
        f.write(report)
    
    # Also update the dashboard
    dashboard = f"# AGI-1 Dashboard\n\n"
    dashboard += f"**Last Updated:** {today} {now}\n\n"
    dashboard += f"## Current State\n\n"
    dashboard += f"- **Repos with AGI-1:** {len(all_health)}\n"
    dashboard += f"- **Total healing patterns:** {total_patterns} (26 starter + learned)\n"
    dashboard += f"- **Genome-ready for promotion:** {total_genome}\n"
    dashboard += f"- **Learning insights:** {total_insights}\n\n"
    dashboard += f"## Notion Databases\n\n"
    dashboard += f"| Database | ID |\n|---|---|\n"
    for name, db_id in NOTION_DBS.items():
        dashboard += f"| {name} | `{db_id}` |\n"
    dashboard += f"\n## Latest Report\n\n"
    dashboard += f"See [[daily-report-{today}]]\n"
    
    dashboard_path = f"{VAULT_PATH}/domains/agi-1/dashboard.md"
    with open(dashboard_path, 'w') as f:
        f.write(dashboard)
    
    return report, report_path


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

def main():
    report_only = '--report-only' in sys.argv
    
    env = load_env()
    notion_key = env.get('NOTION_API_KEY', '')
    
    print(f"AGI-1 Sync Engine — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Scanning {len(REPO_PATHS)} repos...")
    
    all_health = []
    total_obs_synced = 0
    
    for repo_path in REPO_PATHS:
        if not os.path.exists(repo_path):
            print(f"  ⏭️  {repo_path} — not found, skipping")
            continue
        
        repo_name = os.path.basename(repo_path)
        print(f"\n  📂 {repo_name}")
        
        # Scan health
        health = scan_repo_health(repo_path)
        all_health.append(health)
        print(f"     Patterns: {health['patterns_active']}, Heals today: {health['heals_today']}, "
              f"Obs today: {health['observations_today']}")
        
        if not report_only and notion_key:
            # Sync health to Notion
            sync_health_to_notion(notion_key, health, repo_name)
            
            # Sync new observations
            observations, insights = scan_repo_learning(repo_path)
            if observations:
                synced = sync_new_observations_to_notion(notion_key, observations, repo_name)
                total_obs_synced += synced
                print(f"     Synced {synced} new observations to Notion")
    
    # Scan genome
    genome = scan_genome()
    if genome:
        print(f"\n  🧬 Genome: v{genome.get('version', '?')}")
    else:
        print(f"\n  🧬 Genome: not found (will be created on first /agi-sync)")
    
    # Write vault report
    report, report_path = write_vault_report(all_health, genome)
    print(f"\n  📝 Vault report: {report_path}")
    
    if not report_only:
        print(f"\n  ✅ Synced {total_obs_synced} observations to Notion")
    
    # Print report to stdout for cron delivery
    print(f"\n{'='*60}\n")
    print(report)
    
    return report


if __name__ == '__main__':
    main()
