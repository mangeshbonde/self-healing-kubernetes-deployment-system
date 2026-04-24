#!/bin/bash

echo "🚀 Starting Self-Healing System..."

# Activate venv
cd automation
source venv/bin/activate

# Start watcher in background
echo "Starting watcher..."
python3 watcher.py &
WATCHER_PID=$!

# Start dashboard
cd ../dashboard
echo "Starting dashboard..."
python3 app.py &
DASHBOARD_PID=$!

echo ""
echo "===================================="
echo "System is running ✅"
echo "Dashboard: http://<EC2-IP>:5000"
echo "===================================="

# Keep script running
wait