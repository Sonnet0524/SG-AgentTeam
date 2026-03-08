"""
Knowledge extraction tools for keyword extraction and text summarization.

Implements:
- TASK-C1: extract_keywords and generate_summary functions
- TASK-C4: Abstractive Summarization
- TASK-C5: Multi-language Support
"""

import re
import logging
from typing import List, Dict, Any, Tuple, Optional
from collections import Counter
from dataclasses import dataclass
import os

import jieba
import jieba.analyse
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from scripts.utils.language import (
    detect_language,
    is_stop_word,
    tokenize,
    is_chinese_char,
    get_text_statistics,
    LanguageInfo,
)

logger = logging.getLogger(__name__)


# ==================== Configuration ====================

@dataclass
class SummarizationConfig:
    """Configuration for summarization.
    
    Attributes:
        max_length: Maximum summary length in characters
        style: Summary style ('concise', 'detailed', 'bullet')
        use_abstractive: Whether to use abstractive summarization
        model: Model to use for abstractive summarization ('openai', 'local')
        api_key: API key for OpenAI (or set OPENAI_API_KEY env var)
        fallback_to_extractive: Fall back to extractive if abstractive fails
    """
    
    max_length: int = 200
    style: str = 'concise'
    use_abstractive: bool = False
    model: str = 'openai'
    api_key: Optional[str] = None
    fallback_to_extractive: bool = True


# ==================== Keyword Extraction ====================

def extract_keywords(
    text: str,
    method: str = "tfidf",
    top_n: int = 10,
    language: str = "auto"
) -> List[Dict[str, Any]]:
    """
    Extract keywords from text using TF-IDF or TextRank method.
    
    Supports both Chinese and English text with automatic language detection.
    
    Args:
        text: Input text (supports Chinese and English)
        method: Extraction method - "tfidf" or "textrank" (default: "tfidf")
        top_n: Number of keywords to extract (default: 10)
        language: Language code ('zh', 'en', or 'auto' for auto-detection)
    
    Returns:
        List of keyword dictionaries, each containing:
            - 'keyword': str - the extracted keyword
            - 'score': float - importance score (0-1)
        
        Example:
        [
            {'keyword': '机器学习', 'score': 0.85},
            {'keyword': '深度学习', 'score': 0.72}
        ]
    
    Raises:
        ValueError: If method is not "tfidf" or "textrank"
        ValueError: If text is empty
    
    Example:
        >>> text = "机器学习是人工智能的核心技术，深度学习是机器学习的重要分支。"
        >>> keywords = extract_keywords(text, method="tfidf", top_n=5)
        >>> print(keywords[0]['keyword'])
        '机器学习'
        
        >>> text = "Machine learning is the core technology of AI."
        >>> keywords = extract_keywords(text, method="tfidf", top_n=5)
    
    Performance:
        - 1000 characters: <1s
        - 5000 characters: <2s
    """
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")
    
    if method not in ["tfidf", "textrank"]:
        raise ValueError(f"Method must be 'tfidf' or 'textrank', got '{method}'")
    
    if top_n <= 0:
        raise ValueError("top_n must be positive")
    
    # Detect language if auto
    if language == "auto":
        lang_info = detect_language(text)
        language = lang_info.code
    
    if method == "tfidf":
        return _extract_keywords_tfidf(text, top_n, language)
    else:
        return _extract_keywords_textrank(text, top_n, language)


def _tokenize_text(text: str, language: str) -> List[str]:
    """Tokenize text based on language.
    
    Args:
        text: Input text
        language: Language code ('zh' or 'en')
        
    Returns:
        List of tokens
    """
    if language == 'zh':
        # Use jieba for Chinese
        words = jieba.lcut(text)
    else:
        # Simple tokenization for English
        words = re.findall(r'\b\w+\b', text.lower())
    
    # Filter words
    filtered_words = [
        word.lower().strip()
        for word in words
        if len(word.strip()) > 1
        and not word.isspace()
        and not is_stop_word(word, language)
        and _is_valid_word(word)
    ]
    
    return filtered_words


def _is_valid_word(word: str) -> bool:
    """
    Check if a word is valid (contains letters or Chinese characters).
    
    Args:
        word: Word to check
    
    Returns:
        True if word is valid, False otherwise
    """
    if not word or word.isspace():
        return False
    
    has_letter = any(c.isalpha() for c in word)
    has_chinese = any(is_chinese_char(c) for c in word)
    
    return has_letter or has_chinese


def _extract_keywords_tfidf(
    text: str,
    top_n: int,
    language: str
) -> List[Dict[str, Any]]:
    """
    Extract keywords using TF-IDF method.
    
    Args:
        text: Input text
        top_n: Number of keywords to extract
        language: Language code
    
    Returns:
        List of keyword dictionaries with 'keyword' and 'score'
    """
    words = _tokenize_text(text, language)
    
    if not words:
        return []
    
    word_freq = Counter(words)
    total_words = len(words)
    
    processed_text = ' '.join(words)
    
    vectorizer = TfidfVectorizer(
        lowercase=False,
        max_features=100,
        token_pattern=r'(?u)\b\w+\b'
    )
    
    try:
        tfidf_matrix = vectorizer.fit_transform([processed_text])
        feature_names = vectorizer.get_feature_names_out()
        tfidf_scores = tfidf_matrix.toarray()[0]
        
        word_tfidf = dict(zip(feature_names, tfidf_scores))
        
        keywords = []
        for word, tfidf_score in sorted(word_tfidf.items(), key=lambda x: x[1], reverse=True)[:top_n]:
            if tfidf_score > 0:
                normalized_score = min(tfidf_score, 1.0)
                keywords.append({
                    'keyword': word,
                    'score': round(normalized_score, 4)
                })
        
        return keywords
        
    except Exception as e:
        logger.warning(f"TF-IDF extraction failed: {e}, falling back to frequency-based")
        
        keywords = []
        for word, count in word_freq.most_common(top_n):
            normalized_score = min(count / total_words * 2, 1.0)
            keywords.append({
                'keyword': word,
                'score': round(normalized_score, 4)
            })
        
        return keywords


def _extract_keywords_textrank(
    text: str,
    top_n: int,
    language: str
) -> List[Dict[str, Any]]:
    """
    Extract keywords using TextRank algorithm.
    
    Args:
        text: Input text
        top_n: Number of keywords to extract
        language: Language code
    
    Returns:
        List of keyword dictionaries with 'keyword' and 'score'
    """
    words = _tokenize_text(text, language)
    
    if not words:
        return []
    
    window_size = 4
    graph = nx.Graph()
    
    for i in range(len(words) - window_size + 1):
        window_words = words[i:i + window_size]
        for j in range(len(window_words)):
            for k in range(j + 1, len(window_words)):
                word1 = window_words[j]
                word2 = window_words[k]
                
                if graph.has_edge(word1, word2):
                    graph[word1][word2]['weight'] += 1
                else:
                    graph.add_edge(word1, word2, weight=1)
    
    if graph.number_of_nodes() == 0:
        return []
    
    try:
        scores = nx.pagerank(graph, weight='weight')
        
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
        
        max_score = sorted_words[0][1] if sorted_words else 1.0
        
        keywords = [
            {
                'keyword': word,
                'score': round(score / max_score, 4)
            }
            for word, score in sorted_words
        ]
        
        return keywords
        
    except Exception as e:
        logger.warning(f"TextRank extraction failed: {e}, falling back to frequency-based")
        
        word_freq = Counter(words)
        total_words = len(words)
        
        keywords = []
        for word, count in word_freq.most_common(top_n):
            normalized_score = min(count / total_words * 2, 1.0)
            keywords.append({
                'keyword': word,
                'score': round(normalized_score, 4)
            })
        
        return keywords


# ==================== Extractive Summarization ====================

def generate_summary(
    text: str,
    max_length: int = 200,
    language: str = "auto"
) -> Dict[str, Any]:
    """
    Generate extractive summary from text.
    
    This function extracts important sentences from the input text to create
    a summary that preserves key information while staying within the length limit.
    
    Supports both Chinese and English text with automatic language detection.
    
    Args:
        text: Input text (supports Chinese and English)
        max_length: Maximum length of summary in characters (default: 200)
        language: Language code ('zh', 'en', or 'auto' for auto-detection)
    
    Returns:
        Dictionary containing:
            - 'summary': str - the generated summary
            - 'key_sentences': List[str] - list of key sentences extracted
            - 'original_length': int - length of original text
            - 'summary_length': int - length of generated summary
            - 'compression_ratio': float - compression ratio (0-1)
            - 'language': str - detected language
        
        Example:
        {
            'summary': '机器学习是AI的核心技术。',
            'key_sentences': ['机器学习是AI的核心技术。'],
            'original_length': 100,
            'summary_length': 12,
            'compression_ratio': 0.12,
            'language': 'zh'
        }
    
    Raises:
        ValueError: If text is empty
        ValueError: If max_length is not positive
    
    Example:
        >>> text = "机器学习是人工智能的核心技术。深度学习是机器学习的重要分支。"
        >>> result = generate_summary(text, max_length=50)
        >>> print(result['summary'])
        '机器学习是人工智能的核心技术。'
    
    Performance:
        - 1000 characters: <5s
        - 5000 characters: <10s
    """
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")
    
    if max_length <= 0:
        raise ValueError("max_length must be positive")
    
    # Detect language if auto
    if language == "auto":
        lang_info = detect_language(text)
        language = lang_info.code
    
    sentences = _split_sentences(text, language)
    
    if not sentences:
        return {
            'summary': '',
            'key_sentences': [],
            'original_length': len(text),
            'summary_length': 0,
            'compression_ratio': 0.0,
            'language': language
        }
    
    if len(text) <= max_length:
        return {
            'summary': text,
            'key_sentences': [text],
            'original_length': len(text),
            'summary_length': len(text),
            'compression_ratio': 1.0,
            'language': language
        }
    
    sentence_scores = _score_sentences(sentences, language)
    
    ranked_sentences = sorted(
        sentence_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    summary_sentences = []
    current_length = 0
    
    for sentence, score in ranked_sentences:
        sentence_length = len(sentence)
        
        if current_length + sentence_length <= max_length:
            summary_sentences.append((sentence, score))
            current_length += sentence_length
        
        if current_length >= max_length * 0.8:
            break
    
    # Sort by original order
    summary_sentences.sort(key=lambda x: text.index(x[0]))
    
    summary = ''.join([s[0] for s in summary_sentences])
    
    return {
        'summary': summary,
        'key_sentences': [s[0] for s in summary_sentences],
        'original_length': len(text),
        'summary_length': len(summary),
        'compression_ratio': round(len(summary) / len(text), 2),
        'language': language
    }


def _split_sentences(text: str, language: str) -> List[str]:
    """
    Split text into sentences.
    
    Supports both Chinese and English sentence delimiters.
    
    Args:
        text: Input text
        language: Language code
    
    Returns:
        List of sentences
    """
    if language == 'zh':
        # Chinese sentence endings
        sentence_endings = r'[。！？\.\!\?]+'
    else:
        # English sentence endings
        sentence_endings = r'[\.\!\?]+'
    
    sentences = re.split(sentence_endings, text)
    
    # Filter and clean sentences
    sentences = [
        s.strip()
        for s in sentences
        if s.strip() and len(s.strip()) > 3
    ]
    
    return sentences


def _score_sentences(
    sentences: List[str],
    language: str
) -> Dict[str, float]:
    """
    Score sentences by importance using TextRank-like algorithm.
    
    Args:
        sentences: List of sentences
        language: Language code
    
    Returns:
        Dictionary mapping sentences to importance scores
    """
    if len(sentences) <= 1:
        return {s: 1.0 for s in sentences}
    
    sentence_vectors = []
    for sentence in sentences:
        words = _tokenize_text(sentence, language)
        sentence_vectors.append(' '.join(words))
    
    try:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(sentence_vectors)
        
        similarity_matrix = cosine_similarity(tfidf_matrix)
        
        graph = nx.from_numpy_array(similarity_matrix)
        
        scores = nx.pagerank(graph)
        
        return {sentences[i]: scores[i] for i in range(len(sentences))}
        
    except Exception as e:
        logger.warning(f"Sentence scoring failed: {e}, using length-based scoring")
        
        max_len = max(len(s) for s in sentences)
        return {
            sentence: len(sentence) / max_len
            for sentence in sentences
        }


# ==================== Abstractive Summarization ====================

def generate_abstractive_summary(
    text: str,
    config: Optional[SummarizationConfig] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Generate abstractive summary using AI models.
    
    This function generates new text that summarizes the content,
    rather than extracting sentences. Supports both OpenAI API and
    local models.
    
    Args:
        text: Input text (supports Chinese and English)
        config: SummarizationConfig with settings
        **kwargs: Override config parameters
    
    Returns:
        Dictionary containing:
            - 'summary': str - the generated summary
            - 'method': str - 'abstractive' or 'extractive' (fallback)
            - 'model': str - model used
            - 'original_length': int - length of original text
            - 'summary_length': int - length of generated summary
            - 'compression_ratio': float - compression ratio
            - 'language': str - detected language
    
    Example:
        >>> text = "Machine learning is a subset of AI..."
        >>> config = SummarizationConfig(use_abstractive=True, model='openai')
        >>> result = generate_abstractive_summary(text, config=config)
        >>> print(result['summary'])
        'AI subset focusing on data-driven learning.'
    """
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")
    
    # Merge config with kwargs
    if config is None:
        config = SummarizationConfig(**kwargs)
    else:
        # Override with kwargs
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)
    
    # Detect language
    lang_info = detect_language(text)
    language = lang_info.code
    
    # Try abstractive summarization
    summary = None
    method = 'abstractive'
    model_used = config.model
    
    if config.use_abstractive:
        try:
            if config.model == 'openai':
                summary = _generate_abstractive_openai(text, config, language)
            else:
                summary = _generate_abstractive_local(text, config, language)
        except Exception as e:
            logger.warning(f"Abstractive summarization failed: {e}")
            if config.fallback_to_extractive:
                logger.info("Falling back to extractive summarization")
                method = 'extractive (fallback)'
                extractive_result = generate_summary(
                    text,
                    max_length=config.max_length,
                    language=language
                )
                summary = extractive_result['summary']
            else:
                raise
    else:
        # Use extractive
        method = 'extractive'
        extractive_result = generate_summary(
            text,
            max_length=config.max_length,
            language=language
        )
        summary = extractive_result['summary']
    
    return {
        'summary': summary,
        'method': method,
        'model': model_used if method == 'abstractive' else 'extractive',
        'original_length': len(text),
        'summary_length': len(summary),
        'compression_ratio': round(len(summary) / len(text), 2) if len(text) > 0 else 0.0,
        'language': language
    }


def _generate_abstractive_openai(
    text: str,
    config: SummarizationConfig,
    language: str
) -> str:
    """Generate abstractive summary using OpenAI API.
    
    Args:
        text: Input text
        config: Summarization config
        language: Detected language
        
    Returns:
        Generated summary
    """
    try:
        import openai
    except ImportError:
        raise ImportError("openai package not installed. Run: pip install openai")
    
    # Get API key
    api_key = config.api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OpenAI API key required. Set OPENAI_API_KEY environment variable "
            "or pass api_key in config."
        )
    
    # Set up client
    client = openai.OpenAI(api_key=api_key)
    
    # Build prompt based on language and style
    if language == 'zh':
        style_prompts = {
            'concise': '请用简洁的语言总结以下内容，保留关键信息：',
            'detailed': '请详细总结以下内容，包含主要观点和细节：',
            'bullet': '请用要点列表的形式总结以下内容：'
        }
        default_prompt = '请总结以下内容：'
    else:
        style_prompts = {
            'concise': 'Summarize the following content concisely, keeping key information:',
            'detailed': 'Summarize the following content in detail, including main points:',
            'bullet': 'Summarize the following content in bullet points:'
        }
        default_prompt = 'Summarize the following content:'
    
    prompt = style_prompts.get(config.style, default_prompt)
    
    # Truncate text if too long (OpenAI has token limits)
    max_input_chars = 12000  # Rough estimate for token limit
    if len(text) > max_input_chars:
        text = text[:max_input_chars] + "..."
    
    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": f"{prompt}\n\n{text}"}
        ],
        max_tokens=config.max_length * 2,  # Allow some flexibility
        temperature=0.3  # Lower temperature for more focused output
    )
    
    summary = response.choices[0].message.content.strip()
    
    # Truncate if needed
    if len(summary) > config.max_length * 1.5:
        summary = summary[:config.max_length] + "..."
    
    return summary


def _generate_abstractive_local(
    text: str,
    config: SummarizationConfig,
    language: str
) -> str:
    """Generate abstractive summary using local models.
    
    Currently uses a simple extraction-based approach as placeholder.
    In production, this would integrate with local LLMs like:
    - transformers (BART, T5, Pegasus)
    - sentence-transformers
    - Local LLaMA models
    
    Args:
        text: Input text
        config: Summarization config
        language: Detected language
        
    Returns:
        Generated summary
    """
    # Try to use transformers if available
    try:
        from transformers import pipeline
        
        # Use appropriate model for language
        if language == 'zh':
            model_name = "csebuetnlp/mT5_multilingual_XLSum"
        else:
            model_name = "facebook/bart-large-cnn"
        
        summarizer = pipeline("summarization", model=model_name)
        
        # Truncate text for model
        max_input = 1024
        if len(text) > max_input:
            text = text[:max_input]
        
        result = summarizer(
            text,
            max_length=config.max_length,
            min_length=30,
            do_sample=False
        )
        
        return result[0]['summary_text']
        
    except ImportError:
        logger.info("transformers not installed, falling back to extractive")
        # Fallback to extractive
        result = generate_summary(
            text,
            max_length=config.max_length,
            language=language
        )
        return result['summary']
    except Exception as e:
        logger.warning(f"Local model summarization failed: {e}")
        # Fallback to extractive
        result = generate_summary(
            text,
            max_length=config.max_length,
            language=language
        )
        return result['summary']


# ==================== Utility Functions ====================

def get_text_info(text: str) -> Dict[str, Any]:
    """Get comprehensive information about text.
    
    Args:
        text: Input text
        
    Returns:
        Dictionary with text statistics, language info, and keywords
    """
    if not text or not text.strip():
        return {
            'statistics': {},
            'language': 'unknown',
            'keywords': []
        }
    
    # Get statistics
    stats = get_text_statistics(text)
    
    # Get keywords
    try:
        keywords = extract_keywords(text, top_n=5)
    except Exception:
        keywords = []
    
    return {
        'statistics': stats,
        'language': stats.get('language', 'unknown'),
        'language_confidence': stats.get('language_confidence', 0.0),
        'keywords': keywords
    }
