@echo off
REM ====================================
REM PM Team Startup Script
REM ====================================

echo.
echo ========================================
echo   PM Team - Project Manager
echo ========================================
echo.
echo Working Directory: knowledge-assistant-dev
echo.
echo Starting PM Team...
echo.

REM Check if in correct directory (dev repo)
if not exist "practice\agents\pm" (
    echo Error: Not in dev repository!
    echo Please run this script from knowledge-assistant-dev root.
    pause
    exit /b 1
)

REM Start OpenCode with PM Team
opencode --agent pm

pause
