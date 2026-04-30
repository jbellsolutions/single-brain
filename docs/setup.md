# Setup — Fresh Install Guide

## Prerequisites

- DigitalOcean droplet (Ubuntu 22.04+), 4 vCPU / 8 GB RAM recommended
- Docker + Docker Compose installed
- SSH key access as `claw` user (sudo)
- OpenRouter account with two API keys created
- Slack app with Socket Mode enabled (bot token `xoxb-...` + app token `xapp-...`)
- Telegram bot token

## 1. Clone Repository

```bash
git clone https://github.com/jbellsolutions/single-brain.git /srv/single-brain
cd /srv/single-brain
```

## 2. Create .env

```bash
cp .env.example .env
nano .env   # fill in all values
```

Required values:
- `OPENCLAW_GATEWAY_TOKEN` — generate with `openssl rand -hex 32`
- `OPENCLAW_OPENROUTER_API_KEY` — key #1 from OpenRouter
- `HERMES_OPENROUTER_API_KEY` — key #2 from OpenRouter
- Telegram and Slack IDs

## 3. Initialize Vault

```bash
cd /srv/single-brain/vault
git init
git add .
git commit -m "init: vault structure"
```

## 4. Start Stack

```bash
cd /srv/single-brain
docker compose up -d
```

OpenClaw takes up to 3 minutes to become `healthy` (start_period: 180s).

Check status:
```bash
docker compose ps
docker compose logs -f openclaw-gateway
```

## 5. Pair Slack User

On first message from a new Slack user, OpenClaw will ask for pairing approval. To pre-approve:

```bash
docker exec -it openclaw-gateway node -e "
const fs = require('fs');
const path = '/home/node/.openclaw/credentials/slack-default-allowFrom.json';
let data = { version: 1, allowFrom: [] };
try { data = JSON.parse(fs.readFileSync(path)); } catch(e) {}
if (!data.allowFrom.includes('YOUR_SLACK_USER_ID')) {
  data.allowFrom.push('YOUR_SLACK_USER_ID');
  fs.writeFileSync(path, JSON.stringify(data, null, 2));
  console.log('Added.');
} else { console.log('Already present.'); }
"
```

## 6. Install Watchdog

```bash
crontab -e
# Add: * * * * * /srv/single-brain/bin/watchdog.sh
```

## 7. Enable Docker on Boot

```bash
sudo systemctl enable docker
```

## 8. Verify

```bash
# All containers healthy
docker compose ps

# OpenClaw connected to Slack
docker compose logs openclaw-gateway | grep -i "socket mode connected"

# Watchdog running
crontab -l | grep watchdog
```

## Access the UI

From your Mac:
```bash
ssh -L 18789:127.0.0.1:18789 single-brain -N &
open http://localhost:18789
```

The gateway token (from `.env`) is the UI password.
