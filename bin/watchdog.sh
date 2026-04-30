#!/bin/bash
# Single Brain watchdog — runs every 60s via crontab.
# Restarts containers only if exited or dead (not just unhealthy).
# Docker's own restart: unless-stopped handles crashes; health checks are noisy
# during OpenClaw's long channel-init phase, so we leave 'unhealthy' alone.

set -euo pipefail
VAULT=/srv/single-brain/vault
DATE=$(date -u +%F)
LOGFILE=$VAULT/daily-logs/$DATE.md
mkdir -p "$VAULT/daily-logs"
[ -f "$LOGFILE" ] || echo "# $DATE - daily log" > "$LOGFILE"

check_and_heal() {
  local name=$1
  local status
  status=$(docker inspect "$name" --format '{{.State.Health.Status}}{{if not .State.Health}}{{.State.Status}}{{end}}' 2>/dev/null || echo "missing")

  case "$status" in
    healthy|running|unhealthy|starting)
      # healthy/running = good; unhealthy/starting = let Docker manage it
      ;;
    exited|dead|created|restarting)
      ts=$(date -u +%H:%M:%SZ)
      echo "" >> "$LOGFILE"
      echo "## $ts watchdog: $name was $status — restarting" >> "$LOGFILE"
      docker restart "$name" >> "$LOGFILE" 2>&1
      ;;
    missing)
      ts=$(date -u +%H:%M:%SZ)
      echo "" >> "$LOGFILE"
      echo "## $ts watchdog: $name CONTAINER MISSING — manual fix required" >> "$LOGFILE"
      ;;
  esac
}

check_and_heal openclaw-gateway
check_and_heal hermes
