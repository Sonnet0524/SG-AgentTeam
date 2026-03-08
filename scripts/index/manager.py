"""
Index manager for coordinating vector store operations.

Provides high-level interface for index building and management.
v1.2: Added incremental indexing support for batch processing.
"""

import os
import time
import logging
from typing import List, Dict, Optional

from .vector_store import VectorStore

logger = logging.getLogger(__name__)


class IndexManager:
    """
    Manager for vector index operations.
    
    Coordinates between encoder and vector store to build
    and manage semantic indexes.
    
    v1.2: Supports incremental indexing for large datasets.
    
    Attributes:
        index_path: Path to store the index
        vector_store: VectorStore instance
    
    Example:
        >>> manager = IndexManager('.ka-index')
        >>> manager.build_index(vectors, metadata, chunks)
        >>> stats = manager.get_stats()
    """
    
    def __init__(self, index_path: str = '.ka-index'):
        """
        Initialize the index manager.
        
        Args:
            index_path: Path to store the index files
        """
        self.index_path = index_path
        self.vector_store: Optional[VectorStore] = None
        
        logger.info(f"IndexManager initialized with path: {index_path}")
    
    def initialize_empty_index(self, dimension: int = 512) -> None:
        """
        Initialize an empty vector store for incremental indexing.
        
        v1.2: Used for batch processing large datasets.
        
        Args:
            dimension: Vector dimension
        """
        self.vector_store = VectorStore(dimension=dimension)
        logger.info(f"Initialized empty index with dimension={dimension}")
    
    def add_to_index(
        self,
        vectors,
        metadata: List[Dict],
        chunks: List[str]
    ) -> int:
        """
        Add vectors to existing index incrementally.
        
        v1.2: Used for batch processing large datasets.
        
        Args:
            vectors: Numpy array of vectors
            metadata: List of metadata dicts
            chunks: List of text chunks
        
        Returns:
            Number of vectors added
        """
        if not self.vector_store:
            logger.error("Index not initialized. Call initialize_empty_index first.")
            return 0
        
        return self.vector_store.add_vectors(
            vectors,
            metadata=metadata,
            chunks=chunks
        )
    
    def build_index(
        self,
        vectors,
        metadata: List[Dict],
        chunks: List[str],
        dimension: int = 512
    ) -> Dict:
        """
        Build a new vector index.
        
        Args:
            vectors: Numpy array of vectors
            metadata: List of metadata dicts
            chunks: List of text chunks
            dimension: Vector dimension
        
        Returns:
            Dictionary with build statistics
        
        Example:
            >>> manager = IndexManager()
            >>> vectors = encoder.encode_texts(['text'])
            >>> result = manager.build_index(vectors, metadata, chunks)
        """
        start_time = time.time()
        
        # Create new vector store
        self.vector_store = VectorStore(dimension=dimension)
        
        # Add vectors
        n_added = self.vector_store.add_vectors(
            vectors,
            metadata=metadata,
            chunks=chunks
        )
        
        build_time = time.time() - start_time
        
        stats = {
            'success': True,
            'total_vectors': n_added,
            'build_time': f"{build_time:.2f}s",
            'build_time_seconds': build_time,
            'index_path': self.index_path
        }
        
        logger.info(
            f"Index built: {n_added} vectors in {build_time:.2f}s"
        )
        
        return stats
    
    def save_index(self) -> bool:
        """
        Save the current index to disk.
        
        Returns:
            True if successful
        """
        if not self.vector_store:
            logger.error("No vector store to save")
            return False
        
        return self.vector_store.save(self.index_path)
    
    def load_index(self) -> bool:
        """
        Load the index from disk.
        
        Returns:
            True if successful
        """
        self.vector_store = VectorStore()
        return self.vector_store.load(self.index_path)
    
    def search(
        self,
        query_vector,
        top_k: int = 5,
        filters: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Search the index with a query vector.
        
        Args:
            query_vector: Query embedding
            top_k: Number of results to return
            filters: Optional metadata filters
        
        Returns:
            List of search results with metadata
        
        Example:
            >>> manager = IndexManager()
            >>> manager.load_index()
            >>> query_vec = encoder.encode_query('search text')
            >>> results = manager.search(query_vec, top_k=5)
        """
        if not self.vector_store:
            logger.error("No vector store loaded")
            return []
        
        # Search
        distances, indices, metadata = self.vector_store.search(
            query_vector,
            top_k=top_k
        )
        
        # Build results
        results = []
        for i, (dist, idx_list, meta_list) in enumerate(
            zip(distances, indices, metadata)
        ):
            for j, (d, idx, meta) in enumerate(zip(dist, idx_list, meta_list)):
                # Skip invalid indices
                if idx < 0:
                    continue
                
                # Convert distance to similarity (for inner product)
                similarity = float(d)
                
                # Get chunk text
                chunk = self.vector_store.get_chunk(idx)
                
                result = {
                    'rank': j + 1,
                    'similarity': similarity,
                    'index': int(idx),
                    'metadata': meta,
                    'snippet': chunk[:200] if chunk else ''
                }
                
                # Apply filters if specified
                if filters:
                    if all(
                        meta.get(k) == v for k, v in filters.items()
                    ):
                        results.append(result)
                else:
                    results.append(result)
        
        return results[:top_k]
    
    def get_stats(self) -> Dict:
        """
        Get index statistics.
        
        Returns:
            Dictionary with index statistics
        """
        if not self.vector_store:
            return {
                'status': 'not_loaded',
                'index_path': self.index_path
            }
        
        stats = self.vector_store.get_stats()
        stats['index_path'] = self.index_path
        stats['status'] = 'loaded'
        
        # Add index file size if exists
        index_file = os.path.join(self.index_path, 'index.faiss')
        if os.path.exists(index_file):
            size_mb = os.path.getsize(index_file) / 1024 / 1024
            stats['index_size_mb'] = f"{size_mb:.2f} MB"
        
        return stats
    
    def clear_index(self) -> bool:
        """
        Clear the current index.
        
        Returns:
            True if successful
        """
        if self.vector_store:
            self.vector_store.clear()
            logger.info("Index cleared")
            return True
        return False
    
    def index_exists(self) -> bool:
        """
        Check if an index exists at the specified path.
        
        Returns:
            True if index files exist
        """
        index_file = os.path.join(self.index_path, 'index.faiss')
        meta_file = os.path.join(self.index_path, 'metadata.json')
        
        return os.path.exists(index_file) and os.path.exists(meta_file)
