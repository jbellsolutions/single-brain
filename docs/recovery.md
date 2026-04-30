# Recovery Runbook

## Container Won't Start

```bash
docker compose ps          # check status
docker compose logs --tail=50 openclaw-gateway
docker compose logs --tail=50 hermes
```

Common causes: bad `openclaw.json` (config validation), missing env vars, port conflict.

---

## OpenClaw Crash Loop (Config Validation Error)

Symptom: container restarts every ~7s, logs show config validation error.

1. Check logs for the exact error:
   ```bash
   docker compose logs --tail=20 openclaw-gateway | grep -i "error\|invalid\|validation"
   ```

2. Find and restore last-good config:
   ```bash
   ls /srv/single-brain/openclaw/config/openclaw.json.*.bak
   # OpenClaw auto-saves up to 4 rolling backups
   cp /srv/single-brain/openclaw/config/openclaw.json.1.bak \
      /srv/single-brain/openclaw/config/openclaw.json
   docker compose restart openclaw-gateway
   ```

**Known config pitfalls**:
- `dm.policy: "open"` requires `allowFrom: ["*"]` — cannot restrict to a specific user ID
- `gateway.mode` key is not valid in the current schema
- Tokens must be non-empty strings if the channel is `enabled: true`

---

## Slack Bot Not Responding

### Step 1: Check container health
```bash
docker compose ps | grep openclaw
```
Must be `healthy`. If `starting`, wait up to 3 min.

### Step 2: Check Socket Mode connection
```bash
docker compose logs openclaw-gateway | grep -i "socket mode"
```
Should see `slack socket mode connected`.

### Step 3: Check for stuck session
```bash
docker compose logs openclaw-gateway | grep -i "stuck session"
```

If you see `stuck session: sessionKey=agent:main:main state=processing`:

```bash
# Fix stuck session
docker exec openclaw-gateway node -e "
const fs = require('fs');
const path = '/home/node/.openclaw/agents/main/sessions/sessions.json';
const data = JSON.parse(fs.readFileSync(path));
const main = data['agent:main:main'];
if (main) {
  main.status = 'done';
  main.abortedLastRun = false;
  delete main.lastInteractionAt;
  fs.writeFileSync(path, JSON.stringify(data, null, 2));
  console.log('Fixed. status:', main.status);
} else { console.log('Key not found'); }
"
docker compose restart openclaw-gateway
```

### Step 4: Check user allowlist
```bash
docker exec openclaw-gateway cat /home/node/.openclaw/credentials/slack-default-allowFrom.json
```
Your Slack user ID must be in `allowFrom`.

---

## Hermes Won't Start

Hermes `depends_on openclaw-gateway: condition: service_healthy` — it only starts after OpenClaw is healthy (up to 3 min). This is expected.

If OpenClaw is healthy but Hermes still fails:
```bash
docker compose logs --tail=30 hermes
```

Common: permission error on `/opt/data/cron/jobs.json`:
```bash
docker exec --user root hermes chmod 644 /opt/data/cron/jobs.json
docker compose restart hermes
```

---

## Watchdog Not Running

```bash
crontab -l | grep watchdog
```

If missing:
```bash
(crontab -l 2>/dev/null; echo "* * * * * /srv/single-brain/bin/watchdog.sh") | crontab -
```

If duplicate entries (runs twice/min):
```bash
crontab -l | sort | uniq | crontab -
```

---

## Update to Latest Images

```bash
cd /srv/single-brain
docker compose pull
docker compose up -d
```

---

## Full Stack Restart

```bash
cd /srv/single-brain
docker compose down
docker compose up -d
```

---

## SSH Access Lost

From DigitalOcean console (browser-based terminal):
```
https://cloud.digitalocean.com → Droplets → single-brain → Console
```

---

## Disk Full

```bash
df -h
# Clean Docker artifacts
docker system prune -f
# Check vault logs size
du -sh /srv/single-brain/vault/daily-logs/
# Archive old logs
tar -czf /srv/vault-logs-$(date +%F).tar.gz /srv/single-brain/vault/daily-logs/
rm /srv/single-brain/vault/daily-logs/*.md  # keep recent only
```

---

## Rotate API Keys

1. Generate new key in [OpenRouter dashboard](https://openrouter.ai/settings/keys)
2. Update `/srv/single-brain/.env`
3. `docker compose up -d --force-recreate`
