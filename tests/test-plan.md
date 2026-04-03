
````md

# Test Plan — Intelligent Triage System

## Purpose

This document defines the main tests that should be implemented for the **Intelligent Triage System**.

Its goal is to help the team:

- validate core behavior
- prevent regressions
- understand the system flow
- guide less experienced contributors when writing tests

This file describes **what should be tested** and **why**.  
The actual test implementation should be created inside the `tests/` folder.

---

# Test Strategy

The system should be tested in layers:

1. **Utils layer** → text cleaning and normalization
2. **ML layer** → prediction behavior and model outputs
3. **Service layer** → end-to-end pipeline logic
4. **API layer** → request/response validation
5. **Future integrations** → LLM, database, WhatsApp webhooks

---

# Priority Levels

- **P0** → critical for MVP
- **P1** → important for reliability
- **P2** → useful for robustness and future scale

---

# 1. Preprocessing Tests (`test_preprocessing.py`)

## 1.1 Lowercase normalization
**Priority:** P0

### Objective
Ensure text is converted to lowercase before inference.

### Validate
- uppercase input becomes lowercase

### Example input
```text
"HELLO WORLD"
````

### Expected result

```text
"hello world"
```

---

## 1.2 Punctuation removal

**Priority:** P0

### Objective

Ensure punctuation noise is removed correctly.

### Validate

* exclamation marks, commas, periods, etc. are removed or normalized according to system rules

### Example input

```text
"Hello!!! I need help..."
```

### Expected result

Text without noisy punctuation, preserving semantic meaning.

---

## 1.3 Extra whitespace normalization

**Priority:** P0

### Objective

Ensure unnecessary spaces are normalized.

### Validate

* multiple spaces become a single space
* leading/trailing spaces are removed

### Example input

```text
"   I   need   help   "
```

### Expected result

```text
"i need help"
```

---

## 1.4 Stopword removal

**Priority:** P1

### Objective

Validate that stopwords are removed only if this behavior is officially part of preprocessing.

### Validate

* common low-value words are removed
* meaningful words remain

### Note

This test should only exist if stopword removal is actually enabled in the project.

---

## 1.5 Token normalization consistency

**Priority:** P1

### Objective

Ensure equivalent textual variations are treated consistently.

### Validate

* normalized words remain stable across repeated calls
* no random behavior

### Example

Different casing or punctuation should lead to the same cleaned result.

---

## 1.6 Empty string handling

**Priority:** P0

### Objective

Ensure preprocessing handles empty input safely.

### Validate

* empty string does not crash the system
* output is empty string or controlled fallback

---

## 1.7 Special characters handling

**Priority:** P1

### Objective

Ensure unusual characters do not break preprocessing.

### Validate

* accents, symbols, emojis, or special punctuation are handled safely

### Example input

```text
"Olá!!! Preciso de ajuda 😅"
```

### Expected result

System does not crash and returns a valid cleaned string.

---

## 1.8 Numeric text handling

**Priority:** P1

### Objective

Ensure numbers are handled consistently.

### Validate

* numeric values are preserved, removed, or normalized according to preprocessing rules

### Example input

```text
"Error 504 since 10am"
```

### Expected result

Behavior follows project definition and remains consistent.

---

# 2. ML Prediction Tests (`test_model_prediction.py` or `test_predict.py`)

## 2.1 Prediction returns expected structure

**Priority:** P0

### Objective

Ensure the prediction function returns the expected fields.

### Validate

* result contains category
* result contains score/confidence

### Expected structure

```json
{
  "category": "...",
  "score": 0.0
}
```

---

## 2.2 Score is numeric

**Priority:** P0

### Objective

Ensure confidence score is returned in numeric format.

### Validate

* score is `float` or numeric equivalent

---

## 2.3 Score is within valid range

**Priority:** P0

### Objective

Ensure confidence score is valid.

### Validate

* score is between 0 and 1

---

## 2.4 Prediction handles known valid input

**Priority:** P0

### Objective

Ensure the model returns a valid category for known examples.

### Validate

* known training-like input produces a non-empty category
* output format is valid

### Note

Do not make this too rigid unless the model behavior is deterministic enough.

---

## 2.5 Prediction handles low-information input

**Priority:** P1

### Objective

Ensure the model handles vague or weak text safely.

### Validate

* very short inputs do not crash prediction
* output still respects schema

### Example input

```text
"help"
```

---

## 2.6 Prediction handles empty input safely

**Priority:** P0

### Objective

Ensure the model or service rejects/handles empty text safely.

### Validate

* empty input does not produce uncontrolled failure
* system returns controlled error or fallback

---

## 2.7 Model artifact loading works

**Priority:** P1

### Objective

Ensure saved model can be loaded correctly.

### Validate

* model file is found
* object loads without error
* prediction can be executed after loading

---

## 2.8 Vectorizer and model compatibility

**Priority:** P1

### Objective

Ensure vectorizer and trained model work together.

### Validate

* vectorizer output can be used by model
* no shape mismatch occurs

---

# 3. Pipeline Tests (`test_pipeline.py`)

## 3.1 Pipeline runs end-to-end

**Priority:** P0

### Objective

Ensure the complete processing flow works.

### Validate

* input passes through preprocessing
* model prediction is executed
* final response object is returned

---

## 3.2 Pipeline output structure is correct

**Priority:** P0

### Objective

Ensure pipeline output follows the expected contract.

### Validate

* output contains original text or processed text if defined
* output contains category
* output contains score

---

## 3.3 Pipeline uses same preprocessing as training

**Priority:** P0

### Objective

Ensure training and inference are aligned.

### Validate

* inference preprocessing uses the same logic expected by the model
* no mismatch between training and runtime cleaning

---

## 3.4 Pipeline handles invalid input type

**Priority:** P0

### Objective

Ensure wrong input types are safely handled.

### Validate

* `None`, integers, lists, or other invalid types do not break flow silently
* system raises controlled error or validation response

---

## 3.5 Pipeline handles long text

**Priority:** P1

### Objective

Ensure large inputs do not break the flow.

### Validate

* long ticket text is processed safely
* response still follows expected structure

---

## 3.6 Pipeline is deterministic for same input

**Priority:** P1

### Objective

Ensure repeated prediction for same input behaves consistently.

### Validate

* same input returns same category under same model/version
* score should be stable or nearly stable

---

# 4. API Tests (`test_api.py`)

## 4.1 Health endpoint returns success

**Priority:** P0

### Objective

Ensure system health route works.

### Validate

* `/health` returns status code 200
* response confirms service is alive

---

## 4.2 Predict endpoint returns success for valid input

**Priority:** P0

### Objective

Ensure `/predict` works with valid request body.

### Validate

* status code 200
* response contains expected fields

---

## 4.3 Predict endpoint validates request schema

**Priority:** P0

### Objective

Ensure API rejects invalid payloads.

### Validate

* missing `text` returns validation error
* wrong type for `text` returns validation error

---

## 4.4 Predict endpoint returns expected response schema

**Priority:** P0

### Objective

Ensure API response matches contract.

### Validate

* response includes defined keys
* key types are correct

---

## 4.5 Predict endpoint handles empty text

**Priority:** P0

### Objective

Ensure empty request content is safely handled.

### Validate

* API returns controlled error or business-defined fallback

---

## 4.6 Predict endpoint handles internal failure gracefully

**Priority:** P1

### Objective

Ensure internal errors are not exposed in a messy way.

### Validate

* API returns controlled error response
* system does not expose sensitive stack traces to clients

---

## 4.7 Response content type is correct

**Priority:** P1

### Objective

Ensure API returns JSON correctly.

### Validate

* response content type is JSON
* payload is parseable

---

# 5. Schema Validation Tests (`test_schemas.py` if needed)

## 5.1 Request schema accepts valid data

**Priority:** P1

### Objective

Ensure request schema allows correct payload.

### Validate

* valid text input is accepted

---

## 5.2 Request schema rejects missing text

**Priority:** P1

### Objective

Ensure request schema enforces required field.

### Validate

* missing `text` raises validation error

---

## 5.3 Request schema rejects invalid type

**Priority:** P1

### Objective

Ensure schema blocks invalid input type.

### Validate

* integer, list, dict in place of string should fail

---

# 6. Training Tests (`test_training.py`)

## 6.1 Training process runs without crashing

**Priority:** P1

### Objective

Ensure training script completes successfully with valid dataset.

### Validate

* vectorizer fits
* model trains
* artifact is generated

---

## 6.2 Training produces artifact files

**Priority:** P1

### Objective

Ensure training output is persisted correctly.

### Validate

* model artifact exists
* vectorizer artifact exists

---

## 6.3 Training data and labels align

**Priority:** P1

### Objective

Ensure feature matrix and labels are compatible.

### Validate

* no mismatch in training dimensions
* no missing target problem

---

# 7. Future LLM Tests (`test_llm_service.py`)

## 7.1 LLM response generation returns text

**Priority:** P2

### Objective

Ensure LLM integration returns a valid string response.

### Validate

* output is string
* output is not empty for valid context

---

## 7.2 LLM prompt includes category context

**Priority:** P2

### Objective

Ensure prompt construction uses classification context.

### Validate

* generated prompt contains category or structured context if defined

---

## 7.3 LLM fallback works when API fails

**Priority:** P2

### Objective

Ensure system does not break if LLM provider fails.

### Validate

* fallback response or disabled mode works safely

---

## 7.4 LLM can be toggled on/off

**Priority:** P2

### Objective

Ensure optional behavior can be controlled.

### Validate

* when disabled, pipeline skips LLM step
* when enabled, pipeline includes LLM call

---

# 8. Future Database Tests (`test_database.py`)

## 8.1 Prediction record can be stored

**Priority:** P2

### Objective

Ensure prediction results can be persisted.

### Validate

* text, category, and score are saved successfully

---

## 8.2 Stored prediction preserves expected fields

**Priority:** P2

### Objective

Ensure database record matches expected schema.

### Validate

* stored values are complete and consistent

---

# 9. Future WhatsApp Integration Tests (`test_webhooks.py`)

## 9.1 Webhook receives valid incoming payload

**Priority:** P2

### Objective

Ensure webhook endpoint accepts valid messaging event.

### Validate

* incoming webhook returns success
* payload is parsed correctly

---

## 9.2 Webhook rejects invalid payload

**Priority:** P2

### Objective

Ensure malformed webhook body is safely handled.

### Validate

* invalid event does not crash system
* controlled error is returned

---

## 9.3 Webhook triggers classification flow

**Priority:** P2

### Objective

Ensure incoming WhatsApp message reaches pipeline.

### Validate

* message text is extracted
* pipeline is called
* response path starts correctly

---

## 9.4 Webhook response flow handles provider failures

**Priority:** P2

### Objective

Ensure integration is resilient to provider/API issues.

### Validate

* failure does not crash service
* event is handled safely

---

# 10. Regression Tests

## 10.1 Previously fixed preprocessing bug does not return

**Priority:** P1

### Objective

Ensure known bugs stay fixed.

### Validate

* each bug fix should generate at least one regression test

---

## 10.2 API contract remains stable

**Priority:** P1

### Objective

Ensure contract changes are intentional.

### Validate

* if request/response schema changes, tests fail until docs and implementation are updated

---

# 11. Recommended Initial Test Implementation Order

## Phase 1 — MVP Critical

Implement first:

* lowercase normalization
* punctuation removal
* empty string handling
* prediction returns expected structure
* score range validation
* pipeline runs end-to-end
* `/health` returns 200
* `/predict` returns 200 for valid input
* `/predict` rejects invalid payload

---

## Phase 2 — Reliability

Implement next:

* whitespace normalization
* invalid input types
* long text handling
* deterministic behavior
* internal failure handling
* schema validation tests
* artifact loading tests

---

## Phase 3 — Future Expansion

Implement later:

* LLM tests
* database tests
* webhook tests
* regression suite for bugs discovered in production

---

# 12. Definition of a Good Test

A good test should:

* validate one clear behavior
* be easy to read
* fail when the system breaks
* avoid unnecessary complexity
* describe behavior, not implementation details

---

# 13. Final Rule

Whenever a new important behavior is added to the system, ask:

1. Can this break something important?
2. Does this affect the API contract?
3. Does this affect preprocessing or prediction?
4. Should this have a regression test?

If the answer is yes, add a test.

```