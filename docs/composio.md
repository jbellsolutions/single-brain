# Composio Integration

[Composio](https://composio.dev) is a tool provider that gives agents access to 250+ pre-built integrations (Gmail, GitHub, Notion, HubSpot, Linear, etc.) via a single API. Adding it to Single Brain gives Hermes (and OpenClaw) a broad toolkit without building individual integrations.

## Status

**Not yet configured** — this is the planned integration path. The stack runs without Composio; this doc describes how to add it when ready.

## How It Works

Composio exposes tools as OpenAPI-compatible function definitions. Hermes (which accepts hooks and can call external APIs) can use Composio's MCP server or REST API to invoke actions on connected apps.

## Setup

### 1. Get a Composio API Key

Sign up at [composio.dev](https://composio.dev), create an API key.

### 2. Add to `.env`

```bash
COMPOSIO_API_KEY=your_composio_api_key_here
```

Also add to `.env.example`:
```bash
COMPOSIO_API_KEY=
```

### 3. Pass to Hermes Container

In `compose.yml`, add to the `hermes` service environment:

```yaml
hermes:
  environment:
    COMPOSIO_API_KEY: ${COMPOSIO_API_KEY}
```

### 4. Configure in Hermes

Composio provides an MCP server that Hermes can connect to. Add the Composio MCP server to Hermes config at `/root/.hermes/mcp.json` (path may vary by Hermes version):

```json
{
  "mcpServers": {
    "composio": {
      "command": "composio-mcp",
      "args": ["--api-key", "${COMPOSIO_API_KEY}"]
    }
  }
}
```

Refer to [Composio MCP docs](https://docs.composio.dev/mcp) for the current setup instructions — the exact config format may change with Hermes or Composio releases.

### 5. Connect Apps

In the Composio dashboard, connect the apps you want (Gmail, Notion, etc.) and authorize them under your account. Hermes will be able to invoke those tools by name.

## Cost

Composio has a free tier (limited tool calls/month). Paid plans start around $29/mo for unlimited calls. Check [composio.dev/pricing](https://composio.dev/pricing) for current rates.
