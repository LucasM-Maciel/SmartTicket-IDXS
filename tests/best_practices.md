````markdown
# 🧪 Tests — System Validation

## 🎯 Purpose

This folder is used to:

- Validate functionality  
- Ensure code stability  
- Prevent regressions  
- Verify expected behavior  

---

## 🔍 What Should Be Tested

- Text cleaning functions  
- Normalization logic  
- Pipeline behavior  
- Model predictions (basic checks)  
- API endpoints  

---

## 📌 Example Test Cases

```text
test_text_cleaning.py
test_pipeline.py
test_api.py
````

---

## 🧾 Example Test

```python
from app.utils.text_cleaning import clean_text

def test_clean_text_removes_extra_spaces():
    text = "  hello   world  "
    result = clean_text(text)
    assert result == "hello world"
```

---

## ⏱️ When to Write Tests

* After implementing a function
* Before integrating components
* When fixing bugs

---

## ⚠️ Important Rules

* Tests should be simple and focused
* Each test should verify one behavior
* Avoid testing implementation details — test outcomes

---

## 💡 Why This Matters

As the system grows (ML + API + DB + LLM), things can break easily.

Tests help:

* Detect issues early
* Ensure reliability
* Maintain consistency across the system

```