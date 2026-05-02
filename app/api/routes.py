import logging
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.api.schemas import (
    HealthResponse,
    PredictRequest,
    PredictResponse,
    TicketQueueResponse,
)
from app.core.config import MODEL_PATH, VECTORIZER_PATH
from app.core.triage_settings import get_llm_min_score
from app.db.queue_repository import list_tickets_queue
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


@router.get("/tickets", response_model=TicketQueueResponse)
def get_tickets(
    db: Session | None = Depends(get_db),
    queue_target: Annotated[
        Literal["human", "llm"] | None,
        Query(description="If set, only tickets routed to this queue."),
    ] = None,
    limit: Annotated[int, Query(ge=1, le=100, description="Page size (max 100).")] = 50,
    offset: Annotated[int, Query(ge=0, description="Rows to skip for pagination.")] = 0,
) -> TicketQueueResponse:
    """List persisted tickets in queue order: urgency tier (HIGH→MEDIUM→LOW), then FIFO."""
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database persistence not configured.",
        )
    try:
        rows, total = list_tickets_queue(
            db,
            queue_target=queue_target,
            limit=limit,
            offset=offset,
        )
    except SQLAlchemyError:
        logger.exception("Database query failed while listing tickets.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not load tickets; database unavailable.",
        )

    return TicketQueueResponse(
        items=rows,
        total=total,
        limit=limit,
        offset=offset,
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