#!/bin/bash
set -e

APP_DIR="$(cd "$(dirname "$0")/nodeapp" && pwd)"

echo "[DEPLOY] Pulling latest code..."
cd "$APP_DIR"
git pull origin main

echo "[DEPLOY] Installing dependencies..."
npm install --production

echo "[DEPLOY] Stopping old instance..."
pkill -f "node app.js" || true
sleep 1

echo "[DEPLOY] Starting new instance..."
nohup node app.js > "$APP_DIR/app.log" 2>&1 &

echo "[DEPLOY] ✅ Done! PID: $!"
chmod +x deploy.sh