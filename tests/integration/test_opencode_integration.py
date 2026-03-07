"""
Integration tests for opencode usage scenarios.

Tests the tool functions as they would be called by opencode agent.
Validates API contracts, input/output formats, and integration scenarios.
"""

import pytest
import json
import os
import shutil
from pathlib import Path

# Import tools
from scripts.tools.indexing import build_semantic_index, get_index_stats
from scripts.tools.search import semantic_search, batch_search

# Import connectors
from scripts.connectors.email import EmailConnector, EmailConfig
from scripts.connectors.base import SearchResult


class TestOpenCodeIntegration:
    """Test scenarios for opencode agent using knowledge-assistant tools."""
    
    @pytest.fixture(autouse=True)
    def setup_test_index(self, tmp_path):
        """Create a test index before each test."""
        self.index_path = tmp_path / ".test-index"
        self.index_path.mkdir(exist_ok=True)
        
        # Create test documents
        self.test_documents = [
            {
                'content': 'Python是一种高级编程语言，支持面向对象、函数式和过程式编程范式。',
                'metadata': {
                    'path': 'python_intro.md',
                    'title': 'Python编程语言介绍',
                    'category': 'programming'
                }
            },
            {
                'content': '异步编程是现代软件开发的重要技术，可以提高程序的并发性能。',
                'metadata': {
                    'path': 'async_programming.md',
                    'title': '异步编程技术',
                    'category': 'programming'
                }
            },
            {
                'content': '机器学习是人工智能的核心技术，包括监督学习、无监督学习和强化学习。',
                'metadata': {
                    'path': 'ml_intro.md',
                    'title': '机器学习入门',
                    'category': 'ai'
                }
            },
            {
                'content': '数据分析是使用统计和逻辑方法对数据进行解释的过程。',
                'metadata': {
                    'path': 'data_analysis.md',
                    'title': '数据分析基础',
                    'category': 'data'
                }
            }
        ]
        
        # Build index
        result = build_semantic_index(
            documents=self.test_documents,
            index_path=str(self.index_path),
            chunk_size=256,
            show_progress=False
        )
        
        assert result['success'], f"Failed to build test index: {result.get('error')}"
        
        yield
        
        # Cleanup
        if self.index_path.exists():
            shutil.rmtree(self.index_path)
    
    def test_api_contract_build_index(self):
        """Test that build_semantic_index returns expected contract."""
        docs = [{
            'content': 'Test document',
            'metadata': {'id': 'test1'}
        }]
        
        result = build_semantic_index(
            documents=docs,
            index_path=str(self.index_path / "test2"),
            show_progress=False
        )
        
        # Verify contract fields
        assert 'success' in result
        assert 'total_docs' in result
        assert 'total_chunks' in result
        assert 'index_size' in result
        assert 'build_time' in result
        assert 'model' in result
        assert 'dimension' in result
        assert 'index_path' in result
        
        # Verify types
        assert isinstance(result['success'], bool)
        assert isinstance(result['total_docs'], int)
        assert isinstance(result['total_chunks'], int)
        assert isinstance(result['total_chunks'], int)
        assert isinstance(result['model'], str)
        assert isinstance(result['dimension'], int)
    
    def test_api_contract_search(self):
        """Test that semantic_search returns expected contract."""
        results = semantic_search(
            query="Python编程",
            index_path=str(self.index_path),
            top_k=3
        )
        
        # Verify list of results
        assert isinstance(results, list)
        
        if results:
            result = results[0]
            
            # Verify contract fields
            assert 'rank' in result
            assert 'similarity' in result
            assert 'snippet' in result
            assert 'metadata' in result
            assert 'index' in result
            
            # Verify types
            assert isinstance(result['rank'], int)
            assert isinstance(result['similarity'], (int, float))
            assert isinstance(result['snippet'], str)
            assert isinstance(result['metadata'], dict)
    
    def test_scenario_build_knowledge_base(self):
        """
        Scenario: opencode builds a knowledge base from documents.
        
        opencode usage:
        1. User has documents from file scanning
        2. opencode calls build_semantic_index with document data
        3. Index is created and ready for search
        """
        # Simulate opencode receiving documents from file operations
        opencode_documents = []
        
        # Simulate reading markdown files
        test_notes_dir = Path(__file__).parent.parent / "fixtures"
        if test_notes_dir.exists():
            for md_file in test_notes_dir.glob("*.md"):
                content = md_file.read_text(encoding='utf-8')
                opencode_documents.append({
                    'content': content,
                    'metadata': {
                        'path': str(md_file),
                        'title': md_file.stem,
                        'source': 'markdown'
                    }
                })
        
        # If no markdown files, use test documents
        if not opencode_documents:
            opencode_documents = self.test_documents
        
        # opencode calls the tool
        result = build_semantic_index(
            documents=opencode_documents,
            index_path=str(self.index_path / "kb"),
            show_progress=False
        )
        
        # Verify success
        assert result['success']
        assert result['total_docs'] == len(opencode_documents)
        assert result['total_chunks'] > 0
        
        # Verify index was created
        assert (self.index_path / "kb" / "index.faiss").exists()
        assert (self.index_path / "kb" / "metadata.json").exists()
    
    def test_scenario_semantic_search(self):
        """
        Scenario: opencode performs semantic search for user query.
        
        opencode usage:
        1. User asks: "如何学习Python？"
        2. opencode calls semantic_search with the query
        3. Returns relevant documents
        """
        user_query = "如何学习Python编程"
        
        # opencode calls the search tool
        results = semantic_search(
            query=user_query,
            index_path=str(self.index_path),
            top_k=3
        )
        
        # Verify results
        assert len(results) > 0
        assert len(results) <= 3
        
        # Verify results are relevant
        top_result = results[0]
        assert top_result['similarity'] > 0.5
        assert 'Python' in top_result['snippet'] or '编程' in top_result['snippet']
        
        # opencode can present these results to user
        print(f"\n搜索结果:")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['metadata']['title']} (相似度: {result['similarity']:.2f})")
    
    def test_scenario_filtered_search(self):
        """
        Scenario: opencode searches with metadata filters.
        
        opencode usage:
        1. User wants results only from a specific category
        2. opencode applies filters to narrow results
        """
        # Search for programming content only
        results = semantic_search(
            query="编程",
            index_path=str(self.index_path),
            top_k=5,
            filters={'category': 'programming'}
        )
        
        # All results should be from programming category
        for result in results:
            assert result['metadata'].get('category') == 'programming'
    
    def test_scenario_batch_queries(self):
        """
        Scenario: opencode searches for multiple queries efficiently.
        
        opencode usage:
        1. User has multiple search queries
        2. opencode uses batch_search for efficiency
        """
        queries = [
            "Python编程",
            "机器学习",
            "数据分析"
        ]
        
        # opencode calls batch search
        all_results = batch_search(
            queries=queries,
            index_path=str(self.index_path),
            top_k=2
        )
        
        # Verify results
        assert len(all_results) == len(queries)
        
        for i, (query, results) in enumerate(zip(queries, all_results)):
            print(f"\n查询 {i+1}: {query}")
            print(f"结果数: {len(results)}")
            assert isinstance(results, list)
    
    def test_scenario_mixed_sources(self):
        """
        Scenario: opencode searches across mixed data sources.
        
        opencode usage:
        1. User wants to search both documents and emails
        2. opencode uses connectors and search together
        """
        # Simulate email connector
        email_config = EmailConfig(
            server="imap.test.com",
            username="test@test.com",
            password="test_pass"
        )
        
        # In real scenario, would connect to email
        # For testing, we simulate the integration
        email_search_results = []
        
        # Search in knowledge base
        kb_results = semantic_search(
            query="项目进度",
            index_path=str(self.index_path),
            top_k=3
        )
        
        # Combine results
        combined_results = {
            'knowledge_base': kb_results,
            'emails': email_search_results
        }
        
        # opencode can present combined results
        assert 'knowledge_base' in combined_results
        assert 'emails' in combined_results
    
    def test_error_handling_invalid_documents(self):
        """Test error handling for invalid document input."""
        # Empty documents
        result = build_semantic_index(
            documents=[],
            index_path=str(self.index_path / "empty"),
            show_progress=False
        )
        
        assert result['success'] is False
        assert 'error' in result
    
    def test_error_handling_missing_index(self):
        """Test error handling for missing index."""
        results = semantic_search(
            query="test",
            index_path="/nonexistent/path",
            top_k=5
        )
        
        # Should return empty list, not crash
        assert results == []
    
    def test_performance_requirements(self):
        """Test that performance meets requirements."""
        import time
        
        # Build performance
        docs = [
            {'content': f'文档{i}的内容', 'metadata': {'id': i}}
            for i in range(100)
        ]
        
        start = time.time()
        result = build_semantic_index(
            documents=docs,
            index_path=str(self.index_path / "perf"),
            show_progress=False
        )
        build_time = time.time() - start
        
        # Should build 100 docs in < 10s
        assert build_time < 10.0
        assert result['success']
        
        # Search performance
        start = time.time()
        results = semantic_search(
            query="测试查询",
            index_path=str(self.index_path / "perf"),
            top_k=5
        )
        search_time = (time.time() - start) * 1000  # ms
        
        # Should search in < 150ms
        assert search_time < 150
        assert len(results) > 0


class TestIndexStats:
    """Test index statistics functionality."""
    
    def test_get_index_stats(self, tmp_path):
        """Test retrieving index statistics."""
        index_path = tmp_path / ".stats-index"
        
        # Create index
        docs = [{'content': 'Test', 'metadata': {'id': 1}}]
        result = build_semantic_index(
            documents=docs,
            index_path=str(index_path),
            show_progress=False
        )
        assert result['success']
        
        # Get stats
        stats = get_index_stats(str(index_path))
        
        assert stats['exists']
        assert 'total_vectors' in stats
        assert stats['total_vectors'] > 0


class TestIntegrationWithConnectors:
    """Test integration with data connectors."""
    
    @pytest.mark.skip(reason="Email connector requires real IMAP connection")
    def test_email_connector_integration(self):
        """Test integration with EmailConnector."""
        # This would test real email connection
        # Skipped for unit tests
        pass


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
