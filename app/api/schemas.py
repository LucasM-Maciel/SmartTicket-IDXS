from pydantic import BaseModel


class PredictRequest(BaseModel):
    text: str


class PredictResponse(BaseModel):
    text: str
    category: str
    score: float


class HealthResponse(BaseModel):
    status: str
    model_present: bool
    vectorizer_present: bool
