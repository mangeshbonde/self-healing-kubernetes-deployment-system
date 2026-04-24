#!/bin/bash

echo "🚀 Starting Self-Healing System..."

PROJECT_DIR=$(pwd)

# Define venv python explicitly
VENV_PYTHON="$PROJECT_DIR/automation/venv/bin/python"

# Check if venv exists
if [ ! -f "$VENV_PYTHON" ]; then
    echo "❌ Virtual environment not found. Run setup.sh first."
    exit 1
fi

# Start watcher using venv python
echo "Starting watcher..."
cd automation
$VENV_PYTHON watcher.py &
WATCHER_PID=$!

# Start dashboard using same venv python
echo "Starting dashboard..."
cd ../dashboard
$VENV_PYTHON app.py &
DASHBOARD_PID=$!

echo ""
echo "===================================="
echo "System is running ✅"
echo "Dashboard: http://<EC2-IP>:5000"
echo "===================================="

wait