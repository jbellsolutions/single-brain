# Single Brain — OpenClaw + Hermes Agent Stack

Autonomous dual-agent stack running on DigitalOcean. OpenClaw handles Slack/Telegram channels and executes tasks; Hermes orchestrates, self-improves, and writes SOPs. Both share a git-backed vault for memory.

```
┌──────────────────────────────────────────────────────────────┐
│                    DigitalOcean VPS                          │
│                 single-brain (104.236.11.200)                │
│                                                              │
│   ┌─────────────────────┐   ┌──────────────────────────┐    │
│   │   openclaw-gateway  │   │         hermes           │    │
│   │                     │   │                          │    │
│   │  Slack ──► Agent    │   │  Orchestrator /          │    │
│   │  Telegram ► Agent   │   │  Self-improvement        │    │
│   │                     │   │  Cron + SOP writer       │    │
│   │  :18789 (UI)        │   │                          │    │
│   └────────┬────────────┘   └──────────┬───────────────┘    │
│            │                           │                     │
│            └─────────┬─────────────────┘                    │
│                      │                                       │
│              ┌───────▼────────┐                              │
│              │  /vault (git)  │  Shared memory, SOPs,        │
│              │                │  decisions, daily logs       │
│              └────────────────┘                              │
│                                                              │
│  LLM: openrouter/deepseek/deepseek-v4-flash                  │
│  Watchdog: crontab every 60s + Docker restart: unless-stopped│
└──────────────────────────────────────────────────────────────┘
```

## Stack

| Component | Details |
|-----------|---------|
| VPS | DigitalOcean, 4 vCPU / 8 GB RAM / 160 GB SSD |
| OpenClaw | `ghcr.io/openclaw/openclaw:latest` |
| Hermes | `nousresearch/hermes-agent:latest` |
| LLM | OpenRouter → DeepSeek V4 Flash |
| Channels | Slack (Bottom Line Mktg), Telegram (@singlebrain_jb_bot) |
| Vault | Git repo at `/srv/single-brain/vault` |

## Cost

| Item | Monthly |
|------|---------|
| DigitalOcean Droplet | $24 |
| OpenRouter (both agents) | $5–20 |
| **Total** | **$29–44/mo** |

*vs. ~$500–700/mo on Anthropic direct.*

## Directory Structure

```
/srv/single-brain/
├── compose.yml              # Docker Compose (both agents)
├── .env                     # Secrets — never committed
├── .env.example             # Template — safe to commit
├── README.md                # This file
├── bin/
│   └── watchdog.sh          # Health-check + auto-restart script
├── docs/
│   ├── architecture.md      # Deep-dive architecture
│   ├── setup.md             # Fresh install guide
│   ├── channels.md          # Channel config reference
│   └── recovery.md          # Runbook for common failures
├── openclaw/
│   ├── config/              # Mounted → /home/node/.openclaw
│   │   ├── openclaw.json    # Active OpenClaw config (channels, model, plugins)
│   │   ├── credentials/     # Pairing approvals (never commit tokens here)
│   │   └── agents/          # Per-agent sessions and memory
│   ├── workspace/           # Agent working directory
│   └── openclaw.example.json  # Redacted config template
├── hermes/
│   └── config/              # Mounted → /root/.hermes
├── vault/                   # Shared agent memory (git repo)
│   ├── agents/              # Agent instructions (CLAUDE.md, voice)
│   ├── sops/                # Standard operating procedures per domain
│   ├── decisions/           # Append-only decision log
│   ├── daily-logs/          # Agent activity (one file per UTC day)
│   └── domains/             # Work product per domain
├── logs/                    # Shared log mount
└── scripts/                 # Utility scripts
```

## Quick Commands

```bash
# SSH in
ssh single-brain

# Container status
cd /srv/single-brain && docker compose ps

# Live logs
docker compose logs -f openclaw-gateway
docker compose logs -f hermes

# Restart everything
docker compose restart

# Restart one container
docker compose restart openclaw-gateway

# Pull latest images + redeploy
docker compose pull && docker compose up -d

# Open OpenClaw UI (from Mac — requires SSH tunnel)
ssh -L 18789:127.0.0.1:18789 single-brain -N &
open http://localhost:18789

# Check watchdog log
tail -f /srv/single-brain/vault/daily-logs/$(date -u +%F).md

# Edit OpenClaw config
nano /srv/single-brain/openclaw/config/openclaw.json
docker compose restart openclaw-gateway
```

## Channels

| Channel | Status | Bot Name |
|---------|--------|----------|
| Slack | ✅ Active | @single_brain (Bottom Line Mktg Solutions) |
| Telegram | ✅ Active | @singlebrain_jb_bot |

## Always-On (3-layer uptime)

1. **Docker `restart: unless-stopped`** — containers restart on crash/OOM automatically
2. **Docker systemd service** — Docker daemon starts on boot; containers follow
3. **Watchdog crontab** — `* * * * * /srv/single-brain/bin/watchdog.sh` — explicit health check every 60s, logs restarts to vault daily-log

## Security

- Gateway port `18789` binds to `127.0.0.1` only — no public exposure
- Access UI via SSH tunnel only
- All secrets in `.env` (never committed)
- Container `security_opt: no-new-privileges:true`
- SSH key auth only (password disabled)

## Slack Bot Configuration

- **Workspace**: Bottom Line Marketing Solutions (`T01D6BZEGA0`)
- **Bot user**: `@single_brain`
- **Approved DM user**: `U01D077J78S`
- **Pairing**: Stored in `openclaw/config/credentials/slack-default-allowFrom.json`
- **Message bot**: DM `@single_brain` directly in Slack

## Telegram Bot Configuration

- **Bot**: `@singlebrain_jb_bot`
- **Approved user ID**: `1264488761`
- Message the bot directly on Telegram

## See Also

- [Architecture deep-dive](docs/architecture.md)
- [Fresh install guide](docs/setup.md)
- [Channel config reference](docs/channels.md)
- [Recovery runbook](docs/recovery.md)
