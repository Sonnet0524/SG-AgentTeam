"""
Semantic indexing tool for building vector indexes.

Implements TASK-AI1: build_semantic_index function.
v1.2: Added batch processing and progress reporting for large-scale datasets.
"""

import os
import time
import logging
import gc
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass, field

# Add parent directory to path for imports
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from embeddings.encoder import EmbeddingEncoder
from index.manager import IndexManager

logger = logging.getLogger(__name__)


@dataclass
class ProgressInfo:
    """Progress information for batch indexing."""
    current_batch: int = 0
    total_batches: int = 0
    documents_processed: int = 0
    total_documents: int = 0
    chunks_created: int = 0
    elapsed_time: float = 0.0
    estimated_remaining: float = 0.0


def build_semantic_index(
    documents: List[Dict],
    index_path: str = ".ka-index",
    chunk_size: int = 256,
    chunk_overlap: int = 50,
    batch_size: int = 8,
    model_name: str = "BAAI/bge-small-zh-v1.5",
    show_progress: bool = False,
    # v1.2 new parameters for batch processing
    doc_batch_size: int = 100,
    enable_gc: bool = True,
    progress_callback: Optional[Callable[[ProgressInfo], None]] = None
) -> Dict:
    """
    Build a semantic index from documents.
    
    This function processes a list of documents, chunks them into smaller pieces,
    generates embeddings, and builds a FAISS HNSW index for fast semantic search.
    
    v1.2 Optimization: Supports batch processing for large datasets (>10k docs).
    
    Args:
        documents: List of document dictionaries. Each document should have:
            - 'content': str - The text content of the document
            - 'metadata': dict - Metadata about the document (optional)
            Example: [{'content': '...', 'metadata': {'path': 'doc1.md'}}]
        
        index_path: Directory path to save the index files (default: ".ka-index")
            Creates two files:
            - index.faiss: FAISS vector index
            - metadata.json: Chunk metadata and text
        
        chunk_size: Maximum characters per text chunk (default: 256)
            Smaller chunks = more granular search but more vectors
        
        chunk_overlap: Character overlap between consecutive chunks (default: 50)
            Helps maintain context across chunk boundaries
        
        batch_size: Number of texts to encode in parallel (default: 8)
            Smaller batch sizes use less memory
        
        model_name: Name of the embedding model (default: "BAAI/bge-small-zh-v1.5")
            Must be a valid SentenceTransformers model name
        
        show_progress: Whether to show progress bar for encoding (default: False)
        
        doc_batch_size: Number of documents to process per batch (default: 100)
            For large datasets, processes documents in batches to manage memory.
            Recommended: 100-500 for typical systems, lower for limited memory.
        
        enable_gc: Enable garbage collection between batches (default: True)
            Helps manage memory for large datasets.
        
        progress_callback: Optional callback for progress updates (default: None)
            Called with ProgressInfo object after each batch.
    
    Returns:
        Dictionary with build statistics:
        {
            'success': bool,
            'total_docs': int,
            'total_chunks': int,
            'index_size': str,
            'build_time': str,
            'model': str,
            'dimension': int,
            'index_path': str,
            'batches_processed': int  # v1.2: batch count
        }
    
    Raises:
        ValueError: If documents list is empty or invalid
        RuntimeError: If model loading fails
    
    Example:
        >>> documents = [
        ...     {'content': 'Python是一种编程语言', 'metadata': {'id': 1}},
        ...     {'content': '机器学习是AI的核心技术', 'metadata': {'id': 2}}
        ... ]
        >>> result = build_semantic_index(documents)
        >>> print(result['success'])
        True
        >>> print(result['total_chunks'])
        2
    
    Performance (v1.2 optimized):
        - 100 docs: ~1s
        - 1000 docs: ~10s
        - 10000 docs: <5min (target)
    
    Notes:
        - First run will download the model (~130MB)
        - Model is cached for subsequent runs
        - Batch processing reduces peak memory usage
        - Uses HNSW index for fast approximate search
    """
    start_time = time.time()
    
    # Validate inputs
    if not documents:
        return {
            'success': False,
            'error': 'Documents list is empty',
            'total_docs': 0,
            'total_chunks': 0,
            'build_time': '0s',
            'model': model_name
        }
    
    # Validate document structure
    for i, doc in enumerate(documents):
        if 'content' not in doc:
            logger.warning(f"Document {i} missing 'content' field")
        if 'metadata' not in doc:
            doc['metadata'] = {}
    
    total_docs = len(documents)
    
    # Determine if we need batch processing
    use_batch_mode = total_docs > doc_batch_size
    
    if use_batch_mode:
        logger.info(f"Using batch mode for {total_docs} documents (batch_size={doc_batch_size})")
    else:
        logger.info(f"Building semantic index for {total_docs} documents")
    
    try:
        # 1. Initialize encoder
        encoder = EmbeddingEncoder(
            model_name=model_name,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            batch_size=batch_size
        )
        
        # 2. Initialize index manager
        manager = IndexManager(index_path=index_path)
        manager.initialize_empty_index(dimension=encoder.get_dimension())
        
        # 3. Process documents (batch or single)
        all_chunks = []
        all_metadata = []
        total_batches = (total_docs + doc_batch_size - 1) // doc_batch_size if use_batch_mode else 1
        
        if use_batch_mode:
            # Batch processing for large datasets
            for batch_idx in range(0, total_docs, doc_batch_size):
                batch_start = time.time()
                batch_docs = documents[batch_idx:batch_idx + doc_batch_size]
                batch_num = batch_idx // doc_batch_size + 1
                
                # Encode batch
                embeddings, chunk_metadata = encoder.encode_documents(
                    batch_docs,
                    show_progress=show_progress
                )
                
                # Get chunk texts
                batch_chunks = []
                for doc in batch_docs:
                    chunks = encoder.chunk_text(doc.get('content', ''))
                    batch_chunks.extend(chunks)
                
                # Add to index
                manager.add_to_index(
                    vectors=embeddings,
                    metadata=chunk_metadata,
                    chunks=batch_chunks
                )
                
                all_chunks.extend(batch_chunks)
                all_metadata.extend(chunk_metadata)
                
                # Progress reporting
                elapsed = time.time() - start_time
                progress = ProgressInfo(
                    current_batch=batch_num,
                    total_batches=total_batches,
                    documents_processed=min(batch_idx + doc_batch_size, total_docs),
                    total_documents=total_docs,
                    chunks_created=len(all_chunks),
                    elapsed_time=elapsed,
                    estimated_remaining=elapsed * (total_batches - batch_num) / batch_num if batch_num > 0 else 0
                )
                
                if progress_callback:
                    progress_callback(progress)
                
                if show_progress:
                    logger.info(
                        f"Batch {batch_num}/{total_batches}: "
                        f"{len(batch_docs)} docs, {len(batch_chunks)} chunks, "
                        f"{time.time() - batch_start:.1f}s"
                    )
                
                # Memory management
                if enable_gc:
                    gc.collect()
        else:
            # Single batch for small datasets
            embeddings, chunk_metadata = encoder.encode_documents(
                documents,
                show_progress=show_progress
            )
            
            for doc in documents:
                chunks = encoder.chunk_text(doc.get('content', ''))
                all_chunks.extend(chunks)
            
            manager.add_to_index(
                vectors=embeddings,
                metadata=chunk_metadata,
                chunks=all_chunks
            )
            all_metadata = chunk_metadata
        
        # 4. Save index to disk
        if not manager.save_index():
            logger.error("Failed to save index")
            return {
                'success': False,
                'error': 'Failed to save index',
                'total_docs': total_docs,
                'total_chunks': len(all_chunks),
                'build_time': f"{time.time() - start_time:.1f}s",
                'model': model_name
            }
        
        # 5. Calculate index size
        index_file = os.path.join(index_path, 'index.faiss')
        index_size_mb = os.path.getsize(index_file) / 1024 / 1024 if os.path.exists(index_file) else 0
        
        build_time = time.time() - start_time
        
        result = {
            'success': True,
            'total_docs': total_docs,
            'total_chunks': len(all_chunks),
            'index_size': f"{index_size_mb:.2f} MB",
            'build_time': f"{build_time:.1f}s",
            'build_time_seconds': round(build_time, 2),
            'model': model_name,
            'dimension': encoder.get_dimension(),
            'index_path': index_path,
            'batches_processed': total_batches if use_batch_mode else 1,
            'batch_mode': use_batch_mode
        }
        
        logger.info(
            f"Index built successfully: {len(all_chunks)} chunks in {build_time:.1f}s "
            f"({'batch mode' if use_batch_mode else 'single batch'})"
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to build index: {e}")
        return {
            'success': False,
            'error': str(e),
            'total_docs': total_docs,
            'total_chunks': 0,
            'build_time': f"{time.time() - start_time:.1f}s",
            'model': model_name
        }


def get_index_stats(index_path: str = ".ka-index") -> Dict:
    """
    Get statistics about an existing index.
    
    Args:
        index_path: Path to the index directory
    
    Returns:
        Dictionary with index statistics
    
    Example:
        >>> stats = get_index_stats('.ka-index')
        >>> print(stats['total_vectors'])
        100
    """
    manager = IndexManager(index_path=index_path)
    
    if not manager.index_exists():
        return {
            'exists': False,
            'index_path': index_path
        }
    
    if manager.load_index():
        stats = manager.get_stats()
        stats['exists'] = True
        return stats
    
    return {
        'exists': False,
        'error': 'Failed to load index',
        'index_path': index_path
    }
