"""
Tests for multi-language support functionality.

Implements TASK-C5: Multi-language Support tests
"""

import pytest
from unittest.mock import Mock, patch

from scripts.utils.language import (
    detect_language,
    get_stop_words,
    is_stop_word,
    tokenize,
    normalize_text,
    remove_stop_words,
    get_text_statistics,
    LanguageInfo,
    LanguageProcessor,
    language_processor,
    is_chinese_char,
    is_english_char,
    count_chinese_chars,
    count_english_chars,
    CHINESE_STOP_WORDS,
    ENGLISH_STOP_WORDS,
)
from scripts.tools.extraction import (
    extract_keywords,
    generate_summary,
    get_text_info,
)


class TestChineseCharacterDetection:
    """Test cases for Chinese character detection."""
    
    def test_is_chinese_char(self):
        """Test detecting Chinese characters."""
        assert is_chinese_char('中') is True
        assert is_chinese_char('文') is True
        assert is_chinese_char('a') is False
        assert is_chinese_char('A') is False
        assert is_chinese_char('1') is False
        assert is_chinese_char(' ') is False
    
    def test_count_chinese_chars(self):
        """Test counting Chinese characters."""
        assert count_chinese_chars("中文测试") == 4
        assert count_chinese_chars("中文Test") == 2
        assert count_chinese_chars("Test123") == 0
        assert count_chinese_chars("") == 0
    
    def test_is_english_char(self):
        """Test detecting English characters."""
        assert is_english_char('a') is True
        assert is_english_char('Z') is True
        assert is_english_char('中') is False
        assert is_english_char('1') is False
    
    def test_count_english_chars(self):
        """Test counting English characters."""
        assert count_english_chars("Hello") == 5
        assert count_english_chars("Hello世界") == 5
        assert count_english_chars("世界") == 0
        assert count_english_chars("") == 0


class TestLanguageDetection:
    """Test cases for language detection."""
    
    def test_detect_chinese(self):
        """Test detecting Chinese text."""
        text = "这是一段中文文本，用于测试语言检测功能。"
        result = detect_language(text)
        
        assert result.code == 'zh'
        assert result.name == 'Chinese'
        assert result.confidence > 0.5
    
    def test_detect_english(self):
        """Test detecting English text."""
        text = "This is an English text for testing language detection."
        result = detect_language(text)
        
        assert result.code == 'en'
        assert result.name == 'English'
        assert result.confidence > 0.5
    
    def test_detect_empty_text(self):
        """Test detecting empty text."""
        result = detect_language("")
        
        assert result.code == 'unknown'
        assert result.confidence == 0.0
    
    def test_detect_mixed_text(self):
        """Test detecting mixed language text."""
        text = "这是Chinese mixed文本"
        result = detect_language(text)
        
        assert result.is_mixed is True
    
    def test_detect_whitespace(self):
        """Test detecting whitespace-only text."""
        result = detect_language("   \n\t  ")
        
        assert result.code == 'unknown'


class TestStopWords:
    """Test cases for stop words."""
    
    def test_get_chinese_stop_words(self):
        """Test getting Chinese stop words."""
        stop_words = get_stop_words('zh')
        
        assert '的' in stop_words
        assert '是' in stop_words
        assert '在' in stop_words
        assert len(stop_words) > 0
    
    def test_get_english_stop_words(self):
        """Test getting English stop words."""
        stop_words = get_stop_words('en')
        
        assert 'the' in stop_words
        assert 'is' in stop_words
        assert 'and' in stop_words
        assert len(stop_words) > 0
    
    def test_get_unknown_language_stop_words(self):
        """Test getting stop words for unknown language."""
        stop_words = get_stop_words('unknown')
        
        assert stop_words == set()
    
    def test_is_stop_word_chinese(self):
        """Test checking Chinese stop word."""
        assert is_stop_word('的', 'zh') is True
        assert is_stop_word('机器学习', 'zh') is False
    
    def test_is_stop_word_english(self):
        """Test checking English stop word."""
        assert is_stop_word('the', 'en') is True
        assert is_stop_word('machine', 'en') is False
    
    def test_is_stop_word_auto_detect(self):
        """Test auto-detecting language for stop word check."""
        assert is_stop_word('的', 'auto') is True
        assert is_stop_word('the', 'auto') is True


class TestTokenization:
    """Test cases for tokenization."""
    
    def test_tokenize_chinese(self):
        """Test tokenizing Chinese text."""
        text = "机器学习是人工智能"
        tokens = tokenize(text, 'zh')
        
        assert isinstance(tokens, list)
        assert len(tokens) > 0
    
    def test_tokenize_english(self):
        """Test tokenizing English text."""
        text = "Machine learning is AI"
        tokens = tokenize(text, 'en')
        
        assert tokens == ['machine', 'learning', 'is', 'ai']
    
    def test_tokenize_auto(self):
        """Test auto-detecting language for tokenization."""
        text_zh = "中文文本"
        text_en = "English text"
        
        tokens_zh = tokenize(text_zh, 'auto')
        tokens_en = tokenize(text_en, 'auto')
        
        assert len(tokens_zh) > 0
        assert len(tokens_en) > 0
    
    def test_tokenize_empty(self):
        """Test tokenizing empty text."""
        assert tokenize("", 'en') == []
        assert tokenize("", 'zh') == []


class TestTextNormalization:
    """Test cases for text normalization."""
    
    def test_normalize_whitespace(self):
        """Test normalizing whitespace."""
        text = "Hello    world\n\n"
        result = normalize_text(text, 'en')
        
        assert "    " not in result
        assert "\n\n" not in result
    
    def test_normalize_lowercase_english(self):
        """Test lowercasing English text."""
        text = "Hello WORLD"
        result = normalize_text(text, 'en')
        
        assert result == "hello world"
    
    def test_normalize_chinese(self):
        """Test normalizing Chinese text (should not lowercase)."""
        text = "中文文本"
        result = normalize_text(text, 'zh')
        
        assert "中文" in result


class TestTextStatistics:
    """Test cases for text statistics."""
    
    def test_statistics_chinese(self):
        """Test statistics for Chinese text."""
        text = "这是一段中文测试文本"
        stats = get_text_statistics(text)
        
        assert stats['total_chars'] == len(text)
        assert stats['chinese_chars'] > 0
        assert stats['language'] == 'zh'
    
    def test_statistics_english(self):
        """Test statistics for English text."""
        text = "This is an English test text"
        stats = get_text_statistics(text)
        
        assert stats['total_chars'] == len(text)
        assert stats['english_chars'] > 0
        assert stats['language'] == 'en'
    
    def test_statistics_empty(self):
        """Test statistics for empty text."""
        stats = get_text_statistics("")
        
        assert stats['total_chars'] == 0
        assert stats['language'] == 'unknown'


class TestLanguageProcessor:
    """Test cases for LanguageProcessor class."""
    
    def test_processor_creation(self):
        """Test creating a language processor."""
        processor = LanguageProcessor(default_language='zh')
        
        assert processor.default_language == 'zh'
    
    def test_processor_detect(self):
        """Test processor detect method."""
        processor = LanguageProcessor()
        
        result = processor.detect("中文文本")
        assert result.code == 'zh'
    
    def test_processor_tokenize(self):
        """Test processor tokenize method."""
        processor = LanguageProcessor(default_language='en')
        
        tokens = processor.tokenize("Hello world")
        assert tokens == ['hello', 'world']
    
    def test_processor_tokenize_remove_stops(self):
        """Test processor tokenize with stop word removal."""
        processor = LanguageProcessor(default_language='en')
        
        tokens = processor.tokenize("The quick fox", remove_stops=True)
        assert 'the' not in [t.lower() for t in tokens]
    
    def test_processor_get_stop_words(self):
        """Test processor stop words caching."""
        processor = LanguageProcessor()
        
        stops1 = processor.get_stop_words('en')
        stops2 = processor.get_stop_words('en')
        
        assert stops1 is stops2  # Should be cached


class TestKeywordExtractionMultiLanguage:
    """Test cases for multi-language keyword extraction."""
    
    def test_extract_keywords_chinese(self):
        """Test extracting keywords from Chinese text."""
        text = "机器学习是人工智能的核心技术。深度学习是机器学习的重要分支。"
        keywords = extract_keywords(text, language='zh', top_n=5)
        
        assert isinstance(keywords, list)
        assert len(keywords) <= 5
        if keywords:
            assert 'keyword' in keywords[0]
            assert 'score' in keywords[0]
    
    def test_extract_keywords_english(self):
        """Test extracting keywords from English text."""
        text = "Machine learning is a core technology of artificial intelligence. Deep learning is an important branch of machine learning."
        keywords = extract_keywords(text, language='en', top_n=5)
        
        assert isinstance(keywords, list)
        assert len(keywords) <= 5
        if keywords:
            assert 'keyword' in keywords[0]
            assert 'score' in keywords[0]
    
    def test_extract_keywords_auto_detect(self):
        """Test auto-detecting language for keyword extraction."""
        text_zh = "机器学习技术"
        text_en = "Machine learning technology"
        
        keywords_zh = extract_keywords(text_zh, language='auto')
        keywords_en = extract_keywords(text_en, language='auto')
        
        assert isinstance(keywords_zh, list)
        assert isinstance(keywords_en, list)
    
    def test_extract_keywords_tfidf_vs_textrank(self):
        """Test comparing TF-IDF and TextRank methods."""
        text = "机器学习是人工智能的核心。人工智能正在改变世界。"
        
        keywords_tfidf = extract_keywords(text, method='tfidf', top_n=5)
        keywords_textrank = extract_keywords(text, method='textrank', top_n=5)
        
        assert isinstance(keywords_tfidf, list)
        assert isinstance(keywords_textrank, list)


class TestSummaryMultiLanguage:
    """Test cases for multi-language summarization."""
    
    def test_summary_chinese(self):
        """Test generating summary for Chinese text."""
        text = "机器学习是人工智能的核心技术。深度学习是机器学习的重要分支。自然语言处理是AI的重要应用领域。计算机视觉也是重要方向。"
        result = generate_summary(text, max_length=50, language='zh')
        
        assert 'summary' in result
        assert len(result['summary']) <= 60  # Allow some flexibility
        assert result['language'] == 'zh'
    
    def test_summary_english(self):
        """Test generating summary for English text."""
        text = "Machine learning is the core technology of AI. Deep learning is an important branch of machine learning. Natural language processing is a key application area."
        result = generate_summary(text, max_length=100, language='en')
        
        assert 'summary' in result
        assert result['language'] == 'en'
    
    def test_summary_auto_detect(self):
        """Test auto-detecting language for summarization."""
        text_zh = "中文摘要测试文本。这是第二句话。这是第三句话。"
        text_en = "English summary test text. This is the second sentence. This is the third sentence."
        
        result_zh = generate_summary(text_zh, language='auto')
        result_en = generate_summary(text_en, language='auto')
        
        assert result_zh['language'] == 'zh'
        assert result_en['language'] == 'en'


class TestGetTextInfo:
    """Test cases for get_text_info function."""
    
    def test_text_info_chinese(self):
        """Test getting info for Chinese text."""
        text = "机器学习是人工智能的核心技术。"
        info = get_text_info(text)
        
        assert 'statistics' in info
        assert 'language' in info
        assert 'keywords' in info
        assert info['language'] == 'zh'
    
    def test_text_info_english(self):
        """Test getting info for English text."""
        text = "Machine learning is a core technology."
        info = get_text_info(text)
        
        assert info['language'] == 'en'
        assert isinstance(info['keywords'], list)
    
    def test_text_info_empty(self):
        """Test getting info for empty text."""
        info = get_text_info("")
        
        assert info['language'] == 'unknown'
        assert info['keywords'] == []


class TestIntegration:
    """Integration tests for multi-language support."""
    
    def test_full_pipeline_chinese(self):
        """Test full pipeline with Chinese text."""
        text = """
        机器学习是人工智能的一个重要分支。
        它使计算机能够从数据中学习模式，而不需要显式编程。
        深度学习是机器学习的一个子集，使用多层神经网络处理复杂数据。
        自然语言处理是AI的重要应用领域。
        """
        
        # Detect language
        lang_info = detect_language(text)
        assert lang_info.code == 'zh'
        
        # Extract keywords
        keywords = extract_keywords(text, language='zh', top_n=5)
        assert len(keywords) > 0
        
        # Generate summary
        summary = generate_summary(text, max_length=100, language='zh')
        assert len(summary['summary']) > 0
    
    def test_full_pipeline_english(self):
        """Test full pipeline with English text."""
        text = """
        Machine learning is an important branch of artificial intelligence.
        It enables computers to learn patterns from data without explicit programming.
        Deep learning is a subset of machine learning using multi-layer neural networks.
        Natural language processing is an important AI application area.
        """
        
        # Detect language
        lang_info = detect_language(text)
        assert lang_info.code == 'en'
        
        # Extract keywords
        keywords = extract_keywords(text, language='en', top_n=5)
        assert len(keywords) > 0
        
        # Generate summary
        summary = generate_summary(text, max_length=150, language='en')
        assert len(summary['summary']) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
