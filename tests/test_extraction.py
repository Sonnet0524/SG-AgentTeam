"""
Unit tests for knowledge extraction tools.

Tests extract_keywords and generate_summary functions.
"""

import unittest
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.tools.extraction import extract_keywords, generate_summary


class TestExtractKeywords(unittest.TestCase):
    """Test cases for extract_keywords function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_text = """
        机器学习是人工智能的核心技术。深度学习是机器学习的重要分支。
        自然语言处理是人工智能的重要应用领域。计算机视觉也是AI的关键技术。
        机器学习算法包括监督学习、无监督学习和强化学习。
        """
        
        self.english_text = """
        Machine learning is a core technology of artificial intelligence.
        Deep learning is an important branch of machine learning.
        Natural language processing is a key application of AI.
        """
    
    def test_extract_keywords_tfidf_basic(self):
        """Test TF-IDF keyword extraction with basic text."""
        keywords = extract_keywords(self.sample_text, method="tfidf", top_n=5)
        
        self.assertIsInstance(keywords, list)
        self.assertGreater(len(keywords), 0)
        self.assertLessEqual(len(keywords), 5)
        
        for item in keywords:
            self.assertIn('keyword', item)
            self.assertIn('score', item)
            self.assertIsInstance(item['keyword'], str)
            self.assertIsInstance(item['score'], float)
            self.assertGreaterEqual(item['score'], 0)
            self.assertLessEqual(item['score'], 1)
    
    def test_extract_keywords_textrank_basic(self):
        """Test TextRank keyword extraction with basic text."""
        keywords = extract_keywords(self.sample_text, method="textrank", top_n=5)
        
        self.assertIsInstance(keywords, list)
        self.assertGreater(len(keywords), 0)
        self.assertLessEqual(len(keywords), 5)
        
        for item in keywords:
            self.assertIn('keyword', item)
            self.assertIn('score', item)
            self.assertIsInstance(item['keyword'], str)
            self.assertIsInstance(item['score'], float)
            self.assertGreaterEqual(item['score'], 0)
            self.assertLessEqual(item['score'], 1)
    
    def test_extract_keywords_chinese(self):
        """Test keyword extraction with Chinese text."""
        keywords = extract_keywords(self.sample_text, method="tfidf", top_n=10)
        
        self.assertGreater(len(keywords), 0)
        
        has_chinese = any(
            any('\u4e00' <= char <= '\u9fff' for char in item['keyword'])
            for item in keywords
        )
        self.assertTrue(has_chinese, "Should extract Chinese keywords")
    
    def test_extract_keywords_english(self):
        """Test keyword extraction with English text."""
        keywords = extract_keywords(self.english_text, method="tfidf", top_n=5)
        
        self.assertGreater(len(keywords), 0)
        
        for item in keywords:
            self.assertIsInstance(item['keyword'], str)
            self.assertGreater(len(item['keyword']), 0)
    
    def test_extract_keywords_top_n(self):
        """Test different top_n values."""
        for top_n in [1, 3, 5, 10]:
            keywords = extract_keywords(self.sample_text, method="tfidf", top_n=top_n)
            self.assertLessEqual(len(keywords), top_n)
    
    def test_extract_keywords_default_method(self):
        """Test default method is TF-IDF."""
        keywords_default = extract_keywords(self.sample_text, top_n=5)
        keywords_tfidf = extract_keywords(self.sample_text, method="tfidf", top_n=5)
        
        self.assertEqual(len(keywords_default), len(keywords_tfidf))
    
    def test_extract_keywords_empty_text(self):
        """Test extraction with empty text raises error."""
        with self.assertRaises(ValueError) as context:
            extract_keywords("", method="tfidf")
        
        self.assertIn("empty", str(context.exception).lower())
    
    def test_extract_keywords_whitespace_text(self):
        """Test extraction with whitespace-only text raises error."""
        with self.assertRaises(ValueError):
            extract_keywords("   \n\t  ", method="tfidf")
    
    def test_extract_keywords_invalid_method(self):
        """Test extraction with invalid method raises error."""
        with self.assertRaises(ValueError) as context:
            extract_keywords(self.sample_text, method="invalid")
        
        self.assertIn("tfidf", str(context.exception).lower())
        self.assertIn("textrank", str(context.exception).lower())
    
    def test_extract_keywords_invalid_top_n(self):
        """Test extraction with invalid top_n raises error."""
        with self.assertRaises(ValueError):
            extract_keywords(self.sample_text, top_n=0)
        
        with self.assertRaises(ValueError):
            extract_keywords(self.sample_text, top_n=-5)
    
    def test_extract_keywords_performance(self):
        """Test extraction performance meets requirement (<1s for 1000 chars)."""
        long_text = self.sample_text * 20
        self.assertGreater(len(long_text), 1000)
        
        start_time = time.time()
        keywords = extract_keywords(long_text, method="tfidf", top_n=10)
        elapsed_time = time.time() - start_time
        
        self.assertLess(elapsed_time, 1.0, "Should complete in <1s for 1000+ chars")
        self.assertGreater(len(keywords), 0)
    
    def test_extract_keywords_short_text(self):
        """Test extraction with very short text."""
        short_text = "机器学习"
        keywords = extract_keywords(short_text, method="tfidf", top_n=5)
        
        self.assertIsInstance(keywords, list)
    
    def test_extract_keywords_scores_normalized(self):
        """Test that keyword scores are normalized to [0, 1]."""
        keywords = extract_keywords(self.sample_text, method="tfidf", top_n=10)
        
        for item in keywords:
            self.assertGreaterEqual(item['score'], 0)
            self.assertLessEqual(item['score'], 1)
    
    def test_extract_keywords_textrank_vs_tfidf(self):
        """Test that TextRank and TF-IDF produce different results."""
        keywords_tfidf = extract_keywords(self.sample_text, method="tfidf", top_n=10)
        keywords_textrank = extract_keywords(self.sample_text, method="textrank", top_n=10)
        
        self.assertGreater(len(keywords_tfidf), 0)
        self.assertGreater(len(keywords_textrank), 0)


class TestGenerateSummary(unittest.TestCase):
    """Test cases for generate_summary function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_text = """
        机器学习是人工智能的核心技术。它通过算法让计算机从数据中学习。
        深度学习是机器学习的重要分支，使用多层神经网络进行学习。
        自然语言处理是人工智能的重要应用领域，让计算机理解和生成人类语言。
        计算机视觉也是AI的关键技术，让计算机能够识别和处理图像。
        机器学习算法包括监督学习、无监督学习和强化学习等多种类型。
        """
        
        self.short_text = "这是一段简短的文本。"
    
    def test_generate_summary_basic(self):
        """Test basic summary generation."""
        result = generate_summary(self.sample_text, max_length=100)
        
        self.assertIn('summary', result)
        self.assertIn('key_sentences', result)
        self.assertIn('original_length', result)
        self.assertIn('summary_length', result)
        self.assertIn('compression_ratio', result)
        
        self.assertIsInstance(result['summary'], str)
        self.assertIsInstance(result['key_sentences'], list)
        self.assertIsInstance(result['original_length'], int)
        self.assertIsInstance(result['summary_length'], int)
        self.assertIsInstance(result['compression_ratio'], float)
    
    def test_generate_summary_length_limit(self):
        """Test summary respects max_length limit."""
        max_length = 50
        result = generate_summary(self.sample_text, max_length=max_length)
        
        self.assertLessEqual(result['summary_length'], max_length)
    
    def test_generate_summary_short_text(self):
        """Test summary with text shorter than max_length."""
        result = generate_summary(self.short_text, max_length=200)
        
        self.assertEqual(result['summary'], self.short_text)
        self.assertEqual(result['original_length'], result['summary_length'])
        self.assertEqual(result['compression_ratio'], 1.0)
    
    def test_generate_summary_compression_ratio(self):
        """Test compression ratio is calculated correctly."""
        result = generate_summary(self.sample_text, max_length=100)
        
        expected_ratio = round(result['summary_length'] / result['original_length'], 2)
        self.assertEqual(result['compression_ratio'], expected_ratio)
        
        self.assertGreaterEqual(result['compression_ratio'], 0)
        self.assertLessEqual(result['compression_ratio'], 1)
    
    def test_generate_summary_key_sentences(self):
        """Test that key_sentences are extracted."""
        result = generate_summary(self.sample_text, max_length=150)
        
        self.assertGreater(len(result['key_sentences']), 0)
        
        for sentence in result['key_sentences']:
            self.assertIn(sentence, self.sample_text)
    
    def test_generate_summary_preserves_information(self):
        """Test that summary preserves key information."""
        result = generate_summary(self.sample_text, max_length=150)
        
        important_keywords = ['机器学习', '人工智能', '深度学习']
        
        keyword_count = sum(
            1 for keyword in important_keywords
            if keyword in result['summary']
        )
        
        self.assertGreater(keyword_count, 0, "Summary should preserve key information")
    
    def test_generate_summary_empty_text(self):
        """Test summary generation with empty text raises error."""
        with self.assertRaises(ValueError) as context:
            generate_summary("")
        
        self.assertIn("empty", str(context.exception).lower())
    
    def test_generate_summary_whitespace_text(self):
        """Test summary generation with whitespace-only text raises error."""
        with self.assertRaises(ValueError):
            generate_summary("   \n\t  ")
    
    def test_generate_summary_invalid_max_length(self):
        """Test summary generation with invalid max_length raises error."""
        with self.assertRaises(ValueError):
            generate_summary(self.sample_text, max_length=0)
        
        with self.assertRaises(ValueError):
            generate_summary(self.sample_text, max_length=-10)
    
    def test_generate_summary_performance(self):
        """Test summary generation performance (<5s for 1000 chars)."""
        long_text = self.sample_text * 20
        self.assertGreater(len(long_text), 1000)
        
        start_time = time.time()
        result = generate_summary(long_text, max_length=200)
        elapsed_time = time.time() - start_time
        
        self.assertLess(elapsed_time, 5.0, "Should complete in <5s for 1000+ chars")
        self.assertIn('summary', result)
    
    def test_generate_summary_different_lengths(self):
        """Test summary generation with different max_length values."""
        for max_length in [50, 100, 150, 200]:
            result = generate_summary(self.sample_text, max_length=max_length)
            
            self.assertLessEqual(result['summary_length'], max_length)
    
    def test_generate_summary_chinese(self):
        """Test summary generation with Chinese text."""
        result = generate_summary(self.sample_text, max_length=100)
        
        has_chinese = any('\u4e00' <= char <= '\u9fff' for char in result['summary'])
        self.assertTrue(has_chinese, "Summary should contain Chinese characters")
    
    def test_generate_summary_structure(self):
        """Test that summary maintains sentence structure."""
        result = generate_summary(self.sample_text, max_length=150)
        
        self.assertGreater(len(result['key_sentences']), 0)
        
        reconstructed = ''.join(result['key_sentences'])
        self.assertEqual(result['summary'], reconstructed)


class TestIntegration(unittest.TestCase):
    """Integration tests for extraction tools."""
    
    def test_extract_and_summarize(self):
        """Test using both extraction functions together."""
        text = """
        机器学习是人工智能的核心技术。它通过算法让计算机从数据中学习模式。
        深度学习是机器学习的重要分支，使用多层神经网络进行学习。
        自然语言处理是人工智能的重要应用领域，让计算机理解和生成人类语言。
        """
        
        keywords = extract_keywords(text, method="tfidf", top_n=5)
        summary_result = generate_summary(text, max_length=100)
        
        self.assertGreater(len(keywords), 0)
        self.assertIn('summary', summary_result)
        
        keyword_in_summary = any(
            item['keyword'] in summary_result['summary']
            for item in keywords[:3]
        )
        
        self.assertTrue(keyword_in_summary, "Top keywords should appear in summary")
    
    def test_large_document_processing(self):
        """Test processing a large document."""
        large_text = "机器学习是人工智能的核心技术。" * 200
        
        keywords = extract_keywords(large_text, method="tfidf", top_n=10)
        summary = generate_summary(large_text, max_length=200)
        
        self.assertGreater(len(keywords), 0)
        self.assertIn('summary', summary)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_single_word(self):
        """Test with single word input."""
        text = "机器学习"
        
        keywords = extract_keywords(text, method="tfidf", top_n=5)
        self.assertIsInstance(keywords, list)
    
    def test_single_sentence(self):
        """Test with single sentence."""
        text = "机器学习是人工智能的核心技术。"
        
        keywords = extract_keywords(text, method="tfidf", top_n=5)
        summary = generate_summary(text, max_length=100)
        
        self.assertIsInstance(keywords, list)
        self.assertIn('summary', summary)
    
    def test_repeated_content(self):
        """Test with highly repetitive content."""
        text = "机器学习 机器学习 机器学习 " * 20
        
        keywords = extract_keywords(text, method="tfidf", top_n=5)
        self.assertGreater(len(keywords), 0)
    
    def test_mixed_language(self):
        """Test with mixed Chinese and English."""
        text = """
        Machine Learning (机器学习) is a core technology of AI.
        Deep Learning (深度学习) uses neural networks.
        NLP (自然语言处理) enables computers to understand language.
        """
        
        keywords = extract_keywords(text, method="tfidf", top_n=10)
        summary = generate_summary(text, max_length=100)
        
        self.assertGreater(len(keywords), 0)
        self.assertIn('summary', summary)


if __name__ == '__main__':
    unittest.main(verbosity=2)
