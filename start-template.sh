#!/bin/bash
# ====================================
# Template Team Startup Script
# ====================================

echo ""
echo "========================================"
echo "  Template Team - Template System"
echo "========================================"
echo ""
echo "Working Directory: knowledge-assistant-dev"
echo ""
echo "Starting Template Team..."
echo ""

# Check if in correct directory (dev repo)
if [ ! -d "practice/agents/template" ]; then
    echo "Error: Not in dev repository!"
    echo "Please run this script from knowledge-assistant-dev root."
    exit 1
fi

# Start OpenCode with Template Team
opencode --agent template
