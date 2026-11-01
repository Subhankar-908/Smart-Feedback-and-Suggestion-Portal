# Test Samples

This folder will contain `sample_feedback.csv` — test input data for the NLP pipeline.

**Purpose (Phase 8):**
- Provide a realistic set of sample feedback text for testing each NLP module individually.
- Verify that sentiment, category, and urgency detection produce correct outputs.

**CSV Format:**

```
feedback_text,expected_sentiment,expected_category,expected_urgent
"The lab computers are not working for 2 weeks.",Negative,Lab Facilities,True
"The teacher explains concepts very clearly.",Positive,Teaching Pace,False
"Some important chapters have not been covered.",Negative,Syllabus Coverage,False
"The classroom fans are broken.",Negative,Infrastructure,False
"Overall a good experience.",Positive,Other,False
```

This file will be created in Phase 8.
