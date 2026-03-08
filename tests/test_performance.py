#!/usr/bin/env python3
"""
Performance benchmark for v1.2.

Tests indexing and search performance at scale.
v1.2 targets: 10k docs < 5min, search < 100ms, memory < 500MB
"""

import json
import time
import sys
import os
import random
import shutil
import tempfile
import tracemalloc

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.tools.indexing import build_semantic_index, ProgressInfo
from scripts.tools.search import semantic_search, semantic_search_paginated, clear_search_cache
from scripts.index.vector_store import VectorStore


# Sample text templates for generating documents
TEXT_TEMPLATES = [
    "Python是一种高级编程语言，以其简洁清晰的语法而闻名。Python广泛应用于Web开发、数据科学、人工智能、自动化脚本等多个领域。",
    "机器学习是人工智能的核心技术之一。通过训练模型，机器可以从数据中学习规律，实现预测和分类等任务。",
    "异步编程是现代软件开发的重要技术。Python的asyncio库提供了强大的异步编程支持，允许开发者编写高效的并发代码。",
    "数据分析是从数据中提取有价值信息的过程。Python提供了丰富的数据分析工具，如Pandas用于数据处理，NumPy用于数值计算。",
    "深度学习是机器学习的一个分支，使用多层神经网络来学习数据的表示。卷积神经网络广泛应用于图像识别。",
    "自然语言处理是人工智能的重要分支，致力于让计算机理解和处理人类语言。常见的NLP任务包括文本分类、情感分析、机器翻译。",
    "Web开发是Python的重要应用领域之一。Django和Flask是两个流行的Python Web框架。Django是一个全功能的框架。",
    "数据库是现代应用的核心组件。SQL和NoSQL数据库各有优势，选择合适的数据库对于应用性能至关重要。",
    "容器化技术如Docker改变了软件开发和部署的方式。容器提供了轻量级的虚拟化解决方案，使应用更易于部署和扩展。",
    "云计算平台如AWS、Azure和GCP提供了丰富的服务，包括计算、存储、数据库、机器学习等，帮助企业快速构建和扩展应用。"
]

CATEGORIES = ['programming', 'ai', 'data', 'web', 'devops']
TAGS = ['python', 'ai', 'ml', 'web', 'data', 'cloud', 'docker', 'database']


def generate_documents(count: int, avg_length: int = 500) -> list:
    """Generate test documents with varied content."""
    documents = []
    
    for i in range(count):
        # Generate content by combining random templates
        num_templates = random.randint(2, 5)
        selected_templates = random.sample(TEXT_TEMPLATES, num_templates)
        content = ' '.join(selected_templates)
        
        # Extend to approximate length
        while len(content) < avg_length:
            content += ' ' + random.choice(TEXT_TEMPLATES)
        
        # Add some variation
        content += f" 文档编号{i}包含关于技术的详细信息。"
        
        # Create metadata
        doc = {
            'path': f'doc_{i}.md',
            'content': content[:avg_length],  # Cap at avg length
            'metadata': {
                'title': f'技术文档{i}',
                'category': random.choice(CATEGORIES),
                'tags': random.sample(TAGS, random.randint(2, 4)),
                'date': f'2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}',
                'index': i
            }
        }
        documents.append(doc)
    
    return documents


def get_memory_usage_mb():
    """Get current process memory usage in MB."""
    import psutil
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024


def run_benchmark_v12():
    """Run v1.2 performance benchmark for large-scale datasets."""
    print("=" * 70)
    print("v1.2 Performance Benchmark")
    print("Targets: 10k docs < 5min, search < 100ms, memory < 500MB")
    print("=" * 70)
    
    results = []
    temp_dir = tempfile.mkdtemp(prefix="ka_benchmark_")
    
    try:
        # Test with progressively larger datasets
        test_configs = [
            (100, 1.0, "smoke test"),
            (1000, 30.0, "medium dataset"),
            (5000, 150.0, "large dataset"),
            (10000, 300.0, "v1.2 target"),  # 5 minutes = 300 seconds
        ]
        
        for count, target_time, description in test_configs:
            print(f"\n{'='*70}")
            print(f"Testing {description}: {count} documents")
            print(f"{'='*70}")
            
            index_path = os.path.join(temp_dir, f"index_{count}")
            
            # Clear search cache before each test
            clear_search_cache()
            
            # Generate documents
            print(f"\n[1/5] Generating {count} documents...")
            gen_start = time.time()
            documents = generate_documents(count)
            gen_time = time.time() - gen_start
            print(f"      Generated in {gen_time:.2f}s")
            
            # Track memory
            mem_before = get_memory_usage_mb()
            
            # Build index with batch processing
            print(f"\n[2/5] Building semantic index...")
            
            # Progress callback for large datasets
            def progress_callback(info: ProgressInfo):
                if info.current_batch % 10 == 0 or info.current_batch == info.total_batches:
                    print(f"      Batch {info.current_batch}/{info.total_batches}: "
                          f"{info.documents_processed}/{info.total_documents} docs, "
                          f"{info.chunks_created} chunks, "
                          f"elapsed: {info.elapsed_time:.1f}s, "
                          f"ETA: {info.estimated_remaining:.1f}s")
            
            build_start = time.time()
            result = build_semantic_index(
                documents=documents,
                index_path=index_path,
                chunk_size=256,
                batch_size=8,
                doc_batch_size=100,  # v1.2 batch size
                show_progress=count >= 1000,
                progress_callback=progress_callback if count >= 1000 else None
            )
            build_time = time.time() - build_start
            
            mem_after_build = get_memory_usage_mb()
            mem_delta = mem_after_build - mem_before
            
            print(f"\n      Total build time: {build_time:.2f}s")
            print(f"      Documents: {result['total_docs']}")
            print(f"      Chunks: {result['total_chunks']}")
            print(f"      Index size: {result['index_size']}")
            print(f"      Memory delta: {mem_delta:.1f} MB")
            
            # Test search performance (v1.2 target: < 100ms)
            print(f"\n[3/5] Testing search performance (v1.2 target: < 100ms)...")
            queries = [
                "Python编程",
                "机器学习算法",
                "Web开发框架",
                "数据分析工具",
                "云计算平台"
            ]
            
            search_times = []
            for query in queries:
                start = time.time()
                results = semantic_search(
                    query=query,
                    index_path=index_path,
                    top_k=5
                )
                elapsed = (time.time() - start) * 1000  # ms
                search_times.append(elapsed)
                print(f"      Query '{query[:10]}...': {elapsed:.1f}ms ({len(results)} results)")
            
            avg_search_time = sum(search_times) / len(search_times)
            max_search_time = max(search_times)
            
            # Test paginated search (v1.2 feature)
            print(f"\n[4/5] Testing paginated search...")
            paginated = semantic_search_paginated(
                query="Python",
                index_path=index_path,
                page=1,
                page_size=10
            )
            print(f"      Page 1 results: {len(paginated.results)}")
            print(f"      Total available: {paginated.total_available}")
            print(f"      Query time: {paginated.query_time_ms:.1f}ms")
            
            # Test memory-mapped loading (v1.2 feature)
            print(f"\n[5/5] Testing memory-mapped loading...")
            store = VectorStore()
            store.load(index_path, use_mmap=True)
            mem_usage = store.get_memory_usage()
            print(f"      Vectors: {store.get_vector_count()}")
            print(f"      Memory usage: {mem_usage['total_mb']} MB")
            print(f"      MMap mode: {mem_usage['mmap_mode']}")
            
            # Performance checks
            print(f"\n{'='*70}")
            print(f"Performance Check for {count} docs:")
            print(f"{'='*70}")
            
            # Build time check
            build_ok = build_time < target_time
            print(f"  Build time: {build_time:.1f}s {'✅' if build_ok else '❌'} (target: <{target_time}s)")
            
            # Search latency check (v1.2: < 100ms)
            search_ok = avg_search_time < 100
            print(f"  Search latency: {avg_search_time:.1f}ms {'✅' if search_ok else '❌'} (target: <100ms)")
            
            # Memory check (v1.2: < 500MB)
            memory_ok = mem_delta < 500
            print(f"  Memory delta: {mem_delta:.1f}MB {'✅' if memory_ok else '❌'} (target: <500MB)")
            
            # Record results
            benchmark_result = {
                'doc_count': count,
                'description': description,
                'build_time': round(build_time, 2),
                'build_target': target_time,
                'build_ok': build_ok,
                'avg_search_time': round(avg_search_time, 1),
                'max_search_time': round(max_search_time, 1),
                'search_ok': search_ok,
                'memory_delta_mb': round(mem_delta, 1),
                'memory_ok': memory_ok,
                'total_chunks': result['total_chunks'],
                'all_ok': build_ok and search_ok and memory_ok
            }
            results.append(benchmark_result)
    
    finally:
        # Cleanup
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print(f"\nCleaned up temp directory: {temp_dir}")
    
    # Summary
    print(f"\n{'='*70}")
    print("v1.2 BENCHMARK SUMMARY")
    print(f"{'='*70}")
    print(f"\n{'Docs':<8} {'Build':<12} {'Target':<10} {'Search':<12} {'Memory':<12} {'Status'}")
    print("-" * 70)
    
    all_ok = True
    for r in results:
        status = '✅ PASS' if r['all_ok'] else '❌ FAIL'
        if not r['all_ok']:
            all_ok = False
        print(f"{r['doc_count']:<8} {r['build_time']:<12.1f}s {r['build_target']:<10.0f}s "
              f"{r['avg_search_time']:<12.1f}ms {r['memory_delta_mb']:<12.1f}MB {status}")
    
    print("\n" + "="*70)
    if all_ok:
        print("✅ ALL v1.2 PERFORMANCE TARGETS MET!")
        print("="*70)
        print("\n验收结果:")
        print("  ✅ 索引构建性能达标 (10k docs < 5min)")
        print("  ✅ 搜索查询性能达标 (< 100ms)")
        print("  ✅ 内存使用达标 (< 500MB)")
        return 0
    else:
        print("❌ SOME v1.2 PERFORMANCE TARGETS NOT MET")
        print("="*70)
        return 1


def run_memory_benchmark():
    """Run detailed memory usage benchmark."""
    print("=" * 70)
    print("Memory Usage Benchmark")
    print("=" * 70)
    
    tracemalloc.start()
    
    # Test with and without compression
    configs = [
        {"name": "Standard HNSW", "compression": False},
        {"name": "HNSW + PQ Compression", "compression": True},
    ]
    
    test_size = 1000
    documents = generate_documents(test_size)
    
    for config in configs:
        print(f"\n{config['name']}:")
        
        # Create vector store
        store = VectorStore(
            dimension=512,
            use_compression=config['compression']
        )
        
        # Add vectors (simulated)
        import numpy as np
        vectors = np.random.rand(test_size, 512).astype(np.float32)
        store.add_vectors(vectors)
        
        # Get memory usage
        mem_usage = store.get_memory_usage()
        print(f"  Total memory: {mem_usage['total_mb']} MB")
        print(f"  Vectors memory: {mem_usage['vectors_mb']} MB")
        print(f"  Vector count: {mem_usage['vector_count']}")
        print(f"  Compression: {mem_usage['compression_enabled']}")
    
    tracemalloc.stop()


def main():
    """Run the benchmark."""
    import argparse
    
    parser = argparse.ArgumentParser(description='v1.2 Performance Benchmark')
    parser.add_argument('--memory', action='store_true', help='Run memory benchmark only')
    args = parser.parse_args()
    
    if args.memory:
        return run_memory_benchmark()
    else:
        return run_benchmark_v12()


if __name__ == '__main__':
    sys.exit(main())
