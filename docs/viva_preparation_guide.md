# Final Year Project — Viva Preparation & Q&A Guide

## 1. Project Overview & Motivation
**Q: What is the purpose of this project?**  
**A:** The *Smart Feedback & Suggestion Portal* provides an automated, intelligent mechanism for educational institutions to collect, analyze, and act upon student feedback. Instead of manually reviewing hundreds of text submissions, our portal leverages an integrated Natural Language Processing (NLP) pipeline to automatically evaluate sentiment, classify feedback into operational categories, and instantly highlight urgent safety or infrastructure issues.

---

## 2. Technical Architecture & Decisions

**Q: Why did you choose FastAPI over Flask or Django?**  
**A:**
1. **High Performance & Asynchronous Support:** Built on Starlette and Pydantic, FastAPI is one of the fastest Python frameworks available.
2. **Built-in Type Validation:** Automatically enforces request/response schemas via Pydantic v2.
3. **Interactive Documentation:** Generates Swagger UI (`/docs`) out of the box.

**Q: Why use VADER rather than training a heavy Deep Learning model (like BERT or LSTM)?**  
**A:**
1. **Rule-Based & Lightweight:** VADER does not require expensive GPUs, extensive training datasets, or long warm-up delays.
2. **Valence-Aware:** Specifically optimized for sentiment expressions, punctuation emphasis (*e.g., "NOT working!"*), and intensifiers.
3. **Domain Customizability:** We enhanced VADER's lexicon with academic domain keywords (*e.g., "slow", "broken", "crashing"* with negative valence).
4. **Explainability in Viva:** Every score is deterministic and can be traced to exact valence rules.

**Q: How do you handle Student Anonymity?**  
**A:**
- When a student checks `anonymous: True`, the submission stores their `user_id` internally for audit/student history, but all API responses (both student view and admin table) explicitly set `student_name: null`.
- Admins can review the feedback text and take action without seeing who wrote it, encouraging honest student reporting.

---

## 3. NLP Pipeline Workflow

**Q: Can you explain the step-by-step NLP pipeline?**  
**A:**
1. **Preprocessing (`text_cleaner.py`):** Converts text to lowercase, strips URLs/emails/special symbols, tokenizes words, filters standard stop words while preserving sentiment-reversing negations (*e.g. "not", "no"*), and applies WordNet lemmatization.
2. **Sentiment Analysis (`sentiment_analyzer.py`):** Calculates compound polarity score ($-1.0$ to $+1.0$) and maps to `Positive`, `Neutral`, or `Negative`.
3. **Category Classification (`category_classifier.py`):** Evaluates multi-word phrases and keyword token scoring across 5 categories (*Teaching Pace, Lab Facilities, Syllabus Coverage, Infrastructure, Other*).
4. **Urgency Detection (`urgent_detector.py`):** Analyzes prolonged downtime patterns (*e.g., "not working for two weeks"*) and severe safety keywords (*e.g., "sparking", "broken fan"*) when sentiment is negative to set `urgent = True`.

---

## 4. Database Design & Integrity

**Q: What constraints ensure data integrity in your PostgreSQL schema?**  
**A:**
1. **Primary & Foreign Keys:** `users.id` referenced by `feedback.user_id` with `ON DELETE CASCADE`.
2. **Check Constraints:** 
   - `semester BETWEEN 1 AND 8`
   - `role IN ('student', 'admin')`
   - `sentiment_label IN ('Positive', 'Neutral', 'Negative')`
   - `category IN ('Teaching Pace', 'Lab Facilities', 'Syllabus Coverage', 'Infrastructure', 'Other')`
3. **Indexes:** Added to `email`, `department`, `sentiment_label`, `category`, and `urgent` columns for sub-millisecond query performance on the admin dashboard.
