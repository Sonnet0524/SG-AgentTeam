"""
Tests for abstractive summarization functionality.

Implements TASK-C4: Abstractive Summarization tests
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import os

from scripts.tools.extraction import (
    generate_abstractive_summary,
    SummarizationConfig,
    generate_summary,
)


class TestSummarizationConfig:
    """Test cases for SummarizationConfig."""
    
    def test_default_values(self):
        """Test default configuration values."""
        config = SummarizationConfig()
        
        assert config.max_length == 200
        assert config.style == 'concise'
        assert config.use_abstractive is False
        assert config.model == 'openai'
        assert config.api_key is None
        assert config.fallback_to_extractive is True
    
    def test_custom_values(self):
        """Test custom configuration values."""
        config = SummarizationConfig(
            max_length=500,
            style='detailed',
            use_abstractive=True,
            model='local',
            api_key='test-key'
        )
        
        assert config.max_length == 500
        assert config.style == 'detailed'
        assert config.use_abstractive is True
        assert config.model == 'local'
        assert config.api_key == 'test-key'


class TestAbstractiveSummary:
    """Test cases for abstractive summarization."""
    
    def test_extractive_mode(self):
        """Test using extractive mode (default)."""
        text = "机器学习是人工智能的核心技术。深度学习是机器学习的重要分支。自然语言处理是AI的重要应用领域。"
        
        config = SummarizationConfig(use_abstractive=False)
        result = generate_abstractive_summary(text, config=config)
        
        assert 'summary' in result
        assert result['method'] == 'extractive'
        assert result['model'] == 'extractive'
        assert len(result['summary']) <= config.max_length * 1.5
        assert result['language'] == 'zh'
    
    def test_english_text_extractive(self):
        """Test with English text in extractive mode."""
        text = "Machine learning is the core technology of artificial intelligence. Deep learning is an important branch of machine learning. Natural language processing is a key application of AI."
        
        config = SummarizationConfig(use_abstractive=False, max_length=100)
        result = generate_abstractive_summary(text, config=config)
        
        assert 'summary' in result
        assert result['language'] == 'en'
    
    def test_kwargs_override_config(self):
        """Test that kwargs override config values."""
        text = "测试文本内容。" * 20
        
        config = SummarizationConfig(max_length=200)
        result = generate_abstractive_summary(text, config=config, max_length=100)
        
        # Should use the max_length from kwargs
        assert result['summary_length'] <= 100 * 1.5
    
    def test_empty_text_raises_error(self):
        """Test that empty text raises ValueError."""
        with pytest.raises(ValueError, match="Text cannot be empty"):
            generate_abstractive_summary("")
    
    def test_whitespace_text_raises_error(self):
        """Test that whitespace-only text raises ValueError."""
        with pytest.raises(ValueError, match="Text cannot be empty"):
            generate_abstractive_summary("   \n\t  ")
    
    @patch('scripts.tools.extraction._generate_abstractive_openai')
    def test_openai_mode_success(self, mock_openai):
        """Test OpenAI mode with successful API call."""
        mock_openai.return_value = "这是AI生成的摘要。"
        
        text = "这是一段很长的文本。" * 100
        config = SummarizationConfig(
            use_abstractive=True,
            model='openai',
            api_key='test-key'
        )
        
        result = generate_abstractive_summary(text, config=config)
        
        assert result['method'] == 'abstractive'
        assert result['model'] == 'openai'
        assert result['summary'] == "这是AI生成的摘要。"
        mock_openai.assert_called_once()
    
    @patch('scripts.tools.extraction._generate_abstractive_openai')
    def test_openai_failure_fallback(self, mock_openai):
        """Test fallback to extractive when OpenAI fails."""
        mock_openai.side_effect = Exception("API Error")
        
        text = "测试文本内容。" * 50
        config = SummarizationConfig(
            use_abstractive=True,
            model='openai',
            api_key='test-key',
            fallback_to_extractive=True
        )
        
        result = generate_abstractive_summary(text, config=config)
        
        assert 'extractive' in result['method']
        assert 'summary' in result
    
    @patch('scripts.tools.extraction._generate_abstractive_openai')
    def test_openai_failure_no_fallback(self, mock_openai):
        """Test exception when fallback is disabled."""
        mock_openai.side_effect = Exception("API Error")
        
        text = "测试文本内容。" * 50
        config = SummarizationConfig(
            use_abstractive=True,
            model='openai',
            api_key='test-key',
            fallback_to_extractive=False
        )
        
        with pytest.raises(Exception, match="API Error"):
            generate_abstractive_summary(text, config=config)
    
    @patch('scripts.tools.extraction._generate_abstractive_local')
    def test_local_model_success(self, mock_local):
        """Test local model mode."""
        mock_local.return_value = "Local model summary."
        
        text = "Test text content. " * 50
        config = SummarizationConfig(
            use_abstractive=True,
            model='local'
        )
        
        result = generate_abstractive_summary(text, config=config)
        
        assert result['method'] == 'abstractive'
        assert result['model'] == 'local'
        mock_local.assert_called_once()
    
    def test_compression_ratio(self):
        """Test compression ratio calculation."""
        text = "这是一段测试文本。" * 100
        
        config = SummarizationConfig(use_abstractive=False, max_length=50)
        result = generate_abstractive_summary(text, config=config)
        
        assert result['compression_ratio'] > 0
        assert result['compression_ratio'] <= 1.0
        # Note: compression_ratio is rounded to 2 decimal places
        expected_ratio = round(result['summary_length'] / result['original_length'], 2)
        assert result['compression_ratio'] == expected_ratio
    
    def test_different_styles(self):
        """Test different summary styles."""
        text = "测试文本内容。" * 50
        
        for style in ['concise', 'detailed', 'bullet']:
            config = SummarizationConfig(
                use_abstractive=False,
                style=style
            )
            result = generate_abstractive_summary(text, config=config)
            assert 'summary' in result


class TestOpenAISummaryGeneration:
    """Test cases for OpenAI summary generation."""
    
    def test_openai_api_call(self):
        """Test OpenAI API is called with correct parameters."""
        # Create mock client
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Generated summary"
        mock_client.chat.completions.create.return_value = mock_response
        
        # Mock the openai module and OpenAI class
        mock_openai = MagicMock()
        mock_openai.OpenAI.return_value = mock_client
        
        from scripts.tools.extraction import _generate_abstractive_openai
        
        text = "测试文本内容。" * 50
        config = SummarizationConfig(
            api_key='test-key',
            style='concise'
        )
        
        # Patch the openai import in the module
        with patch.dict('sys.modules', {'openai': mock_openai}):
            result = _generate_abstractive_openai(text, config, 'zh')
        
        assert result == "Generated summary"
    
    def test_missing_api_key(self):
        """Test error when API key is missing."""
        from scripts.tools.extraction import _generate_abstractive_openai
        
        text = "测试文本内容。"
        config = SummarizationConfig(api_key=None)
        
        # Clear environment variable for this test
        # The function should raise ValueError before trying to import openai
        # when api_key is None and OPENAI_API_KEY env var is not set
        with patch.dict(os.environ, {'OPENAI_API_KEY': ''}, clear=False):
            # Mock openai to be available (so we get past the import check)
            mock_openai = MagicMock()
            with patch.dict('sys.modules', {'openai': mock_openai}):
                with pytest.raises(ValueError, match="API key required"):
                    _generate_abstractive_openai(text, config, 'zh')


class TestLocalSummaryGeneration:
    """Test cases for local model summary generation."""
    
    @patch('scripts.tools.extraction.generate_summary')
    def test_fallback_when_transformers_unavailable(self, mock_generate):
        """Test fallback to extractive when transformers unavailable."""
        mock_generate.return_value = {
            'summary': 'Extractive summary',
            'key_sentences': ['Extractive summary']
        }
        
        from scripts.tools.extraction import _generate_abstractive_local
        
        text = "测试文本内容。"
        config = SummarizationConfig(max_length=100)
        
        # Mock ImportError for transformers
        with patch.dict('sys.modules', {'transformers': None}):
            result = _generate_abstractive_local(text, config, 'zh')
        
        assert result == 'Extractive summary'


class TestIntegration:
    """Integration tests for abstractive summarization."""
    
    def test_full_workflow_extractive(self):
        """Test full workflow with extractive summarization."""
        text = """
        机器学习是人工智能的一个重要分支。它使计算机能够从数据中学习模式，
        而不需要显式编程。深度学习是机器学习的一个子集，使用多层神经网络
        来处理复杂的数据。自然语言处理是AI的一个重要应用领域。
        """
        
        config = SummarizationConfig(
            use_abstractive=False,
            max_length=100
        )
        
        result = generate_abstractive_summary(text.strip(), config=config)
        
        assert 'summary' in result
        assert len(result['summary']) > 0
        assert result['language'] == 'zh'
        assert result['compression_ratio'] < 1.0
    
    def test_english_full_workflow(self):
        """Test full workflow with English text."""
        text = """
        Machine learning is an important branch of artificial intelligence.
        It enables computers to learn patterns from data without explicit programming.
        Deep learning is a subset of machine learning that uses multi-layer neural
        networks to process complex data. Natural language processing is an important
        application area of AI.
        """
        
        config = SummarizationConfig(
            use_abstractive=False,
            max_length=150
        )
        
        result = generate_abstractive_summary(text.strip(), config=config)
        
        assert 'summary' in result
        assert result['language'] == 'en'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
