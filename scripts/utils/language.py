"""
Language detection and text processing utilities.

Provides language detection, stop word management, and text processing
for multiple languages (primarily Chinese and English).

Implements TASK-C5: Multi-language Support
"""

import re
import logging
from typing import List, Dict, Set, Optional, Tuple, Any
from dataclasses import dataclass
from functools import lru_cache
import unicodedata

logger = logging.getLogger(__name__)


@dataclass
class LanguageInfo:
    """Information about detected language.
    
    Attributes:
        code: ISO 639-1 language code (e.g., 'zh', 'en')
        name: Full language name
        confidence: Detection confidence (0.0 to 1.0)
        is_mixed: Whether text contains multiple languages
    """
    
    code: str
    name: str
    confidence: float
    is_mixed: bool = False


# Chinese character ranges
CHINESE_RANGES = [
    (0x4E00, 0x9FFF),    # CJK Unified Ideographs
    (0x3400, 0x4DBF),    # CJK Unified Ideographs Extension A
    (0x20000, 0x2A6DF),  # CJK Unified Ideographs Extension B
    (0x2A700, 0x2B73F),  # CJK Unified Ideographs Extension C
    (0x2B740, 0x2B81F),  # CJK Unified Ideographs Extension D
    (0x2B820, 0x2CEAF),  # CJK Unified Ideographs Extension E
]

# English letter ranges
ENGLISH_RANGES = [
    (0x0041, 0x005A),    # Uppercase A-Z
    (0x0061, 0x007A),    # Lowercase a-z
]


# Chinese stop words
CHINESE_STOP_WORDS: Set[str] = {
    '的', '了', '在', '是', '我', '有', '和', '就', '不', '人',
    '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去',
    '你', '会', '着', '没有', '看', '好', '自己', '这', '那', '他',
    '她', '它', '们', '这个', '那个', '什么', '怎么', '为什么',
    '哪', '哪里', '谁', '多少', '几', '很', '非常', '太', '更',
    '最', '能', '可以', '应该', '必须', '需要', '得', '把', '被',
    '让', '给', '向', '从', '对', '与', '或', '但', '而', '且',
    '如果', '虽然', '因为', '所以', '但是', '然后', '接着', '于是',
    '只要', '只有', '无论', '不管', '即使', '哪怕', '尽管', '然而',
    '这样', '那样', '怎样', '如何', '为何', '为了', '由于', '以致',
    '及', '等', '等等', '之', '所', '以', '其', '此', '彼',
}

# English stop words (common NLTK-style)
ENGLISH_STOP_WORDS: Set[str] = {
    'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
    'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are',
    'were', 'been', 'be', 'have', 'has', 'had', 'do', 'does', 'did',
    'will', 'would', 'could', 'should', 'may', 'might', 'must',
    'shall', 'can', 'need', 'dare', 'ought', 'used', 'it', 'its',
    'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'we',
    'they', 'what', 'which', 'who', 'whom', 'whose', 'where', 'when',
    'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more',
    'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
    'own', 'same', 'so', 'than', 'too', 'very', 'just', 'also',
    'now', 'here', 'there', 'then', 'once', 'if', 'because', 'until',
    'while', 'about', 'against', 'between', 'into', 'through',
    'during', 'before', 'after', 'above', 'below', 'up', 'down',
    'out', 'off', 'over', 'under', 'again', 'further', 'any',
    'am', 'being', 'get', 'got', 'getting', 'going', 'go', 'goes',
    'make', 'made', 'making', 'take', 'took', 'taking', 'come',
    'came', 'coming', 'see', 'saw', 'seeing', 'know', 'knew',
    'knowing', 'think', 'thought', 'thinking', 'want', 'wanted',
    'wanting', 'give', 'gave', 'giving', 'use', 'used', 'using',
    'find', 'found', 'finding', 'tell', 'told', 'telling', 'ask',
    'asked', 'asking', 'work', 'working', 'seem', 'seemed', 'seeming',
    'feel', 'felt', 'feeling', 'try', 'tried', 'trying', 'leave',
    'left', 'leaving', 'call', 'called', 'calling',
}


def is_chinese_char(char: str) -> bool:
    """Check if a character is Chinese.
    
    Args:
        char: Single character
        
    Returns:
        True if character is Chinese
    """
    if not char:
        return False
    
    code = ord(char)
    for start, end in CHINESE_RANGES:
        if start <= code <= end:
            return True
    return False


def is_english_char(char: str) -> bool:
    """Check if a character is English letter.
    
    Args:
        char: Single character
        
    Returns:
        True if character is English letter
    """
    if not char:
        return False
    
    code = ord(char)
    for start, end in ENGLISH_RANGES:
        if start <= code <= end:
            return True
    return False


def count_chinese_chars(text: str) -> int:
    """Count Chinese characters in text.
    
    Args:
        text: Input text
        
    Returns:
        Number of Chinese characters
    """
    return sum(1 for char in text if is_chinese_char(char))


def count_english_chars(text: str) -> int:
    """Count English letters in text.
    
    Args:
        text: Input text
        
    Returns:
        Number of English letters
    """
    return sum(1 for char in text if is_english_char(char))


def detect_language(text: str) -> LanguageInfo:
    """Detect the primary language of text.
    
    Analyzes character distribution to determine if text is primarily
    Chinese, English, or mixed.
    
    Args:
        text: Input text
        
    Returns:
        LanguageInfo with detected language details
        
    Example:
        >>> info = detect_language("这是中文文本")
        >>> info.code
        'zh'
        >>> info = detect_language("This is English text")
        >>> info.code
        'en'
    """
    if not text or not text.strip():
        return LanguageInfo(
            code='unknown',
            name='Unknown',
            confidence=0.0
        )
    
    # Count characters
    chinese_count = count_chinese_chars(text)
    english_count = count_english_chars(text)
    total_alpha = chinese_count + english_count
    
    if total_alpha == 0:
        return LanguageInfo(
            code='unknown',
            name='Unknown',
            confidence=0.0
        )
    
    chinese_ratio = chinese_count / total_alpha
    english_ratio = english_count / total_alpha
    
    # Determine primary language
    is_mixed = 0.2 < chinese_ratio < 0.8
    
    if chinese_ratio > 0.5:
        confidence = chinese_ratio
        code = 'zh'
        name = 'Chinese'
    elif english_ratio > 0.5:
        confidence = english_ratio
        code = 'en'
        name = 'English'
    else:
        # Default to Chinese if roughly equal
        confidence = 0.5
        code = 'zh'
        name = 'Chinese'
    
    return LanguageInfo(
        code=code,
        name=name,
        confidence=confidence,
        is_mixed=is_mixed
    )


def get_stop_words(language: str = 'zh') -> Set[str]:
    """Get stop words for a language.
    
    Args:
        language: Language code ('zh' for Chinese, 'en' for English)
        
    Returns:
        Set of stop words
    """
    if language == 'zh':
        return CHINESE_STOP_WORDS.copy()
    elif language == 'en':
        return ENGLISH_STOP_WORDS.copy()
    else:
        return set()


def is_stop_word(word: str, language: str = 'auto') -> bool:
    """Check if a word is a stop word.
    
    Args:
        word: Word to check
        language: Language code ('zh', 'en', or 'auto' for auto-detection)
        
    Returns:
        True if word is a stop word
    """
    if not word or not word.strip():
        return False
    
    word = word.lower().strip()
    
    if language == 'auto':
        # Auto-detect based on word
        if any(is_chinese_char(c) for c in word):
            language = 'zh'
        else:
            language = 'en'
    
    stop_words = get_stop_words(language)
    return word in stop_words


def tokenize(text: str, language: str = 'auto') -> List[str]:
    """Tokenize text into words.
    
    For Chinese, uses character-based segmentation as fallback.
    For English, splits on whitespace and punctuation.
    
    Args:
        text: Input text
        language: Language code ('zh', 'en', or 'auto')
        
    Returns:
        List of tokens
    """
    if not text or not text.strip():
        return []
    
    if language == 'auto':
        lang_info = detect_language(text)
        language = lang_info.code
    
    if language == 'zh':
        # Chinese - try jieba first, fallback to character segmentation
        try:
            import jieba
            return list(jieba.cut(text))
        except ImportError:
            # Fallback: split by punctuation and return character sequences
            # This is a simple fallback, not ideal for production
            tokens = []
            current_token = ""
            for char in text:
                if is_chinese_char(char):
                    if current_token:
                        tokens.append(current_token)
                        current_token = ""
                    tokens.append(char)
                elif char.isalpha():
                    current_token += char
                else:
                    if current_token:
                        tokens.append(current_token)
                        current_token = ""
            if current_token:
                tokens.append(current_token)
            return tokens
    else:
        # English - split on non-alphanumeric
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens


def normalize_text(text: str, language: str = 'auto') -> str:
    """Normalize text for processing.
    
    Performs:
    - Unicode normalization
    - Whitespace normalization
    - Lowercase for English
    - Remove extra punctuation
    
    Args:
        text: Input text
        language: Language code
        
    Returns:
        Normalized text
    """
    if not text:
        return ""
    
    # Unicode normalization
    text = unicodedata.normalize('NFKC', text)
    
    # Normalize whitespace
    text = ' '.join(text.split())
    
    if language == 'auto':
        lang_info = detect_language(text)
        language = lang_info.code
    
    if language == 'en':
        # Lowercase for English
        text = text.lower()
    
    return text


def remove_stop_words(
    words: List[str],
    language: str = 'auto'
) -> List[str]:
    """Remove stop words from a list of words.
    
    Args:
        words: List of words
        language: Language code
        
    Returns:
        List of words with stop words removed
    """
    if language == 'auto':
        # Detect from words
        for word in words:
            if any(is_chinese_char(c) for c in word):
                language = 'zh'
                break
        else:
            language = 'en'
    
    stop_words = get_stop_words(language)
    
    return [
        word for word in words
        if word.lower().strip() not in stop_words
    ]


def get_text_statistics(text: str) -> Dict[str, Any]:
    """Get statistics about text.
    
    Args:
        text: Input text
        
    Returns:
        Dictionary with statistics:
            - total_chars: Total character count
            - chinese_chars: Chinese character count
            - english_chars: English letter count
            - word_count: Estimated word count
            - language: Detected language
            - language_confidence: Detection confidence
    """
    if not text:
        return {
            'total_chars': 0,
            'chinese_chars': 0,
            'english_chars': 0,
            'word_count': 0,
            'language': 'unknown',
            'language_confidence': 0.0
        }
    
    chinese_count = count_chinese_chars(text)
    english_count = count_english_chars(text)
    
    lang_info = detect_language(text)
    
    # Estimate word count
    if lang_info.code == 'zh':
        # For Chinese, each character can be considered a word unit
        word_count = chinese_count + len(re.findall(r'\b\w+\b', text))
    else:
        # For English, split on whitespace
        word_count = len(text.split())
    
    return {
        'total_chars': len(text),
        'chinese_chars': chinese_count,
        'english_chars': english_count,
        'word_count': word_count,
        'language': lang_info.code,
        'language_name': lang_info.name,
        'language_confidence': lang_info.confidence,
        'is_mixed': lang_info.is_mixed
    }


class LanguageProcessor:
    """Processor for multi-language text operations.
    
    Provides a unified interface for language detection,
    tokenization, and text processing.
    
    Example:
        >>> processor = LanguageProcessor()
        >>> text = "这是一段中文文本"
        >>> tokens = processor.tokenize(text)
        >>> clean_tokens = processor.remove_stop_words(tokens)
    """
    
    def __init__(self, default_language: str = 'auto'):
        """Initialize the processor.
        
        Args:
            default_language: Default language code
        """
        self.default_language = default_language
        self._stop_words_cache: Dict[str, Set[str]] = {}
    
    def detect(self, text: str) -> LanguageInfo:
        """Detect language of text."""
        return detect_language(text)
    
    def tokenize(
        self,
        text: str,
        language: str = None,
        remove_stops: bool = False
    ) -> List[str]:
        """Tokenize text.
        
        Args:
            text: Input text
            language: Language code (uses default if None)
            remove_stops: Whether to remove stop words
            
        Returns:
            List of tokens
        """
        language = language or self.default_language
        tokens = tokenize(text, language)
        
        if remove_stops:
            tokens = remove_stop_words(tokens, language)
        
        return tokens
    
    def get_stop_words(self, language: str = None) -> Set[str]:
        """Get stop words with caching."""
        language = language or self.default_language
        
        if language == 'auto':
            language = 'zh'  # Default
        
        if language not in self._stop_words_cache:
            self._stop_words_cache[language] = get_stop_words(language)
        
        return self._stop_words_cache[language]
    
    def normalize(
        self,
        text: str,
        language: str = None
    ) -> str:
        """Normalize text."""
        language = language or self.default_language
        return normalize_text(text, language)
    
    def get_statistics(self, text: str) -> Dict[str, Any]:
        """Get text statistics."""
        return get_text_statistics(text)
    
    def is_stop_word(self, word: str, language: str = None) -> bool:
        """Check if word is stop word."""
        language = language or self.default_language
        return is_stop_word(word, language)


# Global processor instance
language_processor = LanguageProcessor()
