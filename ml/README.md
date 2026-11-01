# ML — NLP Pipeline

This folder contains all Natural Language Processing (NLP) modules.

## Responsibility

- Preprocesses raw feedback text (cleaning, tokenization, etc.)
- Performs sentiment analysis using VADER to classify feedback as Positive, Neutral, or Negative.
- Classifies feedback into operational categories (Teaching Pace, Lab Facilities, etc.)
- Detects whether a feedback item represents an urgent issue.

## Why a Separate Module?

Keeping NLP logic separate from the backend makes it:
- Easy to replace individual modules (e.g., swap VADER for a trained model later).
- Easy to test each stage independently.
- Easy to explain each step during viva.

## Technology

| Tool           | Purpose                                |
|----------------|----------------------------------------|
| Python         | NLP language                           |
| NLTK           | Tokenization, stop-word removal, lemmatization |
| vaderSentiment | Sentiment analysis (rule-based, no training required) |

## Folder Structure (to be built in Phases 5–8)

```
ml/
├── preprocessing/
│   └── text_cleaner.py       → Cleans and normalizes raw text
├── sentiment/
│   └── sentiment_analyzer.py → VADER-based sentiment scoring
├── classification/
│   └── category_classifier.py→ Keyword-based category detection
├── test_samples/
│   └── sample_feedback.csv   → Sample inputs for testing the pipeline
└── README.md
```

## NLP Pipeline Flow

```
Raw Text
   ↓
text_cleaner.py      → Lowercase, remove punctuation, tokenize, remove stopwords
   ↓
sentiment_analyzer.py → VADER compound score → Positive / Neutral / Negative
   ↓
category_classifier.py → Keyword matching → Category label
   ↓
Urgent check          → Negative sentiment + strong urgency keywords → True/False
   ↓
Result returned to Backend
```

## Sentiment Score Reference

| Score Range       | Label    |
|-------------------|----------|
| score > 0.05      | Positive |
| -0.05 ≤ score ≤ 0.05 | Neutral |
| score < -0.05     | Negative |

## Categories

| Category        | Example Keywords                          |
|-----------------|-------------------------------------------|
| Teaching Pace   | fast, slow, rush, explain, unclear        |
| Lab Facilities  | lab, computer, system, equipment, broken  |
| Syllabus Coverage| syllabus, topic, chapter, complete, cover |
| Infrastructure  | fan, light, chair, desk, classroom, AC    |
| Other           | (default fallback)                        |
