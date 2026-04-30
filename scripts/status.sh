#!/bin/bash
# Show Single Brain stack status: containers, recent logs, last watchdog entry.

echo "=== Container Status ==="
ssh single-brain "cd /srv/single-brain && docker compose ps"

echo ""
echo "=== Last 10 OpenClaw Log Lines ==="
ssh single-brain "docker logs --tail=10 openclaw-gateway 2>&1"

echo ""
echo "=== Last 10 Hermes Log Lines ==="
ssh single-brain "docker logs --tail=10 hermes 2>&1"

echo ""
echo "=== Last Watchdog Entry ==="
ssh single-brain "tail -20 /srv/single-brain/vault/daily-logs/\$(date -u +%F).md 2>/dev/null || echo 'No log for today yet.'"
