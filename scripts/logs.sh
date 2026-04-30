#!/bin/bash
# Tail live logs for a container.
# Usage: ./logs.sh [openclaw-gateway|hermes]

CONTAINER=${1:-openclaw-gateway}
echo "Tailing logs for $CONTAINER (Ctrl+C to stop)..."
ssh your-server "docker logs -f --tail=50 $CONTAINER 2>&1"
