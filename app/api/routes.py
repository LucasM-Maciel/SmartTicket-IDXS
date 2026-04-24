from fastapi import APIRouter

from app.api.schemas import PredictRequest, PredictResponse
from app.ml.predict_category import predict_category

router = APIRouter()


@router.post("/predict", response_model=PredictResponse)
def predict(body: PredictRequest):
    out = predict_category(body.text)

    return PredictResponse(text=body.text, category=out["category"], score=out["score"])
