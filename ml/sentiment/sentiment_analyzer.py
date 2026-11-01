"""
ml/sentiment/sentiment_analyzer.py
==================================
Sentiment analysis module for student feedback.

Uses VADER (Valence Aware Dictionary and sEntiment Reasoner), which is:
  - Rule-based, lightweight, fast, and does not require complex model training.
  - Highly effective on user-generated text containing punctuation, emoticons, and domain expressions.

Score ranges:
  - Strongly negative: -1.0
  - Neutral:            0.0
  - Strongly positive: +1.0

Classification Thresholds:
  - score >= 0.05  -> Positive
  - score <= -0.05 -> Negative
  - otherwise      -> Neutral
"""

from typing import Dict, Any

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    _VADER = SentimentIntensityAnalyzer()
except ImportError:
    _VADER = None


DOMAIN_LEXICON = {
    # Negative feedback indicators in academic/lab environments
    "slow": -1.8,
    "sluggish": -2.2,
    "broken": -2.5,
    "crash": -2.5,
    "crashing": -2.5,
    "crashed": -2.5,
    "unclear": -2.0,
    "confusing": -2.0,
    "confused": -1.8,
    "rushed": -1.8,
    "rush": -1.5,
    "incomplete": -2.0,
    "unusable": -3.0,
    "uncomfortable": -2.2,
    "sparking": -3.0,
    "hazardous": -3.5,
    "outdated": -1.8,
    "dirty": -2.2,
    "laggy": -2.0,
    "disturbed": -1.8,
    "struggle": -1.8,
    "struggling": -1.8,
    "pending": -1.2,
    # Positive feedback indicators
    "well-structured": 2.5,
    "informative": 2.2,
    "engaging": 2.5,
    "interactive": 2.0,
    "satisfactory": 1.5,
    "helpful": 2.2,
    "thoroughly": 1.8,
}


class SentimentAnalyzer:
    def __init__(self):
        if _VADER is not None:
            self.analyzer = _VADER
        else:
            self.analyzer = None

        # Update lexicon with domain terms when VADER is installed.
        if self.analyzer is not None:
            self.analyzer.lexicon.update(DOMAIN_LEXICON)

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyze the sentiment of a feedback string.

        Parameters:
          text (str): Raw or preprocessed feedback text.

        Returns:
          dict:
            {
              "sentiment_score": float (-1.0 to 1.0),
              "sentiment_label": "Positive" | "Neutral" | "Negative",
              "details": { "pos": float, "neu": float, "neg": float, "compound": float }
            }
        """
        if not text or not isinstance(text, str) or not text.strip():
            return {
                "sentiment_score": 0.0,
                "sentiment_label": "Neutral",
                "details": {"pos": 0.0, "neu": 1.0, "neg": 0.0, "compound": 0.0},
            }

        if self.analyzer is not None:
            scores = self.analyzer.polarity_scores(text)
            compound = round(scores["compound"], 4)
        else:
            # Deterministic fallback for environments without vaderSentiment.
            # This is intentionally lightweight; install requirements.txt for VADER.
            words = text.lower().replace("!", " ! ").replace("?", " ? ").split()
            positive = {"good", "great", "excellent", "helpful", "clear", "clean", "improved", "love", "best", "informative", "engaging", "satisfactory", "wonderful"}
            negative = {"bad", "poor", "slow", "broken", "crash", "crashing", "unclear", "confusing", "confused", "rushed", "incomplete", "unusable", "dirty", "outdated", "urgent", "unsafe", "issue", "problem", "stopped", "terrible", "dangerous", "failed", "failure", "sparking"}
            normalized = [w.strip(".,:;()") for w in words]
            pos = sum(1 for w in normalized if w in positive)
            neg = sum(1 for w in normalized if w in negative)
            # Negated operation phrases are negative even if they contain no
            # intrinsically negative adjective (e.g. "not working").
            lowered = text.lower()
            if any(phrase in lowered for phrase in ("not working", "not functioning", "stopped working", "not operational", "not available")):
                neg += 1
            compound = round(max(-1.0, min(1.0, (pos - neg) / max(1, pos + neg))), 4)
            scores = {"pos": float(pos), "neu": float(max(0, len(words)-pos-neg)), "neg": float(neg), "compound": compound}

        if compound >= 0.05:
            label = "Positive"
        elif compound <= -0.05:
            label = "Negative"
        else:
            label = "Neutral"

        return {
            "sentiment_score": compound,
            "sentiment_label": label,
            "details": scores,
        }


# Singleton instance for quick imports
_default_analyzer = SentimentAnalyzer()


def analyze_sentiment(text: str) -> Dict[str, Any]:
    """
    Convenience function to analyze sentiment using the default VADER analyzer.
    """
    return _default_analyzer.analyze(text)
