"""
Pydantic models for API request/response schemas.

Defines all data models for the FastAPI backend.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# ==================== Search Models ====================

class SearchRequest(BaseModel):
    """Request model for semantic search."""
    
    query: str = Field(
        ...,
        description="Search query text",
        min_length=1,
        example="Python异步编程"
    )
    limit: int = Field(
        default=10,
        description="Maximum number of results",
        ge=1,
        le=100
    )
    offset: int = Field(
        default=0,
        description="Number of results to skip",
        ge=0
    )
    index_path: str = Field(
        default=".ka-index",
        description="Path to the index directory"
    )
    filters: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional metadata filters"
    )
    threshold: Optional[float] = Field(
        default=None,
        description="Minimum similarity threshold",
        ge=0.0,
        le=1.0
    )


class SearchResult(BaseModel):
    """Single search result."""
    
    rank: int = Field(..., description="Result ranking (1-based)")
    similarity: float = Field(..., description="Similarity score")
    snippet: str = Field(..., description="Text snippet (first 200 chars)")
    metadata: Dict[str, Any] = Field(..., description="Document metadata")
    index: int = Field(..., description="Chunk index in the index")
    
    class Config:
        json_schema_extra = {
            "example": {
                "rank": 1,
                "similarity": 0.85,
                "snippet": "Python是一种编程语言，支持异步编程...",
                "metadata": {"source": "doc1.md", "category": "programming"},
                "index": 0
            }
        }


class SearchResponse(BaseModel):
    """Response model for search results."""
    
    results: List[SearchResult] = Field(
        default_factory=list,
        description="List of search results"
    )
    total: int = Field(..., description="Total number of matching results")
    limit: int = Field(..., description="Results per page")
    offset: int = Field(..., description="Current offset")
    query_time_ms: float = Field(..., description="Query execution time in ms")
    
    class Config:
        json_schema_extra = {
            "example": {
                "results": [
                    {
                        "rank": 1,
                        "similarity": 0.85,
                        "snippet": "Python是一种编程语言...",
                        "metadata": {"source": "doc1.md"},
                        "index": 0
                    }
                ],
                "total": 42,
                "limit": 10,
                "offset": 0,
                "query_time_ms": 45.2
            }
        }


# ==================== Document Models ====================

class DocumentCreate(BaseModel):
    """Request model for creating a document."""
    
    content: str = Field(
        ...,
        description="Document content",
        min_length=1
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Document metadata"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "content": "这是一篇关于Python异步编程的文档...",
                "metadata": {
                    "source": "manual.md",
                    "category": "programming",
                    "author": "AI Team"
                }
            }
        }


class DocumentUpdate(BaseModel):
    """Request model for updating a document."""
    
    content: Optional[str] = Field(
        default=None,
        description="Updated document content"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Updated document metadata"
    )


class DocumentResponse(BaseModel):
    """Response model for a document."""
    
    id: str = Field(..., description="Document ID")
    content: str = Field(..., description="Document content")
    metadata: Dict[str, Any] = Field(..., description="Document metadata")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(
        default=None,
        description="Last update timestamp"
    )
    chunk_count: int = Field(
        default=0,
        description="Number of chunks in index"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "doc_123",
                "content": "Python异步编程指南...",
                "metadata": {"source": "guide.md", "category": "programming"},
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T14:20:00Z",
                "chunk_count": 3
            }
        }


class DocumentListResponse(BaseModel):
    """Response model for document list."""
    
    documents: List[DocumentResponse] = Field(
        default_factory=list,
        description="List of documents"
    )
    total: int = Field(..., description="Total number of documents")
    limit: int = Field(..., description="Results per page")
    offset: int = Field(..., description="Current offset")


# ==================== Connector Models ====================

class ConnectorInfo(BaseModel):
    """Information about a connector."""
    
    name: str = Field(..., description="Connector name")
    status: str = Field(
        ...,
        description="Connection status: connected, disconnected, error"
    )
    last_sync: Optional[datetime] = Field(
        default=None,
        description="Last synchronization time"
    )
    error: Optional[str] = Field(
        default=None,
        description="Error message if status is 'error'"
    )
    config: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Connector configuration (sensitive fields masked)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "email",
                "status": "connected",
                "last_sync": "2024-01-15T10:30:00Z",
                "error": None,
                "config": {
                    "server": "imap.gmail.com",
                    "username": "user@gmail.com",
                    "default_folder": "INBOX"
                }
            }
        }


class ConnectorStatus(BaseModel):
    """Response model for connector status."""
    
    connectors: List[ConnectorInfo] = Field(
        default_factory=list,
        description="List of connector statuses"
    )
    total: int = Field(..., description="Total number of connectors")
    
    class Config:
        json_schema_extra = {
            "example": {
                "connectors": [
                    {
                        "name": "email",
                        "status": "connected",
                        "last_sync": "2024-01-15T10:30:00Z",
                        "error": None,
                        "config": {"server": "imap.gmail.com"}
                    },
                    {
                        "name": "calendar",
                        "status": "disconnected",
                        "last_sync": None,
                        "error": None,
                        "config": None
                    }
                ],
                "total": 2
            }
        }


class ConnectorConnectRequest(BaseModel):
    """Request model for connecting a connector."""
    
    connector_name: str = Field(..., description="Name of connector to connect")
    config: Dict[str, Any] = Field(..., description="Connector configuration")
    
    class Config:
        json_schema_extra = {
            "example": {
                "connector_name": "email",
                "config": {
                    "server": "imap.gmail.com",
                    "port": 993,
                    "username": "user@gmail.com",
                    "password": "app_password_here"
                }
            }
        }


# ==================== Error Models ====================

class ErrorResponse(BaseModel):
    """Standard error response model."""
    
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional error details"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Error timestamp"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "NotFoundError",
                "message": "Index not found at path .ka-index",
                "details": {"path": ".ka-index"},
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }


# ==================== Health Check ====================

class HealthCheckResponse(BaseModel):
    """Response model for health check."""
    
    status: str = Field(..., description="Service status: ok, degraded, error")
    version: str = Field(..., description="API version")
    index_status: str = Field(..., description="Index status: available, not_found")
    uptime_seconds: float = Field(..., description="Service uptime in seconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "ok",
                "version": "1.2.0",
                "index_status": "available",
                "uptime_seconds": 3600.5
            }
        }
