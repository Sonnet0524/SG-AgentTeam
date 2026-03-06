@echo off
REM ====================================
REM Template Team Startup Script
REM ====================================

echo.
echo ========================================
echo   Template Team - Template System
echo ========================================
echo.
echo Working Directory: knowledge-assistant-dev
echo.
echo Starting Template Team...
echo.

REM Check if in correct directory (dev repo)
if not exist "practice\agents\template" (
    echo Error: Not in dev repository!
    echo Please run this script from knowledge-assistant-dev root.
    pause
    exit /b 1
)

REM Start OpenCode with Template Team
opencode --agent template

pause
