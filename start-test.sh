#!/bin/bash
# ====================================
# Test Team Startup Script
# ====================================

echo ""
echo "========================================"
echo "  Test Team - Quality Assurance"
echo "========================================"
echo ""
echo "Working Directory: knowledge-assistant-dev"
echo ""
echo "Starting Test Team..."
echo ""

# Check if in correct directory (dev repo)
if [ ! -d "practice/agents/test" ]; then
    echo "Error: Not in dev repository!"
    echo "Please run this script from knowledge-assistant-dev root."
    exit 1
fi

# Start OpenCode with Test Team
opencode --agent test
