"""
API route modules.
"""

from .search import router as search_router
from .documents import router as documents_router
from .connectors import router as connectors_router

__all__ = ['search_router', 'documents_router', 'connectors_router']
