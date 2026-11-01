"""
ml/classification/category_classifier.py
========================================
Rule-based category classification for student feedback.

Primary Operational Categories:
  1. Teaching Pace / Academics
  2. Lab Facilities
  3. Canteen & Food
  4. Placements & Training
  5. College Services & Admin
  6. Infrastructure & Hostel
  7. Library Services
  8. Syllabus Coverage
  9. Other (Default fallback)
"""

import re
from typing import Dict, List, Tuple
from ml.preprocessing.text_cleaner import preprocess, clean_text

CATEGORY_KEYWORDS = {
    "Teaching Pace": [
        "pace", "fast", "slow", "rush", "rushed", "speed", "speedy", "teach", "teaching",
        "teacher", "faculty", "professor", "explain", "explanation", "understand",
        "understanding", "clear", "unclear", "doubt", "doubts", "lecture", "lectures",
        "concept", "concepts", "confusing", "voice", "accent", "audible", "boring",
        "interactive", "delivery", "slides", "notes"
    ],
    "Lab Facilities": [
        "lab", "laboratory", "computer", "computers", "system", "systems", "pc",
        "software", "hardware", "instrument", "instruments", "equipment", "equipments",
        "machine", "machines", "mouse", "keyboard", "monitor", "screen",
        "compiler", "ide", "workbench", "multimeter", "oscilloscope", "wire", "wires",
        "kit", "practical", "practicals", "coding setup"
    ],
    "Canteen & Food": [
        "canteen", "cafeteria", "food", "mess", "meal", "lunch", "dinner", "breakfast",
        "snacks", "tea", "coffee", "hygiene", "hygienic", "unhygienic", "taste", "tasty",
        "quality of food", "stale", "oil", "oily", "drinking water", "water cooler",
        "menu", "cook", "chef", "plate", "plates", "spoon", "dining", "roti", "rice",
        "curry", "cleanliness in canteen"
    ],
    "Placements & Training": [
        "placement", "placements", "tpo", "job", "jobs", "hiring", "recruit", "recruitment",
        "recruiter", "recruiters", "interview", "interviews", "company", "companies",
        "package", "salary", "lpa", "resume", "cv", "aptitude", "mock interview",
        "training", "internship", "internships", "career", "guidance", "skill development",
        "campus drive", "off campus", "drive"
    ],
    "College Services & Admin": [
        "admin", "administration", "office", "registrar", "fee", "fees", "account",
        "counter", "scholarship", "staff", "clerk", "certificate", "documents",
        "admission", "bus", "transport", "transportation", "parking", "security",
        "guard", "id card", "notice", "circular", "management", "portal"
    ],
    "Infrastructure & Hostel": [
        "infrastructure", "classroom", "classrooms", "class", "bench", "benches",
        "desk", "desks", "chair", "chairs", "fan", "fans", "light", "lights",
        "tube light", "ac", "air conditioner", "air condition", "cooling", "heat",
        "hot", "projector", "projectors", "whiteboard", "blackboard", "marker",
        "room", "rooms", "hall", "washroom", "washrooms", "toilet", "toilets",
        "dirty", "smell", "lift", "elevator", "building", "window", "power",
        "electricity", "socket", "switch", "hostel", "warden", "water supply",
        "wifi", "internet"
    ],
    "Library Services": [
        "library", "book", "books", "journal", "journals", "reading room", "study room",
        "librarian", "issue", "issuing", "return", "quiet", "silence", "reference",
        "digital library", "magazines", "author", "edition", "fine"
    ],
    "Syllabus Coverage": [
        "syllabus", "chapter", "chapters", "topic", "topics", "unit", "units",
        "portion", "portions", "curriculum", "course", "subject", "module", "modules",
        "exam", "exams", "midsem", "endsem", "incomplete", "complete", "completed",
        "finish", "coverage", "covered", "uncovered", "pending", "skipped", "skip",
        "assignment", "assignments", "syllabus not completed"
    ],
}

# Multi-word key phrases with higher scoring weight (Weight = 3.0)
CATEGORY_PHRASES = {
    "Teaching Pace": [
        "teaching too fast", "too fast", "too slow", "teaching speed", "hard to follow",
        "cannot understand", "can't understand", "explains very well", "good explanation",
        "clear explanation", "slides are not clear", "doubt session", "lecture pace"
    ],
    "Lab Facilities": [
        "not working", "slow computer", "lab computer", "lab systems", "lab equipment",
        "systems are slow", "computers are slow", "software not installed", "broken equipment",
        "practical sessions", "lab apparatus", "oscilloscope not working"
    ],
    "Canteen & Food": [
        "canteen food", "mess food", "food quality", "taste of food", "unhygienic food",
        "drinking water", "water cooler", "dirty plates", "stale food", "canteen prices",
        "lunch quality", "breakfast quality", "meal quality"
    ],
    "Placements & Training": [
        "placement cell", "placement drive", "tpo cell", "campus placements", "mock interviews",
        "aptitude training", "placement opportunities", "top companies", "internship opportunity",
        "resume building", "training session"
    ],
    "College Services & Admin": [
        "admin office", "accounts section", "fee payment", "scholarship form", "bus service",
        "college transport", "administrative staff", "id card counter", "student support"
    ],
    "Infrastructure & Hostel": [
        "fan not working", "ac not working", "broken chair", "projector not working",
        "hostel room", "washroom cleanliness", "dirty washroom", "poor lighting",
        "no electricity", "broken bench", "hot classroom", "hostel facility"
    ],
    "Library Services": [
        "library books", "reading hall", "book issuing", "digital library", "reference books",
        "library staff", "quiet environment in library"
    ],
    "Syllabus Coverage": [
        "syllabus completion", "syllabus not completed", "topics not covered",
        "chapters skipped", "portion incomplete", "before exams", "pending chapters"
    ],
}


class CategoryClassifier:
    def __init__(self):
        self.category_keywords = CATEGORY_KEYWORDS
        self.category_phrases = CATEGORY_PHRASES

    def classify(self, text: str) -> str:
        """
        Classify feedback text into an operational category using phrase & keyword scoring.
        """
        if not text or not isinstance(text, str) or not text.strip():
            return "Other"

        text_lower = text.lower()
        cleaned_tokens = set(preprocess(text)["lemmatized_tokens"])

        scores: Dict[str, float] = {cat: 0.0 for cat in self.category_keywords}

        # 1. Multi-word phrase matching (Weight = 3.0)
        for cat, phrases in self.category_phrases.items():
            for phrase in phrases:
                if phrase in text_lower:
                    scores[cat] += 3.0

        # 2. Token / keyword matching (Weight = 1.0 / 1.5)
        for cat, keywords in self.category_keywords.items():
            for kw in keywords:
                if " " not in kw:
                    if kw in cleaned_tokens:
                        scores[cat] += 1.0
                else:
                    if kw in text_lower:
                        scores[cat] += 1.5

        # Determine category with highest score
        best_category = "Other"
        max_score = 0.0

        for cat, score in scores.items():
            if score > max_score:
                max_score = score
                best_category = cat

        if max_score == 0.0:
            return "Other"

        return best_category


# Singleton instance
_default_classifier = CategoryClassifier()


def classify_category(text: str) -> str:
    """Convenience function to classify feedback text."""
    return _default_classifier.classify(text)
