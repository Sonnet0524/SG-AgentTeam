"""
Vector store using FAISS for efficient similarity search.

Provides HNSW-based vector indexing and retrieval.
v1.2: Added memory mapping and index compression for large-scale datasets.
"""

import faiss
import numpy as np
import os
import json
from typing import List, Dict, Optional, Tuple
import logging
import pickle

logger = logging.getLogger(__name__)


class VectorStore:
    """
    FAISS-based vector store for semantic search.
    
    Uses HNSW (Hierarchical Navigable Small World) index for fast
    approximate nearest neighbor search.
    
    v1.2: Supports memory-mapped indices and compression for large datasets.
    
    Attributes:
        dimension: Vector dimension
        n_connections: HNSW connections per node (M parameter)
        index: FAISS index instance
        metadata_store: List of metadata for each vector
        use_mmap: Whether to use memory mapping for large indices
    
    Example:
        >>> store = VectorStore(dimension=512)
        >>> vectors = np.random.rand(100, 512).astype('float32')
        >>> store.add_vectors(vectors)
        >>> results = store.search(vectors[0:1], top_k=5)
    """
    
    def __init__(
        self,
        dimension: int = 512,
        n_connections: int = 32,
        use_compression: bool = False,
        compression_bits: int = 8
    ):
        """
        Initialize the vector store.
        
        Args:
            dimension: Vector dimension (default: 512 for bge-small-zh)
            n_connections: HNSW M parameter - connections per node (default: 32)
            use_compression: Use PQ compression for memory efficiency (default: False)
            compression_bits: Bits per subvector for PQ compression (default: 8)
        """
        self.dimension = dimension
        self.n_connections = n_connections
        self.use_compression = use_compression
        self.compression_bits = compression_bits
        self._mmap_mode = False
        
        # Create appropriate index type
        if use_compression:
            # Use IVF + PQ for memory efficiency
            nlist = 100  # Number of clusters
            # Create quantizer first
            quantizer = faiss.IndexHNSWFlat(dimension, n_connections)
            self.index = faiss.IndexIVFPQ(quantizer, dimension, nlist, 8, compression_bits)
            self._is_trained = False
            logger.info(
                f"VectorStore initialized with IVF-PQ compression: "
                f"dimension={dimension}, nlist={nlist}, bits={compression_bits}"
            )
        else:
            # Standard HNSW index
            self.index = faiss.IndexHNSWFlat(dimension, n_connections)
            self._is_trained = True
            # HNSW parameters
            self.index.hnsw.efSearch = 32  # Search depth
            self.index.hnsw.efConstruction = 40  # Construction depth
            logger.info(
                f"VectorStore initialized: dimension={dimension}, "
                f"connections={n_connections}"
            )
        
        # Metadata storage
        self.metadata_store: List[Dict] = []
        self.chunk_store: List[str] = []
    
    def add_vectors(
        self,
        vectors: np.ndarray,
        metadata: Optional[List[Dict]] = None,
        chunks: Optional[List[str]] = None
    ) -> int:
        """
        Add vectors to the index.
        
        Args:
            vectors: Numpy array of vectors with shape (n, dimension)
            metadata: Optional list of metadata dicts for each vector
            chunks: Optional list of text chunks for each vector
        
        Returns:
            Number of vectors added
        
        Example:
            >>> store = VectorStore(512)
            >>> vectors = np.random.rand(10, 512).astype('float32')
            >>> n = store.add_vectors(vectors)
            >>> print(n)
            10
        """
        if len(vectors) == 0:
            return 0
        
        # Ensure float32 type
        if vectors.dtype != np.float32:
            vectors = vectors.astype(np.float32)
        
        # Add to index
        n_added = self.index.ntotal
        self.index.add(vectors)
        n_total = self.index.ntotal
        
        # Store metadata
        if metadata:
            self.metadata_store.extend(metadata)
        else:
            # Add empty metadata
            self.metadata_store.extend([{}] * len(vectors))
        
        # Store chunks
        if chunks:
            self.chunk_store.extend(chunks)
        else:
            self.chunk_store.extend([''] * len(vectors))
        
        logger.debug(f"Added {n_total - n_added} vectors. Total: {n_total}")
        
        return n_total - n_added
    
    def search(
        self,
        query_vectors: np.ndarray,
        top_k: int = 5,
        threshold: Optional[float] = None
    ) -> Tuple[np.ndarray, np.ndarray, List[Dict]]:
        """
        Search for similar vectors.
        
        Args:
            query_vectors: Query vectors with shape (n_queries, dimension)
            top_k: Number of results to return per query
            threshold: Optional similarity threshold (not used in HNSW)
        
        Returns:
            Tuple of (distances, indices, metadata_list)
        
        Example:
            >>> store = VectorStore(512)
            >>> # Add some vectors...
            >>> query = np.random.rand(1, 512).astype('float32')
            >>> distances, indices, metadata = store.search(query, top_k=5)
        """
        if self.index.ntotal == 0:
            return (
                np.array([]).reshape(0, 0),
                np.array([]).reshape(0, 0),
                []
            )
        
        # Ensure float32
        if query_vectors.dtype != np.float32:
            query_vectors = query_vectors.astype(np.float32)
        
        # Search
        distances, indices = self.index.search(query_vectors, top_k)
        
        # Get metadata for results
        metadata_list = []
        for idx_array in indices:
            meta = [self.metadata_store[i] for i in idx_array if i >= 0]
            metadata_list.append(meta)
        
        return distances, indices, metadata_list
    
    def get_vector_count(self) -> int:
        """
        Get the number of vectors in the index.
        
        Returns:
            Number of vectors
        """
        return self.index.ntotal
    
    def get_metadata(self, index: int) -> Optional[Dict]:
        """
        Get metadata for a specific vector index.
        
        Args:
            index: Vector index
        
        Returns:
            Metadata dict or None if index out of range
        """
        if 0 <= index < len(self.metadata_store):
            return self.metadata_store[index]
        return None
    
    def get_chunk(self, index: int) -> Optional[str]:
        """
        Get text chunk for a specific vector index.
        
        Args:
            index: Vector index
        
        Returns:
            Text chunk or None if index out of range
        """
        if 0 <= index < len(self.chunk_store):
            return self.chunk_store[index]
        return None
    
    def save(self, index_path: str, use_mmap: bool = False) -> bool:
        """
        Save the vector store to disk.
        
        v1.2: Added memory-mapped index support for large datasets.
        
        Args:
            index_path: Directory path to save the index
            use_mmap: Save in memory-mappable format (default: False)
        
        Returns:
            True if successful
        
        Example:
            >>> store = VectorStore(512)
            >>> # Add vectors...
            >>> store.save('.ka-index')
        """
        try:
            os.makedirs(index_path, exist_ok=True)
            
            # Save FAISS index
            index_file = os.path.join(index_path, 'index.faiss')
            faiss.write_index(self.index, index_file)
            
            # Save metadata and chunks
            meta_file = os.path.join(index_path, 'metadata.json')
            with open(meta_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'dimension': self.dimension,
                    'n_connections': self.n_connections,
                    'use_compression': self.use_compression,
                    'compression_bits': self.compression_bits,
                    'metadata_store': self.metadata_store,
                    'chunk_store': self.chunk_store
                }, f, ensure_ascii=False, indent=2)
            
            # Save config for mmap support
            config_file = os.path.join(index_path, 'config.pkl')
            with open(config_file, 'wb') as f:
                pickle.dump({
                    'use_mmap': use_mmap,
                    'use_compression': self.use_compression
                }, f)
            
            logger.info(f"VectorStore saved to {index_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save VectorStore: {e}")
            return False
    
    def load(self, index_path: str, use_mmap: bool = False) -> bool:
        """
        Load the vector store from disk.
        
        v1.2: Added memory-mapped loading for reduced memory footprint.
        
        Args:
            index_path: Directory path containing saved index
            use_mmap: Load index with memory mapping (default: False)
                Memory mapping allows loading indices larger than RAM.
        
        Returns:
            True if successful
        
        Example:
            >>> store = VectorStore(512)
            >>> store.load('.ka-index', use_mmap=True)
        """
        try:
            # Load FAISS index
            index_file = os.path.join(index_path, 'index.faiss')
            if not os.path.exists(index_file):
                logger.error(f"Index file not found: {index_file}")
                return False
            
            if use_mmap:
                # Use IO reader for memory mapping
                self.index = faiss.read_index(index_file, faiss.IO_FLAG_MMAP)
                self._mmap_mode = True
                logger.info(f"Index loaded with memory mapping from {index_path}")
            else:
                self.index = faiss.read_index(index_file)
                self._mmap_mode = False
            
            # Load metadata and chunks
            meta_file = os.path.join(index_path, 'metadata.json')
            with open(meta_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.dimension = data.get('dimension', self.dimension)
                self.n_connections = data.get('n_connections', self.n_connections)
                self.use_compression = data.get('use_compression', False)
                self.compression_bits = data.get('compression_bits', 8)
                self.metadata_store = data.get('metadata_store', [])
                self.chunk_store = data.get('chunk_store', [])
            
            logger.info(
                f"VectorStore loaded from {index_path}. "
                f"Vectors: {self.index.ntotal}, MMap: {self._mmap_mode}"
            )
            return True
            
        except Exception as e:
            logger.error(f"Failed to load VectorStore: {e}")
            return False
    
    def clear(self) -> None:
        """
        Clear all vectors and metadata from the store.
        """
        # Recreate appropriate index type
        if self.use_compression:
            quantizer = faiss.IndexHNSWFlat(self.dimension, self.n_connections)
            self.index = faiss.IndexIVFPQ(quantizer, self.dimension, 100, 8, self.compression_bits)
            self._is_trained = False
        else:
            self.index = faiss.IndexHNSWFlat(self.dimension, self.n_connections)
            self._is_trained = True
            self.index.hnsw.efSearch = 32
            self.index.hnsw.efConstruction = 40
        
        # Clear metadata
        self.metadata_store = []
        self.chunk_store = []
        
        logger.info("VectorStore cleared")
    
    def get_stats(self) -> Dict:
        """
        Get statistics about the vector store.
        
        Returns:
            Dictionary with store statistics
        """
        stats = {
            'total_vectors': self.index.ntotal,
            'dimension': self.dimension,
            'n_connections': self.n_connections,
            'metadata_count': len(self.metadata_store),
            'chunk_count': len(self.chunk_store),
            'use_compression': self.use_compression,
            'mmap_mode': self._mmap_mode
        }
        
        # Add memory usage estimate
        stats['estimated_memory_mb'] = self._estimate_memory_usage()
        
        return stats
    
    def _estimate_memory_usage(self) -> float:
        """
        Estimate memory usage in MB.
        
        Returns:
            Estimated memory in MB
        """
        # Vector memory
        n_vectors = self.index.ntotal
        dimension = self.dimension
        
        if self.use_compression:
            # PQ uses less memory (approximately bits/8 bytes per vector)
            vector_memory = n_vectors * dimension * (self.compression_bits / 8) / 8
        else:
            # Float32 = 4 bytes per dimension
            vector_memory = n_vectors * dimension * 4
        
        # Metadata memory (rough estimate)
        meta_memory = len(self.metadata_store) * 200  # ~200 bytes per metadata dict
        chunk_memory = sum(len(c) for c in self.chunk_store)
        
        total_bytes = vector_memory + meta_memory + chunk_memory
        return total_bytes / (1024 * 1024)
    
    def get_memory_usage(self) -> Dict:
        """
        Get detailed memory usage information.
        
        v1.2: Added for memory monitoring.
        
        Returns:
            Dictionary with memory usage breakdown
        """
        n_vectors = self.index.ntotal
        dimension = self.dimension
        
        # Calculate vector memory
        if self.use_compression:
            vector_bytes = n_vectors * dimension * (self.compression_bits / 8) / 8
        else:
            vector_bytes = n_vectors * dimension * 4
        
        # Calculate metadata memory
        meta_bytes = len(self.metadata_store) * 200
        
        # Calculate chunk memory
        chunk_bytes = sum(len(c.encode('utf-8')) for c in self.chunk_store)
        
        total_bytes = vector_bytes + meta_bytes + chunk_bytes
        
        return {
            'total_mb': round(total_bytes / (1024 * 1024), 2),
            'vectors_mb': round(vector_bytes / (1024 * 1024), 2),
            'metadata_mb': round(meta_bytes / (1024 * 1024), 2),
            'chunks_mb': round(chunk_bytes / (1024 * 1024), 2),
            'vector_count': n_vectors,
            'compression_enabled': self.use_compression,
            'mmap_mode': self._mmap_mode
        }
