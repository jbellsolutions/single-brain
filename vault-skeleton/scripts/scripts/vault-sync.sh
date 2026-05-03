#!/usr/bin/env bash
# Vault auto-sync: commit and push any changes every run
# Called by cron every 15 minutes

VAULT="/opt/data/obsidian-vault"
cd "$VAULT" || exit 1

# Pull latest from remote first (if remote exists)
git pull --rebase origin main 2>/dev/null || true

# Stage all changes
git add -A

# Check if there are changes to commit
if git diff --cached --quiet; then
    exit 0  # Nothing to commit
fi

# Commit with timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M ET')
git commit -m "vault sync: ${TIMESTAMP}" --quiet

# Push if remote exists
git push origin main 2>/dev/null || true
