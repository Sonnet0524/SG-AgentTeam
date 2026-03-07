#!/bin/bash
# ====================================
# Integration Team Startup Script
# ====================================

echo
echo "========================================"
echo "  Integration Team - opencode Integration"
echo "========================================"
echo
echo "Working Directory: knowledge-assistant-dev"
echo
echo "Starting Integration Team..."
echo

# Check if in correct directory (dev repo)
if [ ! -d "practice/agents/integration" ]; then
    echo "Error: Not in dev repository!"
    echo "Please run this script from knowledge-assistant-dev root."
    exit 1
fi

# Check if main repository exists
if [ ! -d "../knowledge-assistant" ]; then
    echo "Warning: Main repository not found!"
    echo "Please ensure knowledge-assistant repo exists."
fi

echo
echo "Remember:"
echo "  - You are responsible for: skills, connectors, integration"
echo "  - DO NOT modify: embeddings, index, types, utils"
echo "  - Edit permission: ASK before modifying"
echo "  - Test coverage: > 85% required"
echo
echo "Tasks: Check GitHub Issues with label 'team: integration'"
echo
read -p "Press Enter to continue..."
