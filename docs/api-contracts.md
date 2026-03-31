<!--
🇧🇷 COMO ATUALIZAR:
- Sempre que mudar input/output da API, atualize aqui
- Se adicionar novos endpoints, documente todos
- Backend e ML precisam seguir esse contrato
-->

# API Contracts

## POST /predict

### Request

```json
{
  "text": "I want to cancel my order"
}

RESPONSE

{
  "text": "I want to cancel my order",
  "category": "cancellation",
  "score": 0.92
}

Notes
text must be a string
Response includes classification and confidence score
LLM response may be added later



