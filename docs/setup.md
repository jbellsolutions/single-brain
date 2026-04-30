# Setup — Fresh Install Guide

## Prerequisites

- DigitalOcean droplet (Ubuntu 22.04+), 4 vCPU / 8 GB RAM recommended
- Docker + Docker Compose installed
- SSH key access as `claw` user (sudo)
- OpenRouter account with two API keys created
- Slack app with Socket Mode enabled (bot token `xoxb-...` + app token `xapp-...`)
- Telegram bot token (from @BotFather)

## 0. SSH Config (from your Mac)

Add this to `~/.ssh/config` on your Mac so scripts and tunnel commands work:

```
Host your-server
    HostName YOUR.SERVER.IP
    User claw
    IdentityFile ~/.ssh/id_ed25519
```

Replace `YOUR.SERVER.IP` with your droplet's IP address. Then:

```bash
ssh your-server   # should connect without a password prompt
```

## 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/single-brain.git /srv/single-brain
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
- `TELEGRAM_USER_ID` — your numeric Telegram user ID (not the bot ID)
- `SLACK_TEAM_ID` — workspace team ID (starts with `T`)
- `SLACK_USER_ID` — your user ID in Slack (starts with `U`)

## 3. Configure OpenClaw

```bash
cp openclaw/openclaw.example.json openclaw/config/openclaw.json
nano openclaw/config/openclaw.json
```

Fill in your actual bot tokens where marked `YOUR_SLACK_BOT_TOKEN`, `YOUR_SLACK_APP_TOKEN`, and `YOUR_TELEGRAM_BOT_TOKEN`. This file is gitignored — it will never be committed.

## 4. Initialize Vault

```bash
mkdir -p /srv/single-brain/vault
cd /srv/single-brain/vault
git init
# Optional: copy vault-skeleton/ files as starting point
cp -r /srv/single-brain/vault-skeleton/. /srv/single-brain/vault/
git add .
git commit -m "init: vault structure"
```

## 5. Start Stack

```bash
cd /srv/single-brain
docker compose up -d
```

OpenClaw takes **up to 7 minutes** to become `healthy` (start_period: 420s — covers Slack Socket Mode cold-connect time).

Check status:
```bash
docker compose ps
docker compose logs -f openclaw-gateway
```

## 6. Pair Slack User

On first message from a new Slack user, OpenClaw will ask for pairing approval. To pre-approve your user ID:

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

Replace `YOUR_SLACK_USER_ID` with your actual Slack user ID (e.g. `U01XXXXXXXX`).

## 7. Install Watchdog

```bash
crontab -e
# Add: * * * * * /srv/single-brain/bin/watchdog.sh
```

## 8. Enable Docker on Boot

```bash
sudo systemctl enable docker
```

## 9. Verify

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
ssh -L 18789:127.0.0.1:18789 your-server -N &
open http://localhost:18789
```

The gateway token (from `.env`) is the UI password.
