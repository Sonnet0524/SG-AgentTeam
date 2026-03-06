#!/bin/bash
# ====================================
# Core Team Startup Script
# ====================================

echo
echo "========================================"
echo "  Core Team - Core Data Processing"
echo "========================================"
echo
echo "Working Directory: knowledge-assistant-dev"
echo
echo "Starting Core Team..."
echo

# Check if in correct directory (dev repo)
if [ ! -d "practice/agents/core" ]; then
    echo "Error: Not in dev repository!"
    echo "Please run this script from knowledge-assistant-dev root."
    exit 1
fi

# Check if main repo exists
if [ ! -d "../knowledge-assistant" ]; then
    echo "Warning: Main repository not found!"
    echo "Please ensure knowledge-assistant repo exists."
    read -p "Press Enter to continue..."
fi

echo
echo "Core Team ready!"
echo
echo "Remember:"
echo "  - You are responsible for: types, utils, extraction"
echo "  - DO NOT modify: embeddings, index, connectors"
echo "  - Edit permission: ASK before modifying"
echo "  - Test coverage: > 85% required"
echo
echo "Tasks: Check GitHub Issues with label 'team: core'"
echo
read -p "Press Enter to continue..."
