#!/bin/bash
# Open the OpenClaw UI in your browser via SSH tunnel.
# The gateway runs on localhost-only — requires this tunnel.

PORT=18789

# Kill any existing tunnel on this port
lsof -ti tcp:$PORT | xargs kill -9 2>/dev/null

echo "Opening SSH tunnel → single-brain:$PORT"
ssh -fNL ${PORT}:127.0.0.1:${PORT} single-brain

sleep 1
echo "Opening http://localhost:$PORT ..."
open "http://localhost:$PORT"

echo ""
echo "Tunnel is running in background. To close it:"
echo "  lsof -ti tcp:$PORT | xargs kill -9"
