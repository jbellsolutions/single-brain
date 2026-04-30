# Channel Configuration Reference

## Slack

### Config (openclaw.json)

```json
"channels": {
  "slack": {
    "name": "single-brain",
    "enabled": true,
    "botToken": "xoxb-...",
    "appToken": "xapp-...",
    "ackReaction": "eyes"
  }
}
```

| Field | Description |
|-------|-------------|
| `botToken` | OAuth bot token (`xoxb-...`). Needs `chat:write`, `im:history`, `reactions:write` |
| `appToken` | App-level token (`xapp-...`). Socket Mode. Needs `connections:write` |
| `ackReaction` | Emoji reaction added when message received. `eyes` = 👀 |

### User Allowlist

Approved users are stored in the credentials file (not in `openclaw.json`):

```
/home/node/.openclaw/credentials/slack-default-allowFrom.json
```

```json
{ "version": 1, "allowFrom": ["U01D077J78S"] }
```

To add a user, edit this file inside the container and restart:
```bash
docker exec openclaw-gateway node -e "/* see setup.md */"
docker compose restart openclaw-gateway
```

### Current Status

| | |
|--|--|
| Workspace | Bottom Line Marketing Solutions |
| Team ID | `T01D6BZEGA0` |
| Bot user | `@single_brain` |
| Approved users | `U01D077J78S` (Justin) |
| Socket Mode | Connected |

### Reaction Protocol

| Reaction | Meaning |
|----------|---------|
| 👀 | Message received, processing |
| ✅ | Task completed |
| ⚠️ | Completed with warnings |
| 🚫 | Declined (out of scope or policy) |

---

## Telegram

### Config (openclaw.json)

```json
"channels": {
  "telegram": {
    "name": "single-brain",
    "enabled": true,
    "botToken": "XXXXXXXXXX:..."
  }
}
```

| Field | Description |
|-------|-------------|
| `botToken` | Bot token from @BotFather |

### Current Status

| | |
|--|--|
| Bot | `@singlebrain_jb_bot` |
| Approved user ID | `1264488761` |
| Status | Active |

### To Message

Find `@singlebrain_jb_bot` on Telegram and send a DM directly.

---

## Adding a New Channel

1. Check `openclaw channels list` for available channel plugins
2. Add the channel block to `openclaw.json` under `channels`
3. Restart: `docker compose restart openclaw-gateway`
4. Check logs: `docker compose logs -f openclaw-gateway | grep -i channel`
