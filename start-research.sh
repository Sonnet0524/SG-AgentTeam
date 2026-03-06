#!/bin/bash
# ====================================
# Research Team Startup Script
# ====================================

echo ""
echo "========================================"
echo "  Research Team - Framework Researcher"
echo "========================================"
echo ""
echo "Working Directory: knowledge-assistant-dev"
echo ""
echo "Research Focus: Agent Team Framework Design"
echo "Output Scope: docs/research/, docs/methodology/"
echo ""
echo "Starting Research Team..."
echo ""

# Check if in correct directory (dev repo)
if [ ! -d "practice/agents/research" ]; then
    echo "Error: Not in dev repository!"
    echo "Please run this script from knowledge-assistant-dev root."
    exit 1
fi

# Start OpenCode with Research Team
opencode --agent research
