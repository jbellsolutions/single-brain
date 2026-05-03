# Speaker Agent — Handshake Protocol

## Architecture

```
Justin (Telegram) → Hermes (this VPS) → Vault + Notion → Speaker Agent (separate VPS)
                                            ↑__________________|
                                                    (reads tasks, writes results)
```

## The Vault Is The API

No MCP. No HTTP. The Obsidian vault is the message bus.

```
projects/speaker-agent/
├── INBOX/          ← Hermes writes tasks here. Speaker Agent reads.
├── OUTBOX/         ← Speaker Agent writes results here. Hermes reads.
├── specs/          ← Architecture docs, PRDs, design decisions
├── events/         ← Both agents log significant events
├── sprints/        ← Sprint plans, retrospectives
└── health/         ← Agent health reports (also synced to Notion)
```

## INBOX Format (Hermes → Speaker Agent)

Create files as: `INBOX/TASK-{YYYY-MM-DD}-{seq}.md`

```markdown
---
task_id: TASK-2026-05-02-001
created: 2026-05-02T10:00:00-04:00
priority: P1
repo: backend
type: feature
estimate: 4h
notion_task_id: xxx
---

# Fix auth middleware race condition

**Context:** The JWT refresh middleware has a race condition when two requests 
hit the refresh endpoint simultaneously. Both get new tokens, one gets invalidated.

**Acceptance Criteria:**
- [ ] Add distributed lock on refresh endpoint
- [ ] Write tests for concurrent refresh scenario
- [ ] Update middleware docs
- [ ] PR against `main` with "fix:" commit

**Files to start with:**
- `backend/src/middleware/auth.ts`
- `backend/src/services/token.ts`

**Related:** Notion Task #xxx
```

## OUTBOX Format (Speaker Agent → Hermes)

Speaker Agent writes: `OUTBOX/TASK-{id}-DONE.md`

```markdown
---
task_id: TASK-2026-05-02-001
completed: 2026-05-02T14:30:00-04:00
status: done
pr_url: https://github.com/.../pull/142
files_changed: 3
tests: 7 passed, 0 failed
---

# Done: Fix auth middleware race condition

**What changed:**
- Added Redis-based distributed lock (SETNX with 5s TTL)
- Refresh endpoint now returns 409 if lock held
- 7 new tests covering concurrent refresh, lock timeout, lock release
- Updated middleware docs with concurrency section

**PR:** https://github.com/jbellsolutions/speaker-agent-backend/pull/142

**Notes:** Used ioredis since we already have Redis for session store. 
No new dependencies.
```

## Handshake Workflow

### Hermes (me) writes a task:
1. Create task in Notion 🔊 Speaker Agent — Tasks DB
2. Write INBOX markdown file in vault
3. Git commit + push to `jbellsolutions/single-brain`
4. (Optionally) create GitHub issue and link in Notion

### Speaker Agent picks up task:
1. Cron job (every 5min): `git pull` vault
2. Scans `INBOX/*.md` for new tasks
3. Prioritizes, assigns itself
4. Updates Notion task status to "In Progress"
5. Executes the work

### Speaker Agent reports completion:
1. Writes OUTBOX/TASK-{id}-DONE.md
2. Updates Notion task to "Review" or "Done"
3. Git commit + push to vault
4. Creates GitHub PR
5. Logs event to `events/` and Agent Health

### Hermes (me) reviews:
1. Cron job (every 30min) scans OUTBOX for new DONE files
2. Reviews PRs referenced
3. Updates Notion
4. Reports to Justin in Slack/Telegram

## Event Logging

Both agents write structured events to `projects/speaker-agent/events/`:

```markdown
---
timestamp: 2026-05-02T14:30:00-04:00
agent: speaker-agent
event_type: task_completed
task_id: TASK-2026-05-02-001
---
Task completed. PR #142. 7 tests passing.
```

## Health Monitoring

Speaker Agent writes daily health to `health/YYYY-MM-DD.md` AND Notion 🔊 Speaker Agent — Agent Health DB:

```markdown
---
date: 2026-05-02
sessions: 12
tasks_completed: 3
prs_created: 2
errors: 1
vault_sync: synced
git_push: synced
---
```

## Emergency Protocol

If Speaker Agent goes offline:
1. Hermes detects staleness (>30min since last vault sync or health report)
2. Alerts Justin via Telegram
3. Tasks in INBOX get reassigned to Hermes (manual override)
4. All Speaker Agent tasks in Notion marked "Blocked" with note

## Reset Protocol

If Speaker Agent needs full context reset:
1. Hermes copies current state to `specs/RESET-{date}.md`
2. Hermes writes new `INBOX/CONTEXT.md` with full project state
3. Speaker Agent loads CONTEXT.md on next boot
4. Normal handshake resumes
