"""
Tools module for semantic indexing, search, and knowledge extraction.

Provides high-level API functions for building and searching indexes,
and extracting keywords and summaries from text.
"""

from .indexing import build_semantic_index
from .search import semantic_search
from .extraction import extract_keywords, generate_summary

__all__ = [
    'build_semantic_index',
    'semantic_search',
    'extract_keywords',
    'generate_summary'
]
