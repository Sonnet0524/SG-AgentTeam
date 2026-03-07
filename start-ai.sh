#!/bin/bash
# ====================================
# AI Team Startup Script
# ====================================

echo
echo "========================================"
echo "  AI Team - AI & Semantic Search"
echo "========================================"
echo
echo "Working Directory: knowledge-assistant-dev"
echo
echo "Starting AI Team..."
echo

# Check if in correct directory (dev repo)
if [ ! -d "practice/agents/ai" ]; then
    echo "Error: Not in dev repository!"
    echo "Please run this script from knowledge-assistant-dev root."
    exit 1
fi

# Check if main repo exists
if [ ! -d "../knowledge-assistant" ]; then
    echo "Warning: Main repository not found!"
    echo "Please ensure knowledge-assistant repo exists."
fi

echo
echo "AI Team ready!"
echo
echo "Remember:"
echo "  - You are responsible for: embeddings, vector index, semantic search"
echo "  - DO NOT modify: types, utils, extraction, connectors"
echo "  - Edit permission: ASK before modifying"
echo "  - Test coverage: > 85% required"
echo "  - Install dependencies: pip install sentence-transformers faiss-cpu"
echo
echo "Tasks: Check GitHub Issues with label 'team: ai'"
echo
read -p "Press Enter to continue..."

# Start OpenCode with AI Team
opencode --agent ai
