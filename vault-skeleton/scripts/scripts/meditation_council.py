#!/usr/bin/env python3
"""
AGI-1 Meditation Council — Reflects on learnings and makes general improvement suggestions.

Reads all observations, insights, healing patterns, and genome data across repos.
Synthesizes general learnings that apply beyond specific projects.
Outputs suggestions (never takes action) for:
- Skill improvements
- Process improvements
- Cross-repo patterns
- Framework upgrades

Usage:
    PYTHONPATH=/opt/data/home/.local/lib/python python3 meditation_council.py
"""

import json
import os
import sys
import glob
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from pathlib import Path

VAULT_PATH = os.environ.get('OBSIDIAN_VAULT_PATH', '/opt/data/obsidian-vault')

REPO_PATHS = [
    "/tmp/ai-integraterz-cold-email",
    "/tmp/notion-super-agent-phase-3",
    "/tmp/agi-1",
]

def load_all_data():
    """Load all AGI-1 data across repos."""
    all_patterns = []
    all_observations = []
    all_insights = []
    all_history = []
    
    for repo_path in REPO_PATHS:
        if not os.path.exists(repo_path):
            continue
        repo_name = os.path.basename(repo_path)
        
        for subdir in ['.claude', '.agi1']:
            # Patterns
            p_file = os.path.join(repo_path, subdir, 'healing', 'patterns.json')
            if os.path.exists(p_file):
                with open(p_file) as f:
                    data = json.load(f)
                    for p in data.get('patterns', []):
                        p['_repo'] = repo_name
                        all_patterns.append(p)
            
            # History
            h_file = os.path.join(repo_path, subdir, 'healing', 'history.json')
            if os.path.exists(h_file):
                with open(h_file) as f:
                    data = json.load(f)
                    for h in data.get('entries', data.get('history', [])):
                        h['_repo'] = repo_name
                        all_history.append(h)
            
            # Observations
            o_file = os.path.join(repo_path, subdir, 'learning', 'observations.json')
            if os.path.exists(o_file):
                with open(o_file) as f:
                    data = json.load(f)
                    for o in data.get('observations', []):
                        o['_repo'] = repo_name
                        all_observations.append(o)
            
            # Insights
            i_file = os.path.join(repo_path, subdir, 'learning', 'insights.json')
            if os.path.exists(i_file):
                with open(i_file) as f:
                    data = json.load(f)
                    for i in data.get('insights', []):
                        i['_repo'] = repo_name
                        all_insights.append(i)
    
    return all_patterns, all_observations, all_insights, all_history


def analyze_patterns(patterns):
    """Find cross-cutting themes in healing patterns."""
    findings = []
    
    # Category distribution
    cats = Counter(p.get('category', 'unknown') for p in patterns)
    top_cat = cats.most_common(1)[0] if cats else ('none', 0)
    findings.append({
        "type": "pattern_distribution",
        "finding": f"Most common error category: **{top_cat[0]}** ({top_cat[1]} patterns)",
        "detail": f"Distribution: {dict(cats.most_common(10))}",
        "suggestion": f"Consider writing a dedicated SOP for {top_cat[0]} errors — they're the most frequent pattern."
    })
    
    # High-confidence patterns (genome candidates)
    genome_ready = [p for p in patterns if p.get('confidence', 0) >= 0.8 and p.get('times_fixed', 0) >= 5]
    if genome_ready:
        findings.append({
            "type": "genome_candidates",
            "finding": f"**{len(genome_ready)} patterns** ready for genome promotion",
            "detail": ", ".join(p.get('id', '?') for p in genome_ready),
            "suggestion": "Run `/agi-sync` to promote these to the shared genome. All future repos will inherit them."
        })
    
    # Low-confidence patterns (failing)
    failing = [p for p in patterns if p.get('confidence', 0) < 0.3 and p.get('times_seen', 0) >= 5]
    if failing:
        findings.append({
            "type": "failing_patterns",
            "finding": f"**{len(failing)} patterns** with low confidence (<0.3) after 5+ attempts",
            "detail": ", ".join(f"{p.get('id', '?')} ({p.get('confidence', 0):.0%})" for p in failing),
            "suggestion": "Review and either fix the fix strategy or demote these patterns."
        })
    
    # Cross-repo patterns
    repo_patterns = defaultdict(list)
    for p in patterns:
        repo_patterns[p.get('_repo', 'unknown')].append(p)
    
    if len(repo_patterns) > 1:
        # Find patterns that appear in multiple repos
        pattern_ids = defaultdict(set)
        for p in patterns:
            pattern_ids[p.get('id', '')].add(p.get('_repo', ''))
        cross_repo = {pid: repos for pid, repos in pattern_ids.items() if len(repos) > 1}
        if cross_repo:
            findings.append({
                "type": "cross_repo_patterns",
                "finding": f"**{len(cross_repo)} patterns** appear in multiple repos",
                "detail": str(cross_repo),
                "suggestion": "These are strong genome candidates — they've proven useful across different codebases."
            })
    
    return findings


def analyze_observations(observations):
    """Find systemic themes in observations."""
    findings = []
    
    if not observations:
        findings.append({
            "type": "no_observations",
            "finding": "No learning observations collected yet",
            "detail": "The learning system hasn't captured any signals.",
            "suggestion": "Activate hooks in repos (PostToolUse, SessionEnd) or run `/agi-learn` after sessions."
        })
        return findings
    
    # Type distribution
    types = Counter(o.get('type', 'unknown') for o in observations)
    findings.append({
        "type": "observation_types",
        "finding": f"**{len(observations)} observations** across {len(types)} types",
        "detail": f"Distribution: {dict(types.most_common(10))}",
        "suggestion": None
    })
    
    # Repeated errors (systemic issues)
    repeated = [o for o in observations if o.get('type') == 'repeated_error']
    if repeated:
        findings.append({
            "type": "repeated_errors",
            "finding": f"**{len(repeated)} repeated errors** detected — these are systemic issues",
            "detail": "; ".join(o.get('subject', o.get('evidence', '?'))[:80] for o in repeated[:5]),
            "suggestion": "Each repeated error should become a healing pattern. Create patterns for the top offenders."
        })
    
    # Ignored instructions
    ignored = [o for o in observations if o.get('type') == 'instruction_ignored']
    if ignored:
        subjects = Counter(o.get('subject', '?') for o in ignored)
        findings.append({
            "type": "ignored_instructions",
            "finding": f"**{len(ignored)} ignored instructions** — agents aren't following these",
            "detail": f"Most ignored: {dict(subjects.most_common(5))}",
            "suggestion": "Rewrite these instructions to be clearer, or investigate why agents skip them. "
                         "If consistently ignored, the instruction may be wrong — consider removing it."
        })
    
    # Corrections (2x weight — human feedback)
    corrections = [o for o in observations if o.get('type') == 'correction']
    if corrections:
        findings.append({
            "type": "corrections",
            "finding": f"**{len(corrections)} human corrections** — highest-value learning signals",
            "detail": "; ".join(o.get('evidence', '?')[:80] for o in corrections[:5]),
            "suggestion": "Every correction should generate an insight. Run `/agi-learn` to process these."
        })
    
    return findings


def analyze_skills_meta(patterns, observations, insights):
    """Meta-analysis: how can we improve the WAY we build skills and systems?"""
    findings = []
    
    # Skill-related observations
    skill_obs = [o for o in observations if 'skill' in o.get('type', '')]
    if skill_obs:
        unused = [o for o in skill_obs if o.get('type') == 'skill_unused']
        popular = [o for o in skill_obs if o.get('type') == 'skill_popular']
        
        if unused:
            findings.append({
                "type": "skill_improvement",
                "finding": f"**{len(unused)} skills** are going unused",
                "detail": "; ".join(o.get('subject', '?') for o in unused[:5]),
                "suggestion": "Unused skills should be either: (1) better triggered (update trigger conditions), "
                             "(2) merged into other skills, or (3) archived. Skills that don't fire are dead weight."
            })
        
        if popular:
            findings.append({
                "type": "skill_success",
                "finding": f"**{len(popular)} skills** are frequently used — these are your best patterns",
                "detail": "; ".join(o.get('subject', '?') for o in popular[:5]),
                "suggestion": "Study these skills. What makes them fire often? Apply the same trigger patterns to underperforming skills."
            })
    
    # General meta-learnings
    if len(patterns) >= 10:
        # Fix strategy distribution
        fix_types = Counter(p.get('fix_type', 'unknown') for p in patterns)
        findings.append({
            "type": "meta_fix_strategies",
            "finding": f"Fix strategy distribution: {dict(fix_types)}",
            "detail": "How patterns solve problems",
            "suggestion": "If 'command' dominates, consider building more 'edit' patterns — "
                         "they're more precise and less likely to have side effects."
        })
    
    # Insight quality
    if insights:
        applied = [i for i in insights if i.get('status') == 'applied']
        rejected = [i for i in insights if i.get('status') == 'rejected']
        if applied and rejected:
            ratio = len(applied) / (len(applied) + len(rejected))
            findings.append({
                "type": "insight_quality",
                "finding": f"Insight acceptance rate: **{ratio:.0%}** ({len(applied)} applied, {len(rejected)} rejected)",
                "detail": "How often the learner produces actionable insights",
                "suggestion": "If below 50%, the learner's confidence threshold may be too low. Consider raising from 0.7 to 0.8."
            })
    
    return findings


def generate_council_report(all_findings):
    """Generate the meditation council report."""
    today = datetime.now().strftime('%Y-%m-%d')
    now = datetime.now().strftime('%H:%M ET')
    
    report = f"# 🧘 AGI-1 Meditation Council — {today}\n\n"
    report += f"**Generated:** {now}\n"
    report += "*The council reflects on learnings across all repos and suggests general improvements. "
    report += "It never takes action — only observes and recommends.*\n\n---\n\n"
    
    # Group by category
    categories = {
        "Pattern Health": [f for f in all_findings if f['type'] in ('pattern_distribution', 'genome_candidates', 'failing_patterns', 'cross_repo_patterns')],
        "Learning Signals": [f for f in all_findings if f['type'] in ('observation_types', 'repeated_errors', 'ignored_instructions', 'corrections', 'no_observations')],
        "Skill & Process Improvements": [f for f in all_findings if f['type'] in ('skill_improvement', 'skill_success', 'meta_fix_strategies', 'insight_quality')],
    }
    
    suggestion_count = 0
    
    for cat_name, findings in categories.items():
        if not findings:
            continue
        
        report += f"## {cat_name}\n\n"
        for f in findings:
            report += f"### {f['finding']}\n\n"
            if f.get('detail'):
                report += f"*Detail:* {f['detail']}\n\n"
            if f.get('suggestion'):
                report += f"💡 **Suggestion:** {f['suggestion']}\n\n"
                suggestion_count += 1
            report += "---\n\n"
    
    report += f"\n## Summary\n\n"
    report += f"- **Findings:** {len(all_findings)}\n"
    report += f"- **Suggestions:** {suggestion_count}\n"
    report += f"- **Repos analyzed:** {len([r for r in REPO_PATHS if os.path.exists(r)])}\n\n"
    report += "*These are suggestions only. No actions have been taken. "
    report += "Review and implement what resonates.*\n"
    
    return report


def main():
    print(f"🧘 AGI-1 Meditation Council — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # Load all data
    patterns, observations, insights, history = load_all_data()
    print(f"   Loaded: {len(patterns)} patterns, {len(observations)} observations, {len(insights)} insights")
    
    # Analyze
    all_findings = []
    all_findings.extend(analyze_patterns(patterns))
    all_findings.extend(analyze_observations(observations))
    all_findings.extend(analyze_skills_meta(patterns, observations, insights))
    
    print(f"   Findings: {len(all_findings)}")
    
    # Generate report
    report = generate_council_report(all_findings)
    
    # Write to vault
    today = datetime.now().strftime('%Y-%m-%d')
    os.makedirs(f"{VAULT_PATH}/domains/agi-1", exist_ok=True)
    report_path = f"{VAULT_PATH}/domains/agi-1/meditation-{today}.md"
    with open(report_path, 'w') as f:
        f.write(report)
    print(f"   Report: {report_path}")
    
    # Print for cron delivery
    print(f"\n{'='*60}\n")
    print(report)
    
    return report


if __name__ == '__main__':
    main()
