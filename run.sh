#!/bin/bash

echo "🚀 Starting Self-Healing System..."

# Start watcher
cd automation
source venv/bin/activate
python3 watcher.py &
WATCHER_PID=$!

echo "Watcher running..."

# Start dashboard
cd ../dashboard
python3 app.py &
DASHBOARD_PID=$!

echo "Dashboard running..."

echo "🌐 Access Dashboard at: http://<EC2-IP>:5000"

wait