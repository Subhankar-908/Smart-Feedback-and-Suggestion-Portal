"""
ml/preprocessing/text_cleaner.py
================================
Text preprocessing module for student feedback.

Responsibilities:
  1. Convert text to lowercase.
  2. Remove URLs, emails, and excessive punctuation/special characters.
  3. Tokenize text into words.
  4. Remove common stopwords (while preserving sentiment-negating words like 'not', 'no').
  5. Lemmatize tokens to base dictionary forms.

Designed to be beginner-friendly, robust, and easy to explain during viva.
"""

import re
import string
from typing import List, Dict, Any

# Attempt NLTK imports with robust fallback
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer

    # Never download corpora at application startup: production servers may
    # be offline. Use locally installed corpora when present and fallbacks otherwise.
    _LEMMATIZER = WordNetLemmatizer()
    try:
        _NLTK_STOPWORDS = set(stopwords.words("english"))
    except Exception:
        _NLTK_STOPWORDS = set()
except Exception:
    _LEMMATIZER = None
    _NLTK_STOPWORDS = set()

# Essential stopwords fallback list
_FALLBACK_STOPWORDS = {
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your",
    "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she",
    "her", "hers", "herself", "it", "its", "itself", "they", "them", "their",
    "theirs", "themselves", "what", "which", "who", "whom", "this", "that",
    "these", "those", "am", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an",
    "the", "and", "but", "if", "or", "because", "as", "until", "while", "of",
    "at", "by", "for", "with", "about", "against", "between", "into", "through",
    "during", "before", "after", "above", "below", "to", "from", "up", "down",
    "in", "out", "on", "off", "over", "under", "again", "further", "then", "once",
    "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
    "few", "more", "most", "other", "some", "such", "only", "own", "same", "so",
    "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"
}

# Negation words to keep for sentiment analysis context
_NEGATION_WORDS = {"not", "no", "nor", "never", "neither", "hardly", "barely", "scarcely"}

STOPWORDS = (_NLTK_STOPWORDS or _FALLBACK_STOPWORDS) - _NEGATION_WORDS


def clean_text(text: str) -> str:
    """
    Clean raw input string:
    - Lowercase text
    - Remove URLs and email addresses
    - Remove extra whitespaces
    - Strip punctuation
    """
    if not text or not isinstance(text, str):
        return ""

    text = text.lower()
    # Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    # Remove emails
    text = re.sub(r"\S+@\S+", " ", text)
    # Remove numbers & special characters, keep letters and basic spaces
    text = re.sub(r"[^a-z\s]", " ", text)
    # Remove multiple spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text: str) -> List[str]:
    """
    Split cleaned text into a list of word tokens.
    """
    cleaned = clean_text(text)
    if not cleaned:
        return []
    return cleaned.split()


def remove_stopwords(tokens: List[str]) -> List[str]:
    """
    Filter out common English stop words while keeping meaningful content and negations.
    """
    return [token for token in tokens if token not in STOPWORDS and len(token) > 1]


def lemmatize_tokens(tokens: List[str]) -> List[str]:
    """
    Convert tokens to their dictionary root form (e.g. 'computers' -> 'computer').
    """
    if not _LEMMATIZER:
        return tokens
    lemmatized = []
    for token in tokens:
        try:
            lemmatized.append(_LEMMATIZER.lemmatize(token))
        except Exception:
            lemmatized.append(token)
    return lemmatized


def preprocess(text: str) -> Dict[str, Any]:
    """
    Full preprocessing pipeline.
    
    Returns:
      {
        "raw_text": str,
        "cleaned_text": str,
        "tokens": List[str],
        "filtered_tokens": List[str],
        "lemmatized_tokens": List[str]
      }
    """
    cleaned = clean_text(text)
    tokens = tokenize(text)
    filtered = remove_stopwords(tokens)
    lemmatized = lemmatize_tokens(filtered)

    return {
        "raw_text": text,
        "cleaned_text": cleaned,
        "tokens": tokens,
        "filtered_tokens": filtered,
        "lemmatized_tokens": lemmatized,
    }
