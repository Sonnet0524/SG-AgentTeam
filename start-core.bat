@echo off
REM ====================================
REM Core Team Startup Script
REM ====================================

echo.
echo ========================================
echo   Core Team - Core Data Processing
echo ========================================
echo.
echo Working Directory: knowledge-assistant-dev
echo.
echo Starting Core Team...
echo.

REM Check if in correct directory (dev repo)
if not exist "practice\agents\core" (
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
echo Core Team ready!
echo.
echo Remember:
echo   - You are responsible for: types, utils, extraction
echo   - DO NOT modify: embeddings, index, connectors
echo   - Edit permission: ASK before modifying
echo   - Test coverage: ^> 85%% required
echo.
echo Tasks: Check GitHub Issues with label 'team: core'
echo.
pause

REM Start OpenCode with Core Team
opencode --agent core
