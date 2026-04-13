# API Contracts

## POST /predict

### Request

```json
{
  "text": "I want to cancel my order"
}
```

### Response

```json
{
  "text": "I want to cancel my order",
  "category": "cancellation",
  "score": 0.92
}
```

## Notes

- `text` must be a string.
- Response includes classification and confidence score.
- ML layer (`predict_category`): if preprocessing yields only whitespace, the API may return `category: "unknown"` and `score: 0.0` without loading model artifacts (keep response schema aligned with the FastAPI implementation).
- LLM fields may be added later.
