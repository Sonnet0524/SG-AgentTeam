@echo off
REM ====================================
REM Data Team Startup Script
REM ====================================

echo.
echo ========================================
echo   Data Team - Data System
echo ========================================
echo.
echo Working Directory: knowledge-assistant-dev
echo.
echo Starting Data Team...
echo.

REM Check if in correct directory (dev repo)
if not exist "practice\agents\data" (
    echo Error: Not in dev repository!
    echo Please run this script from knowledge-assistant-dev root.
    pause
    exit /b 1
)

REM Start OpenCode with Data Team
opencode --agent data

pause
