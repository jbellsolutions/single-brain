#!/bin/bash
# Restart one or both containers.
# Usage: ./restart.sh [openclaw-gateway|hermes|all]

TARGET=${1:-all}

if [[ "$TARGET" == "all" ]]; then
  echo "Restarting all containers..."
  ssh single-brain "cd /srv/single-brain && docker compose restart"
elif [[ "$TARGET" == "openclaw-gateway" || "$TARGET" == "hermes" ]]; then
  echo "Restarting $TARGET..."
  ssh single-brain "cd /srv/single-brain && docker compose restart $TARGET"
else
  echo "Usage: $0 [openclaw-gateway|hermes|all]"
  exit 1
fi

echo ""
echo "Waiting 5s for containers to come up..."
sleep 5
ssh single-brain "cd /srv/single-brain && docker compose ps"
