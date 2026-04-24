from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from app.api.schemas import PredictRequest, PredictResponse, HealthResponse
from app.ml.predict_category import predict_category
from app.core.config import MODEL_PATH, VECTORIZER_PATH

router = APIRouter()


@router.post("/predict", response_model=PredictResponse)
def post_predict(body: PredictRequest):
    try:
        out = predict_category(body.text)
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model artifacts missing; check GET /health",
        )

    return PredictResponse(text=body.text, category=out["category"], score=out["score"])


@router.get("/health", response_model=HealthResponse)
def get_health():
    model_present = MODEL_PATH.is_file()
    vectorizer_present = VECTORIZER_PATH.is_file()
    ready = model_present and vectorizer_present
    payload = HealthResponse(status="ready" if ready else "not_ready")
    if ready:
        return payload
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content=payload.model_dump(),
    )