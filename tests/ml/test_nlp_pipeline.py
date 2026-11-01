"""
tests/ml/test_nlp_pipeline.py
==============================
Unit tests for the NLP Pipeline modules:
- Preprocessing (text_cleaner)
- Sentiment Analysis (sentiment_analyzer)
- Category Classification (category_classifier)
- Urgent Issue Detection (urgent_detector)
- Full Pipeline (pipeline.analyze_feedback)
"""

import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from ml.preprocessing.text_cleaner import clean_text, tokenize, remove_stopwords, lemmatize_tokens, preprocess
from ml.sentiment.sentiment_analyzer import analyze_sentiment
from ml.classification.category_classifier import classify_category
from ml.classification.urgent_detector import detect_urgency
from ml.pipeline import analyze_feedback


def test_text_cleaning():
    raw = "The LAB COMPUTERS (Room #102) are NOT working!!! https://college.edu"
    cleaned = clean_text(raw)
    assert "https" not in cleaned
    assert "#" not in cleaned
    assert cleaned == "the lab computers room are not working"


def test_preprocessing():
    text = "Students are having trouble understanding fast lectures."
    res = preprocess(text)
    assert len(res["tokens"]) > 0
    assert "trouble" in res["lemmatized_tokens"] or "understand" in res["lemmatized_tokens"] or "lecture" in res["lemmatized_tokens"]


def test_sentiment_analysis():
    pos_res = analyze_sentiment("The lectures are very clear and the professor is wonderful!")
    assert pos_res["sentiment_label"] == "Positive"
    assert pos_res["sentiment_score"] > 0.05

    neg_res = analyze_sentiment("The lab machines are broken and terrible.")
    assert neg_res["sentiment_label"] == "Negative"
    assert neg_res["sentiment_score"] < -0.05

    neu_res = analyze_sentiment("The syllabus was handed out today.")
    assert neu_res["sentiment_label"] == "Neutral"


def test_category_classification():
    assert classify_category("Teacher is teaching too fast in class.") == "Teaching Pace"
    assert classify_category("Computers in the lab are slow and compiler is missing.") == "Lab Facilities"
    assert classify_category("The teacher has not completed important syllabus chapters.") == "Syllabus Coverage"
    assert classify_category("Classroom fans and tube lights are not working.") == "Infrastructure & Hostel"
    assert classify_category("The canteen food quality is very unhygienic and lunch is cold.") == "Canteen & Food"
    assert classify_category("Need more company placement drives and aptitude training from TPO cell.") == "Placements & Training"
    assert classify_category("Admin office fee counter takes too long and bus transport is delayed.") == "College Services & Admin"
    assert classify_category("Library books are outdated and reading room needs more reference books.") == "Library Services"
    assert classify_category("General remarks.") == "Other"


def test_urgent_issue_detection():
    # Urgent cases
    res1 = analyze_feedback("All computers in the laboratory have stopped working for the last two weeks.")
    assert res1["urgent"] is True
    assert res1["category"] == "Lab Facilities"
    assert res1["sentiment_label"] == "Negative"

    res2 = analyze_feedback("Ceiling fan is broken and sparking with dangerous smoke.")
    assert res2["urgent"] is True

    # Non-urgent negative case
    res3 = analyze_feedback("The teacher is teaching too fast and we are confused.")
    assert res3["urgent"] is False
    assert res3["sentiment_label"] == "Negative"


def test_full_pipeline_integration():
    sample = "The lab computers are very slow and many are not working."
    output = analyze_feedback(sample)

    assert "sentiment_label" in output
    assert "sentiment_score" in output
    assert "category" in output
    assert "urgent" in output
    assert output["sentiment_label"] == "Negative"
    assert output["category"] == "Lab Facilities"


if __name__ == "__main__":
    test_text_cleaning()
    test_preprocessing()
    test_sentiment_analysis()
    test_category_classification()
    test_urgent_issue_detection()
    test_full_pipeline_integration()
    print("ALL ML Pipeline Tests Passed Successfully!")
