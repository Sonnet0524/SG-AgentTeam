"""
Utility modules for knowledge assistant.

Provides language processing, text manipulation, and other utilities.
"""

from .language import (
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

__all__ = [
    'detect_language',
    'get_stop_words',
    'is_stop_word',
    'tokenize',
    'normalize_text',
    'remove_stop_words',
    'get_text_statistics',
    'LanguageInfo',
    'LanguageProcessor',
    'language_processor',
    'is_chinese_char',
    'is_english_char',
    'count_chinese_chars',
    'count_english_chars',
    'CHINESE_STOP_WORDS',
    'ENGLISH_STOP_WORDS',
]
