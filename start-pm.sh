#!/bin/bash
# ====================================
# PM Team Startup Script
# ====================================

echo ""
echo "========================================"
echo "  PM Team - Project Manager"
echo "========================================"
echo ""
echo "Working Directory: knowledge-assistant-dev"
echo ""
echo "Starting PM Team..."
echo ""

# Check if in correct directory (dev repo)
if [ ! -d "practice/agents/pm" ]; then
    echo "Error: Not in dev repository!"
    echo "Please run this script from knowledge-assistant-dev root."
    exit 1
fi

# Start OpenCode with PM Team
opencode --agent pm
