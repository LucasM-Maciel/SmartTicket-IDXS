import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.api.schemas import PredictRequest, PredictResponse, HealthResponse
from app.core.config import MODEL_PATH, VECTORIZER_PATH
from app.core.triage_settings import get_llm_min_score
from app.db.repository import save_ticket_prediction
from app.db.session import get_db
from app.services.classifier import classify_ticket
from app.services.ticket_triage import triage_prediction

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/predict", response_model=PredictResponse)
def post_predict(
    body: PredictRequest, db: Session | None = Depends(get_db)
) -> PredictResponse:
    try:
        out = classify_ticket(body.text)
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model artifacts missing; check GET /health",
        )

    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database persistence not configured.",
        )

    llm_min = get_llm_min_score()
    urgency, queue_target = triage_prediction(out.category, out.score, llm_min_score=llm_min)

    try:
        save_ticket_prediction(
            db,
            text_raw=body.text,
            text_processed=out.text_processed,
            category=out.category,
            score=out.score,
            urgency=urgency,
            queue_target=queue_target,
        )
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Database transaction failed while persisting ticket prediction.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not persist ticket; database unavailable.",
        )

    return PredictResponse(
        text=body.text,
        category=out.category,
        score=out.score,
        urgency=urgency,
        queue_target=queue_target,
    )


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