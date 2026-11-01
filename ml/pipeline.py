"""
ml/pipeline.py
==============
Unified NLP Pipeline Interface for the Smart Feedback Portal.

Pipeline workflow:
  Raw Feedback Text
         ↓
  1. Text Preprocessing (clean, tokenize, lemmatize)
         ↓
  2. Sentiment Analysis (VADER compound score & label)
         ↓
  3. Category Classification (operational category matching)
         ↓
  4. Urgent Issue Detection (negative severity + urgency triggers)
         ↓
  Unified Result Dictionary returned to FastAPI backend
"""

from typing import Dict, Any
from ml.preprocessing.text_cleaner import clean_text, preprocess
from ml.sentiment.sentiment_analyzer import analyze_sentiment
from ml.classification.category_classifier import classify_category
from ml.classification.urgent_detector import detect_urgency


def analyze_feedback(feedback_text: str) -> Dict[str, Any]:
    """
    Execute full NLP pipeline on student feedback text.

    Parameters:
      feedback_text (str): Raw feedback string submitted by student.

    Returns:
      dict:
        {
          "sentiment_score": float,              # -1.0 to 1.0
          "sentiment_label": str,                # 'Positive' | 'Neutral' | 'Negative'
          "category": str,                       # 'Teaching Pace', 'Lab Facilities', etc.
          "urgent": bool,                        # True / False
          "cleaned_text": str,                   # Cleaned lowercase string
          "lemmatized_tokens": list[str]         # Normalized token list
        }
    """
    if not feedback_text or not isinstance(feedback_text, str) or not feedback_text.strip():
        return {
            "sentiment_score": 0.0,
            "sentiment_label": "Neutral",
            "category": "Other",
            "urgent": False,
            "cleaned_text": "",
            "lemmatized_tokens": []
        }

    # Step 1: Preprocessing
    prep = preprocess(feedback_text)
    cleaned = prep["cleaned_text"]

    # Step 2: Sentiment Analysis
    sent_res = analyze_sentiment(feedback_text)
    score = sent_res["sentiment_score"]
    label = sent_res["sentiment_label"]

    # Step 3: Category Classification
    category = classify_category(feedback_text)

    # Step 4: Urgent Issue Detection
    is_urgent = detect_urgency(feedback_text, score)

    return {
        "sentiment_score": score,
        "sentiment_label": label,
        "category": category,
        "urgent": is_urgent,
        "cleaned_text": cleaned,
        "lemmatized_tokens": prep["lemmatized_tokens"]
    }
