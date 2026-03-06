@echo off
REM ====================================
REM Integration Team Startup Script
REM ====================================

echo.
echo ========================================
echo   Integration Team - opencode Integration
echo ========================================
echo.
echo Working Directory: knowledge-assistant-dev
echo.
echo Starting Integration Team...
echo.

REM Check if in correct directory (dev repo)
if not exist "practice\agents\integration" (
    echo Error: Not in dev repository!
    echo Please run this script from knowledge-assistant-dev root.
    pause
    exit /b 1
)

REM Check if main repository exists
if not exist "..\knowledge-assistant" (
    echo Warning: Main repository not found!
    echo Please ensure knowledge-assistant repo exists.
)

echo.
echo Remember:
echo   - You are responsible for: skills, connectors, integration
echo   - DO NOT modify: embeddings, index, types, utils
echo   - Edit permission: ASK before modifying
echo   - Test coverage: ^> 85%% required
echo.
echo Tasks: Check GitHub Issues with label 'team: integration'
echo.
pause
