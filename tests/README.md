# Tests

This folder contains all automated tests for the project.

## Responsibility

- Validates that backend API endpoints behave correctly.
- Validates that the NLP pipeline produces correct outputs.
- Helps catch bugs before they reach the main branch.

## Structure (to be filled in Phase 14)

```
tests/
├── backend/    → API and service tests using pytest
├── ml/         → NLP module unit tests
└── README.md   → This file
```

## What Will Be Tested

### Backend Tests (`tests/backend/`)

| Test Area              | What is Verified                                     |
|------------------------|------------------------------------------------------|
| Auth - Registration    | Valid registration, duplicate email, missing fields  |
| Auth - Login           | Correct credentials, wrong password, unknown user    |
| Feedback Submission    | Valid input, empty text, unauthorized access         |
| Admin Endpoints        | Dashboard data, filter queries, role enforcement     |
| Anonymous Feedback     | Student identity hidden for anonymous submissions    |

### ML Tests (`tests/ml/`)

| Test Area              | What is Verified                                     |
|------------------------|------------------------------------------------------|
| Preprocessing          | Lowercasing, punctuation removal, tokenization       |
| Sentiment Analysis     | Positive, Neutral, Negative classification accuracy  |
| Category Classifier    | Correct category for known example inputs            |
| Urgent Detection       | Correctly flags urgent vs non-urgent feedback        |

## Running Tests

```bash
# From project root
cd backend
pytest ../tests/backend/ -v

cd ..
pytest tests/ml/ -v
```
