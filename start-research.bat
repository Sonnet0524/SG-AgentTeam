@echo off
REM ====================================
REM Research Team Startup Script
REM ====================================

echo.
echo ========================================
echo   Research Team - Framework Researcher
echo ========================================
echo.
echo Working Directory: knowledge-assistant-dev
echo.
echo Research Focus: Agent Team Framework Design
echo Output Scope: docs/research/, docs/methodology/
echo.
echo Starting Research Team...
echo.

REM Check if in correct directory (dev repo)
if not exist "practice\agents\research" (
    echo Error: Not in dev repository!
    echo Please run this script from knowledge-assistant-dev root.
    pause
    exit /b 1
)

REM Start OpenCode with Research Team
opencode --agent research

pause
