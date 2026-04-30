# Channel Configuration Reference

## Slack

### Config (openclaw.json)

```json
"channels": {
  "slack": {
    "name": "single-brain",
    "enabled": true,
    "botToken": "YOUR_SLACK_BOT_TOKEN",
    "appToken": "YOUR_SLACK_APP_TOKEN",
    "ackReaction": "eyes",
    "statusReactions": {
      "enabled": true,
      "emojis": { "done": "white_check_mark", "error": "x" }
    },
    "healthMonitor": { "enabled": false }
  }
}
```

| Field | Description |
|-------|-------------|
| `botToken` | OAuth bot token (`xoxb-...`). Needs `chat:write`, `im:history`, `reactions:write` |
| `appToken` | App-level token (`xapp-...`). Socket Mode. Needs `connections:write` |
| `ackReaction` | Emoji reaction added when message received. `eyes` = 👀 |
| `statusReactions` | Auto-react with ✅/❌ on task done/error |
| `healthMonitor` | **Must be `false`** — internal monitor kills the SDK reconnect before it completes, causing pong timeouts |

### User Allowlist

Approved users are stored in the credentials file (not in `openclaw.json`):

```
/home/node/.openclaw/credentials/slack-default-allowFrom.json
```

```json
{ "version": 1, "allowFrom": ["YOUR_SLACK_USER_ID"] }
```

To add a user, edit this file inside the container and restart:
```bash
docker exec openclaw-gateway node -e "/* see setup.md */"
docker compose restart openclaw-gateway
```

### Current Status

| | |
|--|--|
| Workspace | `<your-workspace-name>` |
| Team ID | `<YOUR_SLACK_TEAM_ID>` |
| Bot user | `<@your_bot_name>` |
| Approved users | `<YOUR_SLACK_USER_ID>` |
| Socket Mode | Configure in `openclaw.json` |

### Reaction Protocol

| Reaction | Meaning |
|----------|---------|
| 👀 | Message received, processing |
| ✅ | Task completed |
| ❌ | Error |
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
    "botToken": "YOUR_TELEGRAM_BOT_TOKEN",
    "reactionLevel": "extensive",
    "healthMonitor": { "enabled": false }
  }
}
```

| Field | Description |
|-------|-------------|
| `botToken` | Bot token from @BotFather |
| `reactionLevel` | `"extensive"` enables full reaction lifecycle (received → processing → done/error) |
| `healthMonitor` | **Must be `false`** — same reason as Slack |

### Current Status

| | |
|--|--|
| Bot | `<@your_telegram_bot>` |
| Approved user ID | `<YOUR_TELEGRAM_USER_ID>` |
| Status | Configure in `openclaw.json` |

### To Message

Find your bot on Telegram and send a DM directly.

---

## Adding a New Channel

1. Check `openclaw channels list` for available channel plugins
2. Add the channel block to `openclaw.json` under `channels`
3. Restart: `docker compose restart openclaw-gateway`
4. Check logs: `docker compose logs -f openclaw-gateway | grep -i channel`
