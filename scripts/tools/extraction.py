"""
Knowledge extraction tools for keyword extraction and text summarization.

Implements TASK-C1: extract_keywords and generate_summary functions.
"""

import re
import logging
from typing import List, Dict, Any, Tuple
from collections import Counter

import jieba
import jieba.analyse
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)


def extract_keywords(
    text: str,
    method: str = "tfidf",
    top_n: int = 10
) -> List[Dict[str, Any]]:
    """
    Extract keywords from text using TF-IDF or TextRank method.
    
    Args:
        text: Input text (supports Chinese)
        method: Extraction method - "tfidf" or "textrank" (default: "tfidf")
        top_n: Number of keywords to extract (default: 10)
    
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
    
    if method == "tfidf":
        return _extract_keywords_tfidf(text, top_n)
    else:
        return _extract_keywords_textrank(text, top_n)


def _is_stop_word(word: str) -> bool:
    """
    Check if a word is a stop word.
    
    Args:
        word: Word to check
    
    Returns:
        True if word is a stop word, False otherwise
    """
    stop_words = {
        '的', '了', '在', '是', '我', '有', '和', '就', '不', '人',
        '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去',
        '你', '会', '着', '没有', '看', '好', '自己', '这', '那',
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
        'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are',
        'were', 'been', 'be', 'have', 'has', 'had', 'do', 'does', 'did',
        'will', 'would', 'could', 'should', 'may', 'might', 'must'
    }
    
    return word.lower() in stop_words


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
    has_chinese = any('\u4e00' <= c <= '\u9fff' for c in word)
    
    return has_letter or has_chinese


def _extract_keywords_tfidf(text: str, top_n: int) -> List[Dict[str, Any]]:
    """
    Extract keywords using TF-IDF method.
    
    Args:
        text: Input text
        top_n: Number of keywords to extract
    
    Returns:
        List of keyword dictionaries with 'keyword' and 'score'
    """
    words = jieba.lcut(text)
    
    filtered_words = [
        word.lower().strip()
        for word in words
        if len(word.strip()) > 1 and not word.isspace() and not _is_stop_word(word) and _is_valid_word(word)
    ]
    
    if not filtered_words:
        return []
    
    word_freq = Counter(filtered_words)
    total_words = len(filtered_words)
    
    processed_text = ' '.join(filtered_words)
    
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


def _extract_keywords_textrank(text: str, top_n: int) -> List[Dict[str, Any]]:
    """
    Extract keywords using TextRank algorithm.
    
    Args:
        text: Input text
        top_n: Number of keywords to extract
    
    Returns:
        List of keyword dictionaries with 'keyword' and 'score'
    """
    words = jieba.lcut(text)
    
    filtered_words = [
        word.lower().strip()
        for word in words
        if len(word.strip()) > 1 and not word.isspace() and not _is_stop_word(word)
    ]
    
    if not filtered_words:
        return []
    
    window_size = 4
    graph = nx.Graph()
    
    for i in range(len(filtered_words) - window_size + 1):
        window_words = filtered_words[i:i + window_size]
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
        
        word_freq = Counter(filtered_words)
        total_words = len(filtered_words)
        
        keywords = []
        for word, count in word_freq.most_common(top_n):
            normalized_score = min(count / total_words * 2, 1.0)
            keywords.append({
                'keyword': word,
                'score': round(normalized_score, 4)
            })
        
        return keywords


def generate_summary(
    text: str,
    max_length: int = 200
) -> Dict[str, Any]:
    """
    Generate extractive summary from text.
    
    This function extracts important sentences from the input text to create
    a summary that preserves key information while staying within the length limit.
    
    Args:
        text: Input text (supports Chinese)
        max_length: Maximum length of summary in characters (default: 200)
    
    Returns:
        Dictionary containing:
            - 'summary': str - the generated summary
            - 'key_sentences': List[str] - list of key sentences extracted
            - 'original_length': int - length of original text
            - 'summary_length': int - length of generated summary
            - 'compression_ratio': float - compression ratio (0-1)
        
        Example:
        {
            'summary': '机器学习是AI的核心技术。',
            'key_sentences': ['机器学习是AI的核心技术。'],
            'original_length': 100,
            'summary_length': 12,
            'compression_ratio': 0.12
        }
    
    Raises:
        ValueError: If text is empty
        ValueError: If max_length is not positive
    
    Example:
        >>> text = "机器学习是人工智能的核心技术。深度学习是机器学习的重要分支。自然语言处理是AI的重要应用领域。"
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
    
    sentences = _split_sentences(text)
    
    if not sentences:
        return {
            'summary': '',
            'key_sentences': [],
            'original_length': len(text),
            'summary_length': 0,
            'compression_ratio': 0.0
        }
    
    if len(text) <= max_length:
        return {
            'summary': text,
            'key_sentences': [text],
            'original_length': len(text),
            'summary_length': len(text),
            'compression_ratio': 1.0
        }
    
    sentence_scores = _score_sentences(sentences)
    
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
    
    summary_sentences.sort(key=lambda x: text.index(x[0]))
    
    summary = ''.join([s[0] for s in summary_sentences])
    
    return {
        'summary': summary,
        'key_sentences': [s[0] for s in summary_sentences],
        'original_length': len(text),
        'summary_length': len(summary),
        'compression_ratio': round(len(summary) / len(text), 2)
    }


def _split_sentences(text: str) -> List[str]:
    """
    Split text into sentences.
    
    Supports both Chinese and English sentence delimiters.
    
    Args:
        text: Input text
    
    Returns:
        List of sentences
    """
    sentence_endings = r'[。！？\.\!\?]+'
    sentences = re.split(sentence_endings, text)
    
    sentences = [
        s.strip()
        for s in sentences
        if s.strip() and len(s.strip()) > 3
    ]
    
    return sentences


def _score_sentences(sentences: List[str]) -> Dict[str, float]:
    """
    Score sentences by importance using TextRank-like algorithm.
    
    Args:
        sentences: List of sentences
    
    Returns:
        Dictionary mapping sentences to importance scores
    """
    if len(sentences) <= 1:
        return {s: 1.0 for s in sentences}
    
    sentence_vectors = []
    for sentence in sentences:
        words = jieba.lcut(sentence)
        filtered_words = [
            word.lower()
            for word in words
            if len(word) > 1 and not _is_stop_word(word)
        ]
        sentence_vectors.append(' '.join(filtered_words))
    
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
