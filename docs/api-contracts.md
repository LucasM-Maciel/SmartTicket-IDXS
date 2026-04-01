````md id="apicontracts001"
# API Contracts

## POST /predict

### Request

```json
{
  "text": "I want to cancel my order"
}
````

---

### Response

```json
{
  "text": "I want to cancel my order",
  "category": "cancellation",
  "score": 0.92
}
```

---

## Notes

* `text` must be a string
* Response includes classification and confidence score
* LLM response may be added later

```


