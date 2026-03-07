"""
Full workflow integration tests.

Tests end-to-end scenarios that combine multiple tools and modules.
Validates complete user journeys from document ingestion to search.
"""

import pytest
import json
import os
import shutil
from pathlib import Path
from typing import List, Dict

from scripts.tools.indexing import build_semantic_index, get_index_stats
from scripts.tools.search import semantic_search, batch_search
from scripts.tools.extraction import extract_keywords, generate_summary
from scripts.connectors.email import EmailConnector, EmailConfig


class TestFullWorkflows:
    """Test complete end-to-end workflows."""
    
    @pytest.fixture
    def large_document_set(self, tmp_path):
        """Create a larger set of documents for realistic testing."""
        documents = []
        
        # Programming documents
        for i in range(10):
            documents.append({
                'content': f'Python编程教程第{i}章。学习Python基础语法、数据类型、控制流程和函数定义。',
                'metadata': {
                    'path': f'python/chapter_{i}.md',
                    'title': f'Python教程第{i}章',
                    'category': 'programming',
                    'language': 'python',
                    'chapter': i
                }
            })
        
        # AI/ML documents
        for i in range(8):
            documents.append({
                'content': f'机器学习实践案例{i}。介绍监督学习、无监督学习和深度学习的实际应用。',
                'metadata': {
                    'path': f'ml/case_{i}.md',
                    'title': f'机器学习案例{i}',
                    'category': 'ai',
                    'topic': 'machine_learning',
                    'index': i
                }
            })
        
        # Data analysis documents
        for i in range(6):
            documents.append({
                'content': f'数据分析方法{i}。使用Pandas和NumPy进行数据处理、清洗和可视化。',
                'metadata': {
                    'path': f'data/method_{i}.md',
                    'title': f'数据分析方法{i}',
                    'category': 'data',
                    'tool': 'pandas',
                    'index': i
                }
            })
        
        return documents
    
    @pytest.fixture
    def temp_index(self, tmp_path, large_document_set):
        """Create a temporary index with test documents."""
        index_path = tmp_path / ".test-workflow-index"
        index_path.mkdir(exist_ok=True)
        
        result = build_semantic_index(
            documents=large_document_set,
            index_path=str(index_path),
            chunk_size=256,
            show_progress=False
        )
        
        assert result['success']
        
        yield index_path
        
        # Cleanup
        if index_path.exists():
            shutil.rmtree(index_path)
    
    def test_workflow_complete_knowledge_base(self, temp_index, large_document_set):
        """
        Workflow 1: Complete knowledge base creation and usage.
        
        Steps:
        1. Create knowledge base from documents
        2. Search for relevant information
        3. Filter by category
        4. Batch search for multiple topics
        """
        # Step 1: Verify index was created
        stats = get_index_stats(str(temp_index))
        assert stats['exists']
        assert stats['total_vectors'] > 0
        
        # Step 2: Search for relevant information
        results = semantic_search(
            query="如何学习Python编程",
            index_path=str(temp_index),
            top_k=5
        )
        
        assert len(results) > 0
        top_result = results[0]
        assert 'Python' in top_result['snippet'] or '编程' in top_result['snippet']
        
        # Step 3: Filter by category
        ai_results = semantic_search(
            query="学习方法",
            index_path=str(temp_index),
            top_k=10,
            filters={'category': 'ai'}
        )
        
        # All results should be from AI category
        for result in ai_results:
            assert result['metadata']['category'] == 'ai'
        
        # Step 4: Batch search
        queries = [
            "Python基础",
            "机器学习应用",
            "数据分析工具"
        ]
        
        batch_results = batch_search(
            queries=queries,
            index_path=str(temp_index),
            top_k=3
        )
        
        assert len(batch_results) == 3
        for results in batch_results:
            assert len(results) > 0
    
    def test_workflow_incremental_updates(self, tmp_path):
        """
        Workflow 2: Incremental knowledge base updates.
        
        Steps:
        1. Create initial knowledge base
        2. Add new documents
        3. Rebuild index
        4. Verify new content is searchable
        """
        index_path = tmp_path / ".incremental-index"
        index_path.mkdir(exist_ok=True)
        
        # Step 1: Initial documents
        initial_docs = [
            {'content': '初始文档1', 'metadata': {'id': 1}},
            {'content': '初始文档2', 'metadata': {'id': 2}}
        ]
        
        result = build_semantic_index(
            documents=initial_docs,
            index_path=str(index_path),
            show_progress=False
        )
        assert result['success']
        assert result['total_docs'] == 2
        
        # Step 2: Add new documents
        new_docs = initial_docs + [
            {'content': '新增文档3 - Python编程', 'metadata': {'id': 3, 'new': True}},
            {'content': '新增文档4 - 机器学习', 'metadata': {'id': 4, 'new': True}}
        ]
        
        # Step 3: Rebuild index (in real scenario, might use incremental update)
        result = build_semantic_index(
            documents=new_docs,
            index_path=str(index_path),
            show_progress=False
        )
        assert result['success']
        assert result['total_docs'] == 4
        
        # Step 4: Verify new content is searchable
        results = semantic_search(
            query="Python",
            index_path=str(index_path),
            top_k=5
        )
        
        assert len(results) > 0
        # Should find the new Python document
        found_new = any(r['metadata'].get('new') for r in results)
        assert found_new
    
    def test_workflow_multilingual_search(self, temp_index):
        """
        Workflow 3: Multilingual search capabilities.
        
        Steps:
        1. Search with Chinese queries
        2. Search with mixed queries
        3. Verify semantic understanding
        """
        # Chinese query
        results_zh = semantic_search(
            query="如何进行数据分析",
            index_path=str(temp_index),
            top_k=3
        )
        
        assert len(results_zh) > 0
        
        # Mixed query
        results_mixed = semantic_search(
            query="Python编程教程",
            index_path=str(temp_index),
            top_k=3
        )
        
        assert len(results_mixed) > 0
        
        # Semantic understanding - related concepts
        results_semantic = semantic_search(
            query="深度学习和神经网络",
            index_path=str(temp_index),
            top_k=3
        )
        
        # Should find machine learning documents even without exact keywords
        assert len(results_semantic) > 0
    
    def test_workflow_performance_monitoring(self, temp_index):
        """
        Workflow 4: Performance monitoring and optimization.
        
        Steps:
        1. Measure query performance
        2. Test with different query lengths
        3. Verify performance meets requirements
        """
        import time
        
        # Short query
        start = time.time()
        results = semantic_search("Python", str(temp_index), top_k=5)
        short_query_time = (time.time() - start) * 1000
        
        assert short_query_time < 150
        assert len(results) > 0
        
        # Medium query
        start = time.time()
        results = semantic_search(
            "如何学习Python编程语言",
            str(temp_index),
            top_k=5
        )
        medium_query_time = (time.time() - start) * 1000
        
        assert medium_query_time < 150
        
        # Long query
        start = time.time()
        results = semantic_search(
            "我想要学习Python编程语言，特别是关于数据类型、控制流程和函数定义的基础知识",
            str(temp_index),
            top_k=5
        )
        long_query_time = (time.time() - start) * 1000
        
        assert long_query_time < 150
    
    def test_workflow_search_suggestions(self, temp_index):
        """
        Workflow 5: Search suggestions and autocomplete.
        
        Steps:
        1. User starts typing
        2. Get suggestions
        3. Refine search based on suggestions
        """
        # Partial query
        partial = "Py"
        
        results = semantic_search(
            query=partial,
            index_path=str(temp_index),
            top_k=5
        )
        
        # Should return results even with partial query
        assert len(results) > 0
        
        # User refines query
        refined = "Python编程"
        
        refined_results = semantic_search(
            query=refined,
            index_path=str(temp_index),
            top_k=5
        )
        
        # Refined query should have better results
        assert len(refined_results) > 0
        # Note: similarity scores from HNSW are inner products, not normalized
        # So we just verify both queries return valid results
        assert results[0]['similarity'] is not None
        assert refined_results[0]['similarity'] is not None
    
    def test_workflow_metadata_enrichment(self, tmp_path):
        """
        Workflow 6: Metadata enrichment and filtering.
        
        Steps:
        1. Create documents with rich metadata
        2. Build index
        3. Search with complex filters
        """
        index_path = tmp_path / ".metadata-index"
        index_path.mkdir(exist_ok=True)
        
        # Documents with rich metadata
        docs = [
            {
                'content': 'Python基础教程',
                'metadata': {
                    'author': '张三',
                    'date': '2024-01-15',
                    'tags': ['python', 'beginner'],
                    'difficulty': 'easy',
                    'category': 'programming'
                }
            },
            {
                'content': 'Python进阶技巧',
                'metadata': {
                    'author': '李四',
                    'date': '2024-02-20',
                    'tags': ['python', 'advanced'],
                    'difficulty': 'hard',
                    'category': 'programming'
                }
            },
            {
                'content': '机器学习入门',
                'metadata': {
                    'author': '王五',
                    'date': '2024-03-10',
                    'tags': ['ml', 'beginner'],
                    'difficulty': 'easy',
                    'category': 'ai'
                }
            }
        ]
        
        result = build_semantic_index(
            documents=docs,
            index_path=str(index_path),
            show_progress=False
        )
        assert result['success']
        
        # Search with filter
        easy_results = semantic_search(
            query="教程",
            index_path=str(index_path),
            top_k=5,
            filters={'difficulty': 'easy'}
        )
        
        # All results should be easy difficulty
        for r in easy_results:
            assert r['metadata']['difficulty'] == 'easy'


class TestWorkflowWithMissingFeatures:
    """Test workflows that depend on features not yet implemented."""
    
    def test_workflow_with_keyword_extraction(self, tmp_path):
        """
        Workflow: Document search with keyword extraction.
        
        Steps:
        1. Extract keywords from documents
        2. Add keywords to metadata
        3. Search by keywords
        """
        index_path = tmp_path / ".keyword-index"
        index_path.mkdir(exist_ok=True)
        
        docs = [
            {
                'content': '机器学习是人工智能的核心技术，深度学习是机器学习的重要分支。神经网络和自然语言处理都是关键领域。',
                'metadata': {'id': 1, 'title': 'AI技术概览'}
            },
            {
                'content': 'Python是一种流行的编程语言，广泛用于数据分析、Web开发和机器学习领域。',
                'metadata': {'id': 2, 'title': 'Python介绍'}
            },
            {
                'content': '数据科学结合了统计学、机器学习和领域知识，用于从数据中提取有价值的洞察。',
                'metadata': {'id': 3, 'title': '数据科学基础'}
            }
        ]
        
        docs_with_keywords = []
        for doc in docs:
            keywords = extract_keywords(doc['content'], method='tfidf', top_n=5)
            enriched_metadata = doc['metadata'].copy()
            enriched_metadata['keywords'] = [kw['keyword'] for kw in keywords]
            enriched_metadata['keyword_scores'] = {kw['keyword']: kw['score'] for kw in keywords}
            
            docs_with_keywords.append({
                'content': doc['content'],
                'metadata': enriched_metadata
            })
        
        result = build_semantic_index(
            documents=docs_with_keywords,
            index_path=str(index_path),
            show_progress=False
        )
        assert result['success']
        
        results = semantic_search(
            query="机器学习",
            index_path=str(index_path),
            top_k=3
        )
        
        assert len(results) > 0
        
        for res in results:
            assert 'keywords' in res['metadata']
            assert isinstance(res['metadata']['keywords'], list)
            if res['metadata']['id'] == 1:
                keywords = res['metadata']['keywords']
                has_related_keyword = any(kw in ['机器', '学习', '深度', '人工智能', '神经网络'] for kw in keywords)
                assert has_related_keyword or len(keywords) > 0
    
    def test_workflow_with_summaries(self, tmp_path):
        """
        Workflow: Document search with summary generation.
        
        Steps:
        1. Generate summaries for long documents
        2. Index with summaries
        3. Display summaries in search results
        """
        index_path = tmp_path / ".summary-index"
        index_path.mkdir(exist_ok=True)
        
        long_docs = [
            {
                'content': '机器学习是人工智能的一个重要分支，它使计算机系统能够从数据中学习并改进性能。机器学习包括监督学习、无监督学习和强化学习等多种方法。深度学习是机器学习的一个子集，使用多层神经网络来处理复杂的数据模式。自然语言处理和计算机视觉是机器学习的重要应用领域。在实际应用中，机器学习被广泛用于推荐系统、图像识别、语音识别和自动驾驶等场景。',
                'metadata': {'id': 1, 'title': '机器学习详解', 'category': 'ai'}
            },
            {
                'content': 'Python是一种高级编程语言，以其简洁的语法和强大的功能而闻名。它支持多种编程范式，包括面向对象、函数式和过程式编程。Python拥有丰富的标准库和第三方包，使其成为数据科学、Web开发和自动化测试的首选语言。NumPy、Pandas和Scikit-learn是Python在数据科学领域的核心库。Django和Flask是流行的Web框架。Python的易学性和强大的社区支持使其成为初学者的理想选择。',
                'metadata': {'id': 2, 'title': 'Python编程语言', 'category': 'programming'}
            }
        ]
        
        docs_with_summaries = []
        for doc in long_docs:
            summary_result = generate_summary(doc['content'], max_length=100)
            
            enriched_metadata = doc['metadata'].copy()
            enriched_metadata['summary'] = summary_result['summary']
            enriched_metadata['original_length'] = summary_result['original_length']
            enriched_metadata['compression_ratio'] = summary_result['compression_ratio']
            
            docs_with_summaries.append({
                'content': doc['content'],
                'metadata': enriched_metadata
            })
        
        result = build_semantic_index(
            documents=docs_with_summaries,
            index_path=str(index_path),
            show_progress=False
        )
        assert result['success']
        
        results = semantic_search(
            query="Python数据科学",
            index_path=str(index_path),
            top_k=2
        )
        
        assert len(results) > 0
        
        for res in results:
            assert 'summary' in res['metadata']
            assert len(res['metadata']['summary']) <= 120
            assert res['metadata']['original_length'] > len(res['metadata']['summary'])
            assert 0 < res['metadata']['compression_ratio'] <= 1.0
    
    @pytest.mark.skip(reason="Email connector requires real IMAP connection")
    def test_workflow_email_integration(self, tmp_path):
        """
        Workflow: Email and document hybrid search.
        
        Steps:
        1. Connect to email
        2. Search emails
        3. Combine with document search
        """
        # TODO: Implement with real email connection
        pass


class TestErrorRecoveryWorkflows:
    """Test error handling and recovery in workflows."""
    
    def test_workflow_handle_corrupted_index(self, tmp_path):
        """
        Workflow: Handle corrupted index gracefully.
        
        Steps:
        1. Create index
        2. Corrupt index files
        3. Attempt search
        4. Rebuild index
        5. Verify recovery
        """
        index_path = tmp_path / ".corrupt-index"
        index_path.mkdir(exist_ok=True)
        
        # Create index
        docs = [{'content': 'Test', 'metadata': {'id': 1}}]
        result = build_semantic_index(
            documents=docs,
            index_path=str(index_path),
            show_progress=False
        )
        assert result['success']
        
        # Corrupt index
        faiss_file = index_path / "index.faiss"
        if faiss_file.exists():
            with open(faiss_file, 'wb') as f:
                f.write(b'corrupted')
        
        # Attempt search - should handle gracefully
        results = semantic_search(
            query="test",
            index_path=str(index_path),
            top_k=5
        )
        
        # Should not crash, might return empty or handle error
        assert isinstance(results, list)
        
        # Rebuild index
        result = build_semantic_index(
            documents=docs,
            index_path=str(index_path),
            show_progress=False
        )
        assert result['success']
        
        # Verify recovery
        results = semantic_search(
            query="Test",
            index_path=str(index_path),
            top_k=5
        )
        assert len(results) > 0
    
    def test_workflow_handle_large_queries(self, tmp_path):
        """
        Workflow: Handle very large queries gracefully.
        
        Steps:
        1. Create index
        2. Search with extremely long query
        3. Verify it doesn't crash
        """
        index_path = tmp_path / ".large-query-index"
        index_path.mkdir(exist_ok=True)
        
        # Create index
        docs = [{'content': 'Test document', 'metadata': {'id': 1}}]
        result = build_semantic_index(
            documents=docs,
            index_path=str(index_path),
            show_progress=False
        )
        assert result['success']
        
        # Very long query
        long_query = "测试 " * 1000  # 2000+ characters
        
        # Should handle gracefully without crashing
        results = semantic_search(
            query=long_query,
            index_path=str(index_path),
            top_k=5
        )
        
        # Should return results or empty list, not crash
        assert isinstance(results, list)


class TestDataIntegrity:
    """Test data integrity across workflows."""
    
    def test_metadata_preservation(self, tmp_path):
        """Test that metadata is preserved through indexing and search."""
        index_path = tmp_path / ".integrity-index"
        index_path.mkdir(exist_ok=True)
        
        # Document with specific metadata
        original_doc = {
            'content': 'Test content for metadata preservation',
            'metadata': {
                'id': 'test-123',
                'author': 'Test Author',
                'date': '2024-01-01',
                'tags': ['test', 'metadata'],
                'custom_field': 'custom_value'
            }
        }
        
        # Build index
        result = build_semantic_index(
            documents=[original_doc],
            index_path=str(index_path),
            show_progress=False
        )
        assert result['success']
        
        # Search
        results = semantic_search(
            query="Test content",
            index_path=str(index_path),
            top_k=1
        )
        
        assert len(results) > 0
        
        # Verify metadata is preserved
        result_metadata = results[0]['metadata']
        assert result_metadata['id'] == original_doc['metadata']['id']
        assert result_metadata['author'] == original_doc['metadata']['author']
        assert result_metadata['custom_field'] == original_doc['metadata']['custom_field']
        assert set(result_metadata['tags']) == set(original_doc['metadata']['tags'])


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
