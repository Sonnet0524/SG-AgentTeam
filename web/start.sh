#!/bin/bash

# Knowledge Assistant Web UI Startup Script
# Starts both the API server and serves the web UI

echo "========================================="
echo "Knowledge Assistant Web UI"
echo "========================================="
echo ""

# Configuration
API_HOST="${KA_API_HOST:-0.0.0.0}"
API_PORT="${KA_API_PORT:-8000}"
WEB_PORT="${KA_WEB_PORT:-3000}"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to kill background processes on exit
cleanup() {
    echo ""
    echo "${YELLOW}Shutting down...${NC}"
    if [ ! -z "$API_PID" ]; then
        kill $API_PID 2>/dev/null
    fi
    if [ ! -z "$WEB_PID" ]; then
        kill $WEB_PID 2>/dev/null
    fi
    exit 0
}

trap cleanup SIGINT SIGTERM

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check if required Python packages are installed
echo "${BLUE}Checking dependencies...${NC}"
python3 -c "import fastapi" 2>/dev/null || {
    echo "Installing FastAPI..."
    pip install fastapi uvicorn python-multipart pydantic
}

# Start API server
echo ""
echo "${GREEN}Starting API server on http://${API_HOST}:${API_PORT}${NC}"
python3 scripts/api/main.py &
API_PID=$!

# Wait for API to start
sleep 2

# Check if API is running
if ! kill -0 $API_PID 2>/dev/null; then
    echo "Error: API server failed to start"
    exit 1
fi

echo ""
echo "${GREEN}API server started successfully${NC}"
echo "API Documentation: http://localhost:${API_PORT}/docs"
echo ""

# Start web server
echo "${GREEN}Starting web server on http://localhost:${WEB_PORT}${NC}"
echo ""

# Check if http.server is available
if python3 -c "import http.server" 2>/dev/null; then
    cd web
    python3 -m http.server $WEB_PORT &
    WEB_PID=$!
    cd ..
else
    echo "Error: Python http.server not available"
    cleanup
    exit 1
fi

# Open browser (optional)
if command -v open &> /dev/null; then
    sleep 1
    open "http://localhost:${WEB_PORT}"
elif command -v xdg-open &> /dev/null; then
    sleep 1
    xdg-open "http://localhost:${WEB_PORT}"
fi

echo ""
echo "========================================="
echo "${GREEN}Knowledge Assistant is running!${NC}"
echo "========================================="
echo ""
echo "Web UI:       http://localhost:${WEB_PORT}"
echo "API Docs:     http://localhost:${API_PORT}/docs"
echo "API ReDoc:    http://localhost:${API_PORT}/redoc"
echo ""
echo "Press Ctrl+C to stop the servers"
echo ""

# Wait for processes
wait
