# Changelog — Bug Fixes & Patches

This file documents every non-obvious bug, fix, and key decision made during the build of this stack. If you hit a weird problem, check here first.

---

## 2026-04-29 — Watchdog Restart Loop

**Symptom**: Stack would restart repeatedly. `openclaw-gateway` would become `unhealthy` and the watchdog would restart it, which reset the Slack Socket Mode connection and caused another `unhealthy` → restart cycle.

**Root cause**: Two compounding issues:
1. The health check `curl` had no `--max-time` flag. During Slack Socket Mode cold-connect (~4 min), curl would hang indefinitely, causing the health check to time out → `unhealthy` after 3 retries.
2. The watchdog restarted containers in `unhealthy` state — but `unhealthy` is not the same as `dead`. A healthy-but-slow-starting container was being killed unnecessarily.

**Fix**:
- Added `--max-time 10` to the healthcheck curl command to prevent hangs
- Extended `start_period` from 180s → 420s (7 min) to cover Slack Socket Mode cold-connect time
- Updated watchdog to only restart containers in `exited` or `dead` state; `unhealthy`, `starting`, and `running` are left alone

---

## 2026-04-29 — Slack Pong Timeouts

**Symptom**: Slack WebSocket would disconnect every ~296s. Bot would stop responding until container restart.

**Root cause**: OpenClaw's internal `health-monitor` was killing the Slack SDK's WebSocket reconnect before it could complete (the SDK reconnects automatically after a pong timeout, but the health monitor killed the process first).

**Fix**: Add `"healthMonitor": {"enabled": false}` to the Slack (and Telegram) channel config in `openclaw.json`. The Docker health check and watchdog provide external health monitoring instead.

---

## 2026-04-29 — Config Validation Errors

Several config keys were tried that turned out to be invalid or misplaced:

| Invalid config | Problem | Fix |
|---------------|---------|-----|
| `"gateway": {"mode": "local"}` | `gateway.mode` is not a valid key — causes validation error on startup | Remove it |
| `"channels.slack.reactionLevel"` | `reactionLevel` is WhatsApp-only at the per-channel level | Remove from Slack config |
| `"channels.slack.statusReactions"` | Must be at the global `"messages"` level, not inside a channel block | Move to `"messages": {"statusReactions": {...}}` |
| `"dm": {"policy": "open", "allowFrom": ["U01..."]}"` | `allowFrom` only works with specific user IDs when `policy` is not `"open"` | Use `allowFrom: ["*"]` with `policy: "open"`, or remove `dm` block and use credentials file |

---

## 2026-04-29 — Stuck Session (`status: processing`)

**Symptom**: Agent stops responding. Container is healthy. Logs show `agent:main:main` session stuck with `status: "processing"` or missing `endedAt`.

**Root cause**: A previous task crashed mid-execution without properly closing the session. On next message, OpenClaw tries to resume the stuck session and hangs.

**Fix**: Run this inside the container to force-close stuck sessions:

```bash
docker exec openclaw-gateway node -e "
const fs = require('fs');
const path = '/home/node/.openclaw/agents/main/sessions/sessions.json';
const data = JSON.parse(fs.readFileSync(path));
let fixed = 0;
data.sessions = data.sessions.map(s => {
  if (s.status === 'processing' || !s.endedAt) {
    s.status = 'done';
    s.endedAt = new Date().toISOString();
    fixed++;
  }
  return s;
});
fs.writeFileSync(path, JSON.stringify(data, null, 2));
console.log('Fixed ' + fixed + ' sessions.');
"
docker compose restart openclaw-gateway
```

---

## 2026-04-28 — 16,454 Files Accidentally Staged

**Symptom**: `git status` showed 16,454 files staged. `git add .` had picked up `openclaw/repo/` — the full upstream OpenClaw source tree.

**Root cause**: `openclaw/repo/` was not in `.gitignore`.

**Fix**:
```bash
echo "openclaw/repo/" >> .gitignore
git rm -r --cached .
git add .
git commit -m "fix: remove openclaw/repo from tracking"
```

---

## 2026-04-28 — OpenClaw Slack Pairing Approval

**Symptom**: First DM to the bot gets no response. Logs show "pairing required."

**Root cause**: OpenClaw requires explicit pairing approval for each Slack user before it will respond to their DMs. This is not documented clearly in the official docs.

**Fix**: Pre-approve your user ID via the container node script (see `docs/setup.md` Step 6). Alternatively, send a DM from Slack and approve via the OpenClaw UI at `http://localhost:18789`.

---

## 2026-04-28 — OpenRouter Model Config

**Note**: The model string for OpenRouter must use the slug format:
```json
"model": { "primary": "openrouter/deepseek/deepseek-v4-flash" }
```
Not `"deepseek/deepseek-v4-flash"` alone — the `openrouter/` prefix is required for the OpenRouter plugin to intercept the request.
