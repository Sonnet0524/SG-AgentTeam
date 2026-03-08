"""
Search API routes.

Provides semantic search functionality via REST API.
"""

import time
import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from scripts.tools.search import semantic_search
from ..models.schemas import SearchRequest, SearchResponse, SearchResult, ErrorResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/search", tags=["search"])


@router.get(
    "",
    response_model=SearchResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid query"},
        404: {"model": ErrorResponse, "description": "Index not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Semantic Search",
    description="Perform semantic search on the knowledge base. Returns ranked results based on semantic similarity."
)
async def search(
    q: str = Query(
        ...,
        description="Search query text",
        min_length=1,
        example="Python异步编程"
    ),
    limit: int = Query(
        default=10,
        description="Maximum number of results",
        ge=1,
        le=100
    ),
    offset: int = Query(
        default=0,
        description="Number of results to skip (for pagination)",
        ge=0
    ),
    index_path: str = Query(
        default=".ka-index",
        description="Path to the index directory"
    ),
    threshold: Optional[float] = Query(
        default=None,
        description="Minimum similarity threshold (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
):
    """
    Perform semantic search on indexed documents.
    
    This endpoint searches the knowledge base using semantic similarity,
    returning the most relevant documents ranked by similarity score.
    
    - **q**: Search query (natural language, keywords, or questions)
    - **limit**: Maximum number of results to return (1-100)
    - **offset**: Number of results to skip (for pagination)
    - **index_path**: Path to the index directory
    - **threshold**: Optional minimum similarity threshold
    
    Returns ranked results with similarity scores and metadata.
    """
    start_time = time.time()
    
    try:
        # Perform semantic search
        results = semantic_search(
            query=q,
            index_path=index_path,
            top_k=limit + offset,  # Get extra for offset
            threshold=threshold
        )
        
        # Apply offset
        if offset > 0:
            results = results[offset:]
        
        # Convert to SearchResult models
        search_results = [
            SearchResult(
                rank=r['rank'],
                similarity=r['similarity'],
                snippet=r['snippet'],
                metadata=r['metadata'],
                index=r['index']
            )
            for r in results
        ]
        
        query_time = (time.time() - start_time) * 1000  # Convert to ms
        
        logger.info(f"Search completed: {len(search_results)} results in {query_time:.1f}ms")
        
        return SearchResponse(
            results=search_results,
            total=len(results),  # Note: This is approximate (we don't have total count)
            limit=limit,
            offset=offset,
            query_time_ms=round(query_time, 2)
        )
        
    except FileNotFoundError as e:
        logger.error(f"Index not found: {e}")
        raise HTTPException(
            status_code=404,
            detail={
                "error": "NotFoundError",
                "message": f"Index not found at path: {index_path}",
                "details": {"path": index_path}
            }
        )
    
    except Exception as e:
        logger.error(f"Search failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": f"Search failed: {str(e)}",
                "details": {"query": q}
            }
        )


@router.post(
    "",
    response_model=SearchResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        404: {"model": ErrorResponse, "description": "Index not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Semantic Search (POST)",
    description="Perform semantic search with full request body support including filters."
)
async def search_post(request: SearchRequest):
    """
    Perform semantic search with POST request.
    
    This endpoint supports advanced search options including metadata filters.
    
    Request body:
    - **query**: Search query text (required)
    - **limit**: Maximum number of results (default: 10)
    - **offset**: Number of results to skip (default: 0)
    - **index_path**: Path to the index directory (default: ".ka-index")
    - **filters**: Optional metadata filters
    - **threshold**: Optional minimum similarity threshold
    """
    start_time = time.time()
    
    try:
        # Perform semantic search
        results = semantic_search(
            query=request.query,
            index_path=request.index_path,
            top_k=request.limit + request.offset,
            filters=request.filters,
            threshold=request.threshold
        )
        
        # Apply offset
        if request.offset > 0:
            results = results[request.offset:]
        
        # Convert to SearchResult models
        search_results = [
            SearchResult(
                rank=r['rank'],
                similarity=r['similarity'],
                snippet=r['snippet'],
                metadata=r['metadata'],
                index=r['index']
            )
            for r in results
        ]
        
        query_time = (time.time() - start_time) * 1000
        
        logger.info(f"POST search completed: {len(search_results)} results in {query_time:.1f}ms")
        
        return SearchResponse(
            results=search_results,
            total=len(results),
            limit=request.limit,
            offset=request.offset,
            query_time_ms=round(query_time, 2)
        )
        
    except FileNotFoundError as e:
        logger.error(f"Index not found: {e}")
        raise HTTPException(
            status_code=404,
            detail={
                "error": "NotFoundError",
                "message": f"Index not found at path: {request.index_path}",
                "details": {"path": request.index_path}
            }
        )
    
    except Exception as e:
        logger.error(f"Search failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": f"Search failed: {str(e)}",
                "details": {"query": request.query}
            }
        )
