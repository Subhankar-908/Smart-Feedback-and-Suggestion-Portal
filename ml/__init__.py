"""
ml package
==========
Contains all Natural Language Processing (NLP) modules:
  - preprocessing: text cleaning, tokenization, lemmatization
  - sentiment: VADER sentiment analysis
  - classification: operational category classification and urgency detection
  - pipeline: unified analyze_feedback function
"""

from ml.pipeline import analyze_feedback
from ml.preprocessing.text_cleaner import clean_text, preprocess
from ml.sentiment.sentiment_analyzer import analyze_sentiment
from ml.classification.category_classifier import classify_category
from ml.classification.urgent_detector import detect_urgency

__all__ = [
    "analyze_feedback",
    "clean_text",
    "preprocess",
    "analyze_sentiment",
    "classify_category",
    "detect_urgency",
]
