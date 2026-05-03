#!/usr/bin/env bash
# =============================================================================
# Speaker Agent VPS Setup
# Run this on the NEW VPS (Ubuntu 22.04+). Single command.
#
# Usage:
#   curl -sSL https://raw.githubusercontent.com/jbellsolutions/single-brain/main/scripts/speaker-agent-setup.sh | bash
#
# Or download and run:
#   chmod +x speaker-agent-setup.sh && ./speaker-agent-setup.sh
# =============================================================================
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}  Speaker Agent VPS Setup${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""

# ── Pre-flight checks ────────────────────────────────────────────
if [[ $EUID -eq 0 ]]; then
  echo -e "${RED}Do not run as root. Run as your normal user with sudo.${NC}"
  exit 1
fi

if ! command -v git &>/dev/null; then
  echo "Installing git..."
  sudo apt-get update -qq && sudo apt-get install -y -qq git
fi

# ── Python + venv ─────────────────────────────────────────────────
echo -e "${YELLOW}[1/6] Setting up Python...${NC}"
if ! command -v python3 &>/dev/null; then
  sudo apt-get install -y -qq python3 python3-pip python3-venv
fi

# ── Node.js (for MCP tools if needed) ────────────────────────────
if ! command -v node &>/dev/null; then
  echo -e "${YELLOW}[2/6] Installing Node.js...${NC}"
  curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
  sudo apt-get install -y -qq nodejs
fi

# ── Hermes Agent Install ──────────────────────────────────────────
echo -e "${YELLOW}[3/6] Installing Hermes Agent...${NC}"
if ! command -v hermes &>/dev/null; then
  curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
fi

# ── Speaker Agent Profile ─────────────────────────────────────────
echo -e "${YELLOW}[4/6] Creating Speaker Agent profile...${NC}"

HERMES_PROFILE_DIR="$HOME/.hermes/profiles/speaker-agent"
mkdir -p "$HERMES_PROFILE_DIR"

cat > "$HERMES_PROFILE_DIR/config.yaml" << 'HERMESCONF'
# Speaker Agent — isolated profile
# This agent only knows about the Speaker Agent project.
# It does NOT have access to AI Integraterz data, keys, or memory.

model:
  default: REPLACE_MODEL
  provider: openrouter
  base_url: https://openrouter.ai/api/v1

agent:
  max_turns: 60
  reasoning_effort: medium

terminal:
  backend: local
  cwd: /opt/speaker-agent

compression:
  enabled: true
  threshold: 0.5

memory:
  memory_enabled: true
  user_profile_enabled: false

display:
  personality: technical
  show_reasoning: false

skills:
  external_dirs: []
  template_vars: true

cron:
  wrap_response: true

approvals:
  mode: smart

security:
  redact_secrets: true
  tirith_enabled: true

# ── Vault sync (shared with Hermes) ──
# This is how Hermes and Speaker Agent communicate
VAULT_PATH: /opt/speaker-agent/vault
VAULT_REPO: jbellsolutions/single-brain
VAULT_SYNC_INTERVAL: 300

# ── Notion (same workspace, reads Speaker Agent DBs) ──
NOTION_TASKS_DB_ID: "3553fa00-4c9d-8164-99a2-e15c2c7e216a"
NOTION_SPRINTS_DB_ID: "3553fa00-4c9d-81b9-b194-db64b36e27bb"
NOTION_HEALTH_DB_ID: "3553fa00-4c9d-8174-b138-e569b05746ff"

# ── Repos ──
SPEAKER_FRONTEND_REPO: REPLACE_FRONTEND_REPO
SPEAKER_BACKEND_REPO: REPLACE_BACKEND_REPO
HERMESCONF

# ── API Keys (YOU fill these in) ──────────────────────────────────
cat > "$HERMES_PROFILE_DIR/.env" << 'ENVFILE'
# Speaker Agent — API Keys
# Fill these in with SEPARATE keys from Hermes (isolated billing)

# LLM Provider (use a DIFFERENT key than Hermes for separate billing)
OPENROUTER_API_KEY=sk-or-v1-YOUR_KEY_HERE

# Notion (can share Hermes' key — same workspace)
NOTION_API_KEY=ntn_YOUR_KEY_HERE

# GitHub (for pushing to Speaker Agent repos)
GITHUB_TOKEN=ghp_YOUR_TOKEN_HERE

# Slack (if Tony/Lester will chat with it)
SLACK_BOT_TOKEN=xoxb-YOUR_TOKEN_HERE
SLACK_APP_TOKEN=xapp-YOUR_TOKEN_HERE
ENVFILE

# ── Working directory ─────────────────────────────────────────────
echo -e "${YELLOW}[5/6] Setting up project directory...${NC}"

WORKDIR="/opt/speaker-agent"
sudo mkdir -p "$WORKDIR"
sudo chown "$USER:$USER" "$WORKDIR"

# Clone vault for handshake
git clone "git@github.com:jbellsolutions/single-brain.git" "$WORKDIR/vault" 2>/dev/null || {
  echo "SSH key required. Add your SSH key to GitHub first:"
  echo "  ssh-keygen -t ed25519 -C 'speaker-agent@vps'"
  echo "  cat ~/.ssh/id_ed25519.pub  # add to github.com/settings/keys"
  echo "Then re-run: git clone git@github.com:jbellsolutions/single-brain.git $WORKDIR/vault"
}

# Clone Speaker Agent repos
echo "Clone repos:"
echo "  cd $WORKDIR"
echo "  git clone REPLACE_FRONTEND_REPO frontend"
echo "  git clone REPLACE_BACKEND_REPO backend"

# ── Cron: vault sync every 5 minutes ──────────────────────────────
echo -e "${YELLOW}[6/6] Setting up cron jobs...${NC}"

SYNC_SCRIPT="$WORKDIR/scripts/vault-sync.sh"
mkdir -p "$WORKDIR/scripts"

cat > "$SYNC_SCRIPT" << 'SYNCSCRIPT'
#!/usr/bin/env bash
cd /opt/speaker-agent/vault
git pull origin main --rebase 2>/dev/null
if [[ -n $(git status --porcelain) ]]; then
  git add -A
  git commit -m "speaker-agent: auto-sync $(date -Iseconds)" 2>/dev/null
  git push origin main 2>/dev/null
fi
SYNCSCRIPT
chmod +x "$SYNC_SCRIPT"

# Add to crontab (idempotent)
(crontab -l 2>/dev/null | grep -v "vault-sync.sh"; echo "*/5 * * * * $SYNC_SCRIPT") | crontab -

# ── Done ──────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}  Speaker Agent VPS Ready${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo "NEXT STEPS (do these manually):"
echo ""
echo "1. Edit ~/.hermes/profiles/speaker-agent/.env"
echo "   → Fill in OPENROUTER_API_KEY, NOTION_API_KEY, GITHUB_TOKEN"
echo ""
echo "2. Edit ~/.hermes/profiles/speaker-agent/config.yaml"
echo "   → Replace REPLACE_MODEL (e.g. 'deepseek/deepseek-chat')"
echo "   → Replace REPLACE_FRONTEND_REPO and REPLACE_BACKEND_REPO"
echo ""
echo "3. Set up SSH key for GitHub:"
echo "   ssh-keygen -t ed25519 -C 'speaker-agent@vps'"
echo "   cat ~/.ssh/id_ed25519.pub  # → github.com/settings/keys"
echo ""
echo "4. Clone the repos:"
echo "   cd /opt/speaker-agent"
echo "   git clone <FRONTEND_REPO> frontend"
echo "   git clone <BACKEND_REPO> backend"
echo ""
echo "5. Create AGENTS.md in each repo root (I'll push templates)"
echo ""
echo "6. Start the agent:"
echo "   hermes --profile speaker-agent"
echo ""
echo "7. To chat with it via Slack, set up gateway:"
echo "   hermes --profile speaker-agent gateway setup"
echo "   hermes --profile speaker-agent gateway install"
echo "   hermes --profile speaker-agent gateway start"
echo ""
echo -e "${YELLOW}Hermes will push AGENTS.md templates to your repos.${NC}"
echo -e "${YELLOW}Once vault sync is live, Hermes will assign first tasks.${NC}"
