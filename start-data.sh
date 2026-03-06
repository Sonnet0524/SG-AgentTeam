#!/bin/bash
# ====================================
# Data Team Startup Script
# ====================================

echo ""
echo "========================================"
echo "  Data Team - Data System"
echo "========================================"
echo ""
echo "Working Directory: knowledge-assistant-dev"
echo ""
echo "Starting Data Team..."
echo ""

# Check if in correct directory (dev repo)
if [ ! -d "practice/agents/data" ]; then
    echo "Error: Not in dev repository!"
    echo "Please run this script from knowledge-assistant-dev root."
    exit 1
fi

# Start OpenCode with Data Team
opencode --agent data
