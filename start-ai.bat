@echo off
REM ====================================
REM AI Team Startup Script
REM ====================================

echo.
echo ========================================
echo   AI Team - AI & Semantic Search
echo ========================================
echo.
echo Working Directory: knowledge-assistant-dev
echo.
echo Starting AI Team...
echo.

REM Check if in correct directory (dev repo)
if not exist "practice\agents\ai" (
    echo Error: Not in dev repository!
    echo Please run this script from knowledge-assistant-dev root.
    pause
    exit /b 1
)

REM Check if main repo exists
if not exist "..\knowledge-assistant" (
    echo Warning: Main repository not found!
    echo Please ensure knowledge-assistant repo exists.
    pause
)

echo.
echo AI Team ready!
echo.
echo Remember:
echo   - You are responsible for: embeddings, vector index, semantic search
echo   - DO NOT modify: types, utils, extraction, connectors
echo   - Edit permission: ASK before modifying
echo   - Test coverage: > 85%% required
echo   - Install dependencies: pip install sentence-transformers faiss-cpu
echo.
echo Tasks: Check GitHub Issues with label 'team: ai'
echo.
pause
