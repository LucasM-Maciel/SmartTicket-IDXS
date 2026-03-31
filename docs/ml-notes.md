<!--
🇧🇷 COMO ATUALIZAR:
- Sempre que testar modelo novo, registrar aqui
- Sempre que mudar preprocessing, registrar
- Sempre que avaliar modelo, colocar métricas
- Isso vira ouro pra entrevista depois
-->

# ML Notes

## Objective
Classify customer messages into predefined categories

## Categories (Initial)

- support
- financial
- complaint
- cancellation

## Pipeline

```text
text → clean → normalize → vectorize (TF-IDF) → model

[Model]
-Logistic Regression (baseline)

[Features]
-TF-IDF vectors

[Evaluation Metrics]
-Accuracy
-Precision
-Recall
-F1-score

[Current Status]
-Project structure created
-Pipeline defined (not fully implemented yet)

[Future Improvements]
-Try Naive Bayes
-Try SVM
-Improve preprocessing
-Hyperparameter tuning