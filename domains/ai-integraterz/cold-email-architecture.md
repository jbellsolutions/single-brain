# Cold Email System — Complete Architecture

**Repo:** `jbellsolutions/ai-integraterz-cold-email`
**Local Clone:** `/tmp/ai-integraterz-cold-email`
**Generated:** 2026-05-02

---

## Pipeline Overview

```
Lead Ingestion (CSV / Apify / Prospector)
    ↓
Strategy Squad (Opus 4.7, 3-agent council) → campaign-brief.md
    ↓
Research Squad (Haiku 4.5, parallel ×10) → per-prospect signals (S/A/B/C tiers)
    ↓
Copy Squad (Sonnet 4.6 hook + Haiku body + 4 validators + retries) → 3-email sequences
    ↓
SmartLead Squad (deterministic) → campaign in DRAFTED state
    ↓
Operator reviews → schedules → emails send
    ↓
Reply Loop (60s poll) → auto-handle OOO/unsub/spam → real replies → Slack
```

## Offers

1. **Power-Partner** — peer operator, "let's build together" framing
2. **Direct-Value** — placement/revenue, tangible outcome framing
3. **Capstone** — simple workflow rebuild, low-friction entry

## Campaign Naming

`<niche>-<offer>-<VARIANT>` (e.g. `recruiters-power-partner-A`)

## Email Rules

- Email 1: ≤125 words, conversation starter, reply-based CTA
- Email 2: ≤150 words, SAME subject (threading), new angle
- Email 3: ≤125 words, soft permission close
- **NO URLs** in emails 1-3 (only after reply)
- Sign off: `-- Justin`
- No flattery, no generic openers, no program-talk

## 4 Validation Gates (with retries)

1. **Slop check** — 25+ banned AI-tell phrases
2. **Sales check** — no fake timeframes, no "free", no money talk
3. **URL check** — zero URLs allowed
4. **Threading check** — emails 2 & 3 must have identical subject to email 1

## Reply Handling

- **Auto-handled silently:** OOO, unsubscribe (+ blocklist), spam
- **Triage classes:** positive, objection, question, soft_no, spam
- **Draft pipeline:** Haiku triage → Sonnet draft → Haiku approver → Slack for human
- **URL allowlist gate:** If drafter hallucinates a URL, verdict forced to FAIL

## Slack Tools (17)

`list_active_campaigns`, `list_briefs`, `read_brief`, `stats`, `ingest_csv_from_slack`, `pull_prospector_nl`, `pull_prospector_saved`, `prospect_fetch_confirmed`, `launch_pilot`, `load_leads_from_smartlead`, `preview_emails`, `schedule_campaign`, `generate_preview_pack`, `archive_campaign`, `precreate_campaigns`, `update_voice_rules`, `update_brief`

## Daemons

- **slack_agent** — polls `#cold-email-control` every 8s, Sonnet 4.6 routing
- **reply_loop** — polls SmartLead inbox every 60s
- **watchdog.sh** — supervises both, restarts within 15s

---

## Voice Rules (from data/voice_rules.md)

# Justin's voice rules — APPLIED TO EVERY COLD EMAIL

These rules live in `data/voice_rules.md` and are loaded by the Copy squad on
top of the campaign brief. They override anything in the brief that
contradicts them. Updates here propagate immediately to the next preview /
launch — no campaign-by-campaign edits required.

## The frame (most important)

A cold email is the START of a conversation, not a pitch.

Justin is an operator who runs an AI integration shop. He emails recruiters
the way an operator messages another operator with a curious observation and
a low-friction question. He is *not* selling. He is *not* announcing a
program. He is *not* offering anything for free upfront. He is opening a door.

If a draft reads like marketing copy, like a "limited time" offer, like a
"program" with a name, like a pitch deck condensed to a paragraph — it is
wrong. Rewrite.

## What the voice sounds like (recruiter campaigns)

**Power-Partner**: *"We're recruiters like you. Built our own AI stack.
Giving it away because I want to help the industry survive AI. That's it."*
Tone: peer-to-peer, deeply researched, conversation-starter. NO "paid partner
side." NO "program." NO "free recruiter stack" framing as a hook. The hook
is the observation about their firm + the offer to chat about the AI build,
nothing else upfront.

**Direct-Value (AICO/Expert/Sovereign)**: *"We're recruiters who place AI
techs, VAs, and chief officers into recruiting businesses. Great way to get
another revenue stream for you. Bigger purpose: save the industry, help
businesses adapt so they don't go extinct."* Tone: industry-survival framing,
peer concern, less sales-y. NO "AI sourcing agent." NO "14-day sprint" or any
made-up timeframe. NO "free." Match the placement-into-businesses framing,
not the build-this-thing-for-you framing.

**Capstone**: *"We'll rebuild one recruiting workflow. That's it."* Tone:
simple, non-pretentious, no timeframe promises. NO "6-10 weeks" or any
specific duration. NO "free expert rebuild" — just "we'll rebuild one
workflow with your team." If the brief or default copy mentions duration,
strip it.

## Hard rules (Copy squad enforces; bad drafts get retried)

1. *No links in emails 1, 2, or 3.* No calendar links, no website, no
   one-pager. Links go in the *reply* AFTER the prospect has replied AND
   asked. The whole 3-step sequence is link-free.

2. *Emails 2 and 3 use the same subject line as email 1, verbatim.* The
   thread depends on subject equality in the prospect's inbox; changing it
   breaks threading and the follow-up reads as a fresh cold email.

3. *No fake timeframes.* Never say "14-day sprint," "30-day sprint," "6-10
   weeks," "6 to 10 weeks." If a number isn't real and approved for this
   campaign, don't write it. Vague honesty ("a few weeks of co-building")
   beats specific lies ("we ship in 14 days").

4. *No "free" in the hook.* "Free recruiter stack," "for free," "completely
   free" all read as marketing/pitch. The free-ness lands in the *reply*,
   not the cold open.

5. *No program-talk.* "This program," "our program," "limited spots," "limited
   time" — never. Justin runs an integration shop, not a course.

6. *No "AI sourcing agent" framing* unless this campaign's brief explicitly
   approves it as the angle. Default voice across recruiter campaigns is "AI
   built solutions" / "an AI [role]" / "AI techs, VAs, chief officers."

7. *Email 1 ≤ 125 words. Email 2 ≤ 150 words. Email 3 ≤ 125 words.* Mobile-
   formatted. Sign off `-- Justin`.

8. *Reply-based CTA only.* "Worth a 12-min Loom?" "Want me to send the
   breakdown?" "Useful?" — never demanding, never with a link.

## What the prospect should feel after reading email 1

> "Huh, this isn't a pitch. This is a real recruiter who built something for
> their own shop and wants to know if I want to hear about it. I'll reply."

That's the bar. If the draft would make the prospect think *"oh, another AI
service vendor,"* it's wrong. Rewrite.



---

## AGENTS.md (Squad Definitions)

# AGENTS.md — Who works on this repo

This repo is operated by a swarm of specialized agents. This document
declares their roles, boundaries, and handoffs.

## Live in-process agents (forge-spawned)

### Strategy Squad
**Where**: `squads/strategy/squad.py`
**Model**: Opus 4.7 (1M context) via `anthropic-opus-1m` profile
**Topology**: PARALLEL_COUNCIL × 3 members, MAJORITY consensus
**Job**: Read campaign brief context (offer + niche + voice rules) + lead summary, emit a `brief.md` to `data/campaigns/<name>/brief.md`. Runs ONCE per campaign; cached forever.
**Boundary**: Does not touch leads, does not call Smartlead, does not write copy.
**Handoff to**: Research Squad (passes `brief` string).

### Research Squad
**Where**: `squads/research/squad.py`
**Model**: Haiku 4.5 (`anthropic-haiku`)
**Topology**: SOLO × N parallel (max 10 concurrent)
**Job**: For each `Lead`, surface a per-prospect signal (recent post, hire, funding, podcast, etc.). Output: dict written to `data/research/<email>.json`.
**Boundary**: Read-only on the web/sources; never writes Smartlead state.
**Handoff to**: Copy Squad (passes `(lead, signal)` pair).

### Copy Squad
**Where**: `squads/copy/squad.py`
**Models**: Sonnet 4.6 (hook) + Haiku 4.5 (body)
**Job**: Hook draft → Body draft → 4 validators (slop, sales, URL, threading). Retry up to 3 times with violation feedback injected. Output: `data/emails/<email>.json`.
**Boundary**: Never writes to Smartlead. Never overrides voice rules.
**Handoff to**: Smartlead Squad (passes the email sequence).

### Smartlead Squad
**Where**: `squads/smartlead/squad.py`
**Model**: deterministic (no LLM)
**Job**: Lookup-or-create Smartlead campaign by `<niche>-<offer>-<VARIANT>`. On first creation, save sequence template. Always: append leads with per-prospect custom_fields holding the generated copy.
**Boundary**: Idempotent. Will NOT recreate a campaign if one with the name exists; will NOT clobber an existing sequence template.
**Handoff to**: Operator (review in Smartlead UI, then `schedule_campaign` flips DRAFTED → ACTIVE).

### Reply Squad
**Where**: `squads/reply/squad.py`
**Models**: Haiku (triage + approver) + Sonnet (drafter)
**Job**: Per inbound reply: classify → draft response → URL allowlist gate. Auto-handles unsubscribe/OOO/spam silently. Other replies post to `#cold-email-replies` for human approval.
**Boundary**: Never sends a reply without human "send" in the thread (or auto-handle category).
**Handoff to**: Operator via Slack thread; on confirmation, calls `cli.reply_to_thread`.

## Daemons (long-running processes)

### slack_agent
**Where**: `orchestrator/slack_agent.py`
**Model**: Sonnet 4.6 for the routing tool-use loop
**Job**: Poll `#cold-email-control` every 8s; for each user message, run Anthropic tool-use over 17 registered tools.
**Boundary**: Confirms before destructive/credit-spending tools (`launch_pilot`, `prospect_fetch_confirmed`, `archive_campaign`, `precreate_campaigns`, `schedule_campaign`).
**Trigger**: User messages or file uploads in the control channel.
**Termination**: Never (under watchdog supervision).

### reply_loop
**Where**: `orchestrator/reply_loop.py`
**Job**: Poll Smartlead inbox every 60s. Process new replies through Reply Squad.
**Boundary**: Auto-handles only if triage confidence is high (unsubscribe/OOO/spam classes).
**Trigger**: Polling tick.
**Termination**: Never (under watchdog).

### watchdog
**Where**: `ops/watchdog.sh`
**Job**: Supervise both daemons. Restart within 15s of crash. Throttle to one restart per 30s.
**Termination**: User CTRL-C or kill.

## Skill agents (AGI-1 — installed at `~/.claude/skills/agi-1/`)

| Slash command | What it does | When to invoke |
|---|---|---|
| `/agi-1` | Full 8-phase pipeline | Major refactor / first bootstrap |
| `/agi-audit` | Score this repo | Before/after a change set |
| `/agi-heal` | Auto-fix a known error pattern | When a runtime error occurs |
| `/agi-learn` | Extract patterns from observations | Every 10 sessions |
| `/agi-council` | 3-perspective critique | Before a significant design change |
| `/agi-walkthrough` | End-to-end explainer | Onboarding a new collaborator |

## Handoff data schemas

Currently dict-passing (gap; pydantic adoption is a TODO). The implicit contracts:

- **Lead** → `{lead_id, name, email, company, title, linkedin_url}`
- **Signal** (research output) → `{tier: 'S'|'A'|'B', summary: str, evidence: list[str]}` (loose)
- **Email step** → `{step: 1|2|3, subject: str, body: str, delay_days: int}`
- **Smartlead lead payload** → `{first_name, last_name, email, company_name, custom_fields: dict}`

Future work: enforce these via pydantic models (TODO #2 in council critique).

## Escalation path

```
slack_agent (orchestrator)
   ↓ (operator confirms)
launch_pilot → Strategy → Research → Copy → SmartleadSquad
                                                ↓
                                          Smartlead (sends)
                                                ↓
                                          replies arrive
                                                ↓
                                          reply_loop → Reply Squad
                                                ↓
                                          #cold-email-replies (operator approves)
```

Maximum hop count from orchestrator to human = 2 (orchestrator → squads → operator review).

## KPIs (per agent)

Currently informal. Council critique flagged this as the lowest-scoring dimension. Targets to instrument (TODO):

- Strategy: % of briefs reused on append (target >90%)
- Research: signal tier distribution per campaign (target ≥30% S/A)
- Copy: slop_pass rate first attempt (target ≥80%); avg attempts to pass (target ≤1.5)
- Smartlead: lookup-vs-create ratio (target close to 1:1 once campaigns mature)
- Reply Squad: auto-handle rate (target ~30% of replies handled silently)
- slack_agent: median time to first response (target <12s)
- watchdog: restarts/day (target 0; alert if >3)



---
Tags: [[ai-integraterz]] [[cold-email]] [[smartlead]] [[voice-rules]] [[squads]]