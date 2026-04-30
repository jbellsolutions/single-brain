# Architecture

## Overview

Single Brain is a dual-agent autonomous stack. OpenClaw handles inbound channel messages and executes tasks; Hermes orchestrates long-horizon work, writes SOPs, and can spawn sub-tasks. Both agents share a git-backed vault for persistent memory.

## Components

### OpenClaw Gateway

- **Image**: `ghcr.io/openclaw/openclaw:latest`
- **Role**: Channel-facing agent. Listens on Slack (Socket Mode) and Telegram. Routes messages to the `main` agent. Executes tools (web, code, file ops).
- **UI**: Runs on `:18789` (localhost-only). Access via SSH tunnel.
- **Config**: `/srv/single-brain/openclaw/config/` (mounted into container at `/home/node/.openclaw`)
- **Key files**:
  - `openclaw.json` — channels, model, plugins
  - `credentials/slack-default-allowFrom.json` — user allowlist for Slack DMs
  - `agents/main/sessions/sessions.json` — per-session state (important for debugging stuck sessions)

### Hermes

- **Image**: `nousresearch/hermes-agent:latest`
- **Role**: Orchestrator. Reads vault SOPs, writes decisions, runs scheduled jobs, self-improves. Starts only after OpenClaw is healthy.
- **Config**: `/srv/single-brain/hermes/config/` (mounted at `/root/.hermes`)
- **Entry point**: `hermes gateway run --accept-hooks` (daemon mode)

### Vault

- **Path**: `/srv/single-brain/vault/` (mounted at `/vault` in both containers)
- **Type**: Git repository
- **Purpose**: Shared persistent memory. Agents append to daily-logs, read SOPs, write decisions.
- **Layout**:
  ```
  vault/
  ├── agents/          CLAUDE.md (instructions), voice.md
  ├── sops/            Per-domain standard operating procedures
  ├── decisions/       Append-only log of major decisions
  ├── daily-logs/      One .md file per UTC day
  └── domains/         Work product (drafts, published, health)
  ```

## LLM Routing

Both agents use OpenRouter as the inference provider with DeepSeek V4 Flash as default:

```
Agent → OpenRouter API → deepseek/deepseek-v4-flash
```

Two separate API keys allow per-agent spend tracking and independent credit limits in the OpenRouter dashboard.

**Cost comparison**:
- DeepSeek V4 Flash via OpenRouter: ~$0.14/M input, ~$0.28/M output
- Claude Sonnet via Anthropic direct: ~$3/M input, ~$15/M output
- **Savings: 17–35×**

## Network

```
Internet → (Slack/Telegram APIs) → OpenClaw container
                                       │ agent_net bridge
                                    Hermes container

External access to UI:
  Mac ──SSH-tunnel──► VPS :18789 (localhost) ──► openclaw-gateway :18789
```

The gateway port is never publicly exposed.

## Data Flow (Slack message)

1. User DMs your bot (`@your_bot_name`) in Slack
2. Slack sends event via Socket Mode to `xapp-...` token
3. OpenClaw receives event, checks `credentials/slack-default-allowFrom.json`
4. If user is in allowlist → create/resume session → route to `main` agent
5. Agent processes with DeepSeek V4 Flash via OpenRouter
6. Response sent back to Slack thread
7. Session state persisted to `agents/main/sessions/sessions.json`
