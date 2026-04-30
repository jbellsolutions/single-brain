# Single Brain — OpenClaw + Hermes Agent Stack

Autonomous dual-agent stack. OpenClaw handles Slack/Telegram channels and executes tasks; Hermes orchestrates, self-improves, and writes SOPs. Both share a git-backed vault for memory.

> Inspired by [Eric Siu's video](https://www.youtube.com/watch?v=N5L1C1STZkw) — adapted with bug fixes, Composio tooling, and a full recovery runbook.

```
┌──────────────────────────────────────────────────────────────┐
│                    DigitalOcean VPS                          │
│                 your-vps-hostname                            │
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
| Channels | Slack, Telegram |
| Vault | Git repo at `/srv/single-brain/vault` |
| Tooling | Composio (250+ integrations for Hermes) |

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
│   ├── recovery.md          # Runbook for common failures
│   ├── changelog.md         # Bug fixes and patches log
│   └── composio.md          # Composio integration guide
├── openclaw/
│   ├── config/              # Mounted → /home/node/.openclaw
│   │   ├── openclaw.json    # Active OpenClaw config (channels, model, plugins) — NOT committed
│   │   └── agents/          # Per-agent sessions and memory
│   ├── workspace/           # Agent working directory
│   └── openclaw.example.json  # Redacted config template — copy to config/openclaw.json
├── hermes/
│   └── config/              # Mounted → /root/.hermes
├── vault-skeleton/          # Template vault structure — copy to /srv/single-brain/vault
├── vault/                   # Shared agent memory (git repo, not committed here)
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
# SSH in (requires SSH config alias — see docs/setup.md)
ssh your-server

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
ssh -L 18789:127.0.0.1:18789 your-server -N &
open http://localhost:18789

# Check watchdog log
tail -f /srv/single-brain/vault/daily-logs/$(date -u +%F).md

# Edit OpenClaw config
nano /srv/single-brain/openclaw/config/openclaw.json
docker compose restart openclaw-gateway
```

## Channels

| Channel | Status | Notes |
|---------|--------|-------|
| Slack | Configure in `openclaw.json` | Socket Mode, emoji reactions built-in |
| Telegram | Configure in `openclaw.json` | Full reaction lifecycle via `reactionLevel: "extensive"` |

## Always-On (3-layer uptime)

1. **Docker `restart: unless-stopped`** — containers restart on crash/OOM automatically
2. **Docker systemd service** — Docker daemon starts on boot; containers follow
3. **Watchdog crontab** — `* * * * * /srv/single-brain/bin/watchdog.sh` — explicit health check every 60s, logs restarts to vault daily-log

## Security

- Gateway port `18789` binds to `127.0.0.1` only — no public exposure
- Access UI via SSH tunnel only
- All secrets in `.env` (never committed)
- `openclaw/config/openclaw.json` is gitignored (contains live bot tokens)
- Container `security_opt: no-new-privileges:true`
- SSH key auth only (password disabled)

## See Also

- [Architecture deep-dive](docs/architecture.md)
- [Fresh install guide](docs/setup.md)
- [Channel config reference](docs/channels.md)
- [Recovery runbook](docs/recovery.md)
- [Bug fixes & changelog](docs/changelog.md)
- [Composio integration](docs/composio.md)
