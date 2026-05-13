#!/usr/bin/env bash
# Tunnel public HTTPS -> local Flask (default http://127.0.0.1:5000).
#
# One-time setup:
#   1. Sign up: https://dashboard.ngrok.com/signup
#   2. Copy authtoken from: https://dashboard.ngrok.com/get-started/your-authtoken
#   3. Run: ngrok config add-authtoken YOUR_TOKEN
#
# Then start Flask (another terminal):  python app.py
# Then run this script:               ./start_ngrok.sh
#
# Use the printed "Forwarding" https URL from your Hostinger VPS (curl, scripts, etc.).
# Ngrok web UI on this machine: http://127.0.0.1:4040
#
# Optional: protect the tunnel (recommended):
#   NGROK_BASIC_AUTH='user:password' ./start_ngrok.sh
#
set -euo pipefail
PORT="${1:-5000}"
if [[ -n "${NGROK_BASIC_AUTH:-}" ]]; then
  # Example: NGROK_BASIC_AUTH='apiuser:astrongsecret' ./start_ngrok.sh
  exec ngrok http "$PORT" --basic-auth="$NGROK_BASIC_AUTH"
else
  exec ngrok http "$PORT"
fi
