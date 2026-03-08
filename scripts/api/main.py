"""
FastAPI Main Application.

Knowledge Assistant Backend API for v1.2.
Provides REST API endpoints for semantic search, document management, and connector status.
"""

import os
import sys
import time
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.api.routes import search_router, documents_router, connectors_router
from scripts.api.models.schemas import ErrorResponse, HealthCheckResponse
from scripts.index.manager import IndexManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global variables
START_TIME = time.time()
APP_VERSION = "1.2.0"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("=" * 60)
    logger.info(f"Knowledge Assistant API v{APP_VERSION}")
    logger.info("=" * 60)
    logger.info("Starting application...")
    
    # Check if index exists
    index_path = os.environ.get("KA_INDEX_PATH", ".ka-index")
    if os.path.exists(os.path.join(index_path, "index.faiss")):
        logger.info(f"Index found at {index_path}")
    else:
        logger.warning(f"No index found at {index_path}. Build an index first.")
    
    logger.info("Application started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    logger.info("Application stopped")


# Create FastAPI application
app = FastAPI(
    title="Knowledge Assistant API",
    description="""
## Knowledge Assistant Backend API

Provides REST API endpoints for semantic search, document management, and connector integration.

### Features

- **Semantic Search**: Search documents using natural language queries
- **Document Management**: CRUD operations for knowledge base documents
- **Connector Status**: Monitor and manage data source connections

### Quick Start

1. Build an index using the indexing tools
2. Start the API server: `uvicorn scripts.api.main:app --reload`
3. Access the API documentation at `/docs`
4. Use the search endpoint to query your knowledge base

### Version

Current version: v1.2.0
    """,
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "*"  # Allow all origins in development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with detailed messages."""
    logger.warning(f"Validation error: {exc}")
    
    # Extract error details
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "ValidationError",
            "message": "Request validation failed",
            "details": {"errors": errors},
            "timestamp": datetime.now().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors."""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred",
            "details": {"error_type": type(exc).__name__},
            "timestamp": datetime.now().isoformat()
        }
    )


# Include routers
app.include_router(search_router, prefix="")
app.include_router(documents_router, prefix="")
app.include_router(connectors_router, prefix="")


# Root endpoint
@app.get(
    "/",
    summary="Root endpoint",
    description="Returns basic API information",
    tags=["root"]
)
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Knowledge Assistant API",
        "version": APP_VERSION,
        "docs": "/docs",
        "health": "/health"
    }


# Health check endpoint
@app.get(
    "/health",
    response_model=HealthCheckResponse,
    summary="Health Check",
    description="Check the health status of the API and its dependencies",
    tags=["health"]
)
async def health_check():
    """
    Health check endpoint.
    
    Returns the current status of the API service, including:
    - Service status (ok/degraded/error)
    - Version information
    - Index availability
    - Uptime
    """
    # Check index status
    index_path = os.environ.get("KA_INDEX_PATH", ".ka-index")
    index_manager = IndexManager(index_path=index_path)
    index_exists = index_manager.index_exists()
    
    # Determine overall status
    if index_exists:
        status_value = "ok"
    else:
        status_value = "degraded"
    
    return HealthCheckResponse(
        status=status_value,
        version=APP_VERSION,
        index_status="available" if index_exists else "not_found",
        uptime_seconds=time.time() - START_TIME
    )


# API info endpoint
@app.get(
    "/api",
    summary="API Info",
    description="Get information about available API endpoints",
    tags=["root"]
)
async def api_info():
    """Get API information and available endpoints."""
    return {
        "version": APP_VERSION,
        "endpoints": {
            "search": {
                "GET /api/search": "Search documents (query params)",
                "POST /api/search": "Search documents (request body)"
            },
            "documents": {
                "GET /api/documents": "List documents",
                "POST /api/documents": "Create document",
                "GET /api/documents/{id}": "Get document",
                "PUT /api/documents/{id}": "Update document",
                "DELETE /api/documents/{id}": "Delete document"
            },
            "connectors": {
                "GET /api/connectors/status": "Get all connector statuses",
                "POST /api/connectors/connect": "Connect a connector",
                "POST /api/connectors/disconnect": "Disconnect a connector",
                "GET /api/connectors/{name}/status": "Get specific connector status"
            }
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json"
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment
    host = os.environ.get("KA_API_HOST", "0.0.0.0")
    port = int(os.environ.get("KA_API_PORT", "8000"))
    reload = os.environ.get("KA_API_RELOAD", "true").lower() == "true"
    
    logger.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        "scripts.api.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
