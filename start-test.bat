@echo off
REM ====================================
REM Test Team Startup Script
REM ====================================

echo.
echo ========================================
echo   Test Team - Quality Assurance
echo ========================================
echo.
echo Working Directory: knowledge-assistant-dev
echo.
echo Starting Test Team...
echo.

REM Check if in correct directory (dev repo)
if not exist "practice\agents\test" (
    echo Error: Not in dev repository!
    echo Please run this script from knowledge-assistant-dev root.
    pause
    exit /b 1
)

REM Start OpenCode with Test Team
opencode --agent test

pause
