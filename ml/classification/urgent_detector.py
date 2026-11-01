"""
ml/classification/urgent_detector.py
====================================
Urgent Issue Detection module for student feedback.

Identifies severe, critical, or prolonged negative issues that require immediate
administrative intervention (e.g. hazardous conditions, lab equipment down for weeks,
broken fans/lights causing extreme distress).

Logic:
  1. Primary condition: Negative sentiment score (<= -0.3).
  2. Urgent keyword/phrase detection: Matches indicators of severity, prolonged disruption,
     or safety risks.
  3. Returns a boolean `urgent: True/False` along with matched reasons/triggers.
"""

import re
from typing import Dict, Any, List

# High urgency and prolonged issue keywords
URGENT_KEYWORDS = [
    "urgent", "urgently", "emergency", "immediate", "immediately", "critical",
    "severe", "hazardous", "danger", "dangerous", "accident", "shock", "spark",
    "fire", "smoke", "broken", "leak", "leaking", "damage", "damaged", "injury",
    "injured", "threat", "worst", "unusable", "unbearable", "impossible"
]

# High urgency multi-word patterns
URGENT_PATTERNS = [
    r"stop(ped)?\s+working",
    r"not\s+working\s+(for|since)",
    r"for\s+(the\s+)?last\s+(two|three|several|\d+)\s+weeks?",
    r"for\s+(the\s+)?last\s+(two|three|several|\d+)\s+months?",
    r"for\s+(two|three|\d+)\s+weeks",
    r"for\s+(two|three|\d+)\s+months",
    r"all\s+(the\s+)?computers?\s+(are\s+)?(down|broken|not\s+working)",
    r"all\s+systems?\s+(are\s+)?(down|broken|crashed)",
    r"electric(al)?\s+shock",
    r"heavy\s+leakage",
    r"extreme(ly)?\s+hot",
    r"cannot\s+conduct\s+practicals?",
    r"affecting\s+our\s+practicals?",
    r"please\s+(fix|resolve|replace)\s+(urgently|immediately)"
]


class UrgentDetector:
    def __init__(self, sentiment_threshold: float = -0.25):
        self.sentiment_threshold = sentiment_threshold
        self.urgent_keywords = set(URGENT_KEYWORDS)
        self.urgent_patterns = [re.compile(p, re.IGNORECASE) for p in URGENT_PATTERNS]

    def detect(self, text: str, sentiment_score: float) -> Dict[str, Any]:
        """
        Evaluate whether the given feedback is an urgent issue.

        Parameters:
          text (str): Feedback content.
          sentiment_score (float): Sentiment compound score (-1.0 to 1.0).

        Returns:
          dict:
            {
              "urgent": bool,
              "reasons": List[str]
            }
        """
        if not text or not isinstance(text, str):
            return {"urgent": False, "reasons": []}

        text_lower = text.lower()
        matched_reasons = []

        # 1. Pattern matching (prolonged downtime, severe failures)
        for pattern in self.urgent_patterns:
            match = pattern.search(text_lower)
            if match:
                matched_reasons.append(f"Pattern matched: '{match.group(0)}'")

        # 2. Keyword matching
        words = set(re.findall(r"\b[a-z]+\b", text_lower))
        found_keywords = words.intersection(self.urgent_keywords)
        if found_keywords:
            matched_reasons.append(f"Urgent keywords: {', '.join(sorted(found_keywords))}")

        # Urgency criteria:
        # - If severe patterns or safety keywords found AND sentiment is not positive
        # - OR sentiment is clearly negative (score <= threshold) AND urgent triggers exist
        # - OR extremely negative sentiment (score <= -0.75) with broken/failure context
        is_urgent = False

        if matched_reasons and sentiment_score <= 0.1:
            is_urgent = True
        elif sentiment_score <= -0.75 and ("broken" in text_lower or "not working" in text_lower):
            is_urgent = True
            matched_reasons.append("Severe negative sentiment with equipment failure")

        return {
            "urgent": is_urgent,
            "reasons": matched_reasons
        }


# Singleton instance
_default_detector = UrgentDetector()


def detect_urgency(text: str, sentiment_score: float) -> bool:
    """Convenience function returning True if issue is urgent."""
    result = _default_detector.detect(text, sentiment_score)
    return result["urgent"]
