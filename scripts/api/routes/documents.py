"""
Document management API routes.

Provides CRUD operations for documents in the knowledge base.
"""

import os
import json
import uuid
import logging
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query, status

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ..models.schemas import (
    DocumentCreate,
    DocumentUpdate,
    DocumentResponse,
    DocumentListResponse,
    ErrorResponse
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/documents", tags=["documents"])

# In-memory document store (for demo purposes)
# In production, this would be a database
_documents_db: dict = {}
_documents_metadata_file = ".ka-documents/metadata.json"


def _load_documents_db():
    """Load documents metadata from disk."""
    global _documents_db
    
    if os.path.exists(_documents_metadata_file):
        try:
            with open(_documents_metadata_file, 'r', encoding='utf-8') as f:
                _documents_db = json.load(f)
            logger.info(f"Loaded {len(_documents_db)} documents from disk")
        except Exception as e:
            logger.warning(f"Failed to load documents metadata: {e}")
            _documents_db = {}


def _save_documents_db():
    """Save documents metadata to disk."""
    os.makedirs(os.path.dirname(_documents_metadata_file), exist_ok=True)
    
    try:
        with open(_documents_metadata_file, 'w', encoding='utf-8') as f:
            json.dump(_documents_db, f, ensure_ascii=False, indent=2, default=str)
        logger.info(f"Saved {len(_documents_db)} documents to disk")
    except Exception as e:
        logger.error(f"Failed to save documents metadata: {e}")


# Load on module import
_load_documents_db()


@router.get(
    "",
    response_model=DocumentListResponse,
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="List Documents",
    description="Retrieve a paginated list of all documents in the knowledge base."
)
async def list_documents(
    limit: int = Query(
        default=20,
        description="Maximum number of documents to return",
        ge=1,
        le=100
    ),
    offset: int = Query(
        default=0,
        description="Number of documents to skip",
        ge=0
    ),
    category: Optional[str] = Query(
        default=None,
        description="Filter by category"
    )
):
    """
    List all documents in the knowledge base.
    
    - **limit**: Maximum number of documents (1-100)
    - **offset**: Number of documents to skip (for pagination)
    - **category**: Optional category filter
    
    Returns a paginated list of documents with metadata.
    """
    try:
        # Get all documents
        documents = list(_documents_db.values())
        
        # Filter by category if specified
        if category:
            documents = [
                doc for doc in documents
                if doc.get('metadata', {}).get('category') == category
            ]
        
        # Sort by created_at (newest first)
        documents.sort(
            key=lambda d: d.get('created_at', ''),
            reverse=True
        )
        
        # Apply pagination
        total = len(documents)
        documents = documents[offset:offset + limit]
        
        # Convert to response models
        doc_responses = [
            DocumentResponse(
                id=doc['id'],
                content=doc['content'],
                metadata=doc.get('metadata', {}),
                created_at=datetime.fromisoformat(doc['created_at']) if isinstance(doc['created_at'], str) else doc['created_at'],
                updated_at=datetime.fromisoformat(doc['updated_at']) if doc.get('updated_at') and isinstance(doc['updated_at'], str) else doc.get('updated_at'),
                chunk_count=doc.get('chunk_count', 0)
            )
            for doc in documents
        ]
        
        return DocumentListResponse(
            documents=doc_responses,
            total=total,
            limit=limit,
            offset=offset
        )
        
    except Exception as e:
        logger.error(f"Failed to list documents: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": f"Failed to list documents: {str(e)}"
            }
        )


@router.post(
    "",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Create Document",
    description="Add a new document to the knowledge base."
)
async def create_document(document: DocumentCreate):
    """
    Create a new document.
    
    Request body:
    - **content**: Document content (required)
    - **metadata**: Optional metadata dictionary
    
    Returns the created document with assigned ID and timestamps.
    
    Note: Document will need to be indexed separately using the indexing API.
    """
    try:
        # Generate document ID
        doc_id = f"doc_{uuid.uuid4().hex[:12]}"
        
        # Create document record
        now = datetime.now()
        doc_record = {
            'id': doc_id,
            'content': document.content,
            'metadata': document.metadata or {},
            'created_at': now.isoformat(),
            'updated_at': None,
            'chunk_count': 0
        }
        
        # Save to database
        _documents_db[doc_id] = doc_record
        _save_documents_db()
        
        logger.info(f"Created document: {doc_id}")
        
        return DocumentResponse(
            id=doc_id,
            content=document.content,
            metadata=document.metadata or {},
            created_at=now,
            updated_at=None,
            chunk_count=0
        )
        
    except Exception as e:
        logger.error(f"Failed to create document: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": f"Failed to create document: {str(e)}"
            }
        )


@router.get(
    "/{doc_id}",
    response_model=DocumentResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Document not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Get Document",
    description="Retrieve a specific document by ID."
)
async def get_document(doc_id: str):
    """
    Get a document by ID.
    
    - **doc_id**: Document identifier
    
    Returns the full document with content and metadata.
    """
    doc = _documents_db.get(doc_id)
    
    if not doc:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "NotFoundError",
                "message": f"Document not found: {doc_id}",
                "details": {"doc_id": doc_id}
            }
        )
    
    return DocumentResponse(
        id=doc['id'],
        content=doc['content'],
        metadata=doc.get('metadata', {}),
        created_at=datetime.fromisoformat(doc['created_at']) if isinstance(doc['created_at'], str) else doc['created_at'],
        updated_at=datetime.fromisoformat(doc['updated_at']) if doc.get('updated_at') and isinstance(doc['updated_at'], str) else doc.get('updated_at'),
        chunk_count=doc.get('chunk_count', 0)
    )


@router.put(
    "/{doc_id}",
    response_model=DocumentResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        404: {"model": ErrorResponse, "description": "Document not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Update Document",
    description="Update an existing document's content or metadata."
)
async def update_document(doc_id: str, update: DocumentUpdate):
    """
    Update a document.
    
    - **doc_id**: Document identifier
    
    Request body (all fields optional):
    - **content**: Updated content
    - **metadata**: Updated metadata
    
    Returns the updated document.
    
    Note: If content is updated, the document will need to be re-indexed.
    """
    doc = _documents_db.get(doc_id)
    
    if not doc:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "NotFoundError",
                "message": f"Document not found: {doc_id}",
                "details": {"doc_id": doc_id}
            }
        )
    
    try:
        # Update fields
        now = datetime.now()
        
        if update.content is not None:
            doc['content'] = update.content
            doc['chunk_count'] = 0  # Reset chunk count, needs re-indexing
        
        if update.metadata is not None:
            doc['metadata'] = update.metadata
        
        doc['updated_at'] = now.isoformat()
        
        # Save
        _documents_db[doc_id] = doc
        _save_documents_db()
        
        logger.info(f"Updated document: {doc_id}")
        
        return DocumentResponse(
            id=doc['id'],
            content=doc['content'],
            metadata=doc.get('metadata', {}),
            created_at=datetime.fromisoformat(doc['created_at']),
            updated_at=now,
            chunk_count=doc.get('chunk_count', 0)
        )
        
    except Exception as e:
        logger.error(f"Failed to update document: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": f"Failed to update document: {str(e)}"
            }
        )


@router.delete(
    "/{doc_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": ErrorResponse, "description": "Document not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Delete Document",
    description="Remove a document from the knowledge base."
)
async def delete_document(doc_id: str):
    """
    Delete a document.
    
    - **doc_id**: Document identifier
    
    Returns 204 No Content on success.
    
    Note: This does not remove the document from the search index.
    The index needs to be rebuilt to remove deleted documents.
    """
    if doc_id not in _documents_db:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "NotFoundError",
                "message": f"Document not found: {doc_id}",
                "details": {"doc_id": doc_id}
            }
        )
    
    try:
        # Delete document
        del _documents_db[doc_id]
        _save_documents_db()
        
        logger.info(f"Deleted document: {doc_id}")
        
        return None
        
    except Exception as e:
        logger.error(f"Failed to delete document: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": f"Failed to delete document: {str(e)}"
            }
        )
