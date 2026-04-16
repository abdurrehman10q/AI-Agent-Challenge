from fastapi import APIRouter
from api.schemas.response import FeedbackRequest
from core.logger import logger

router = APIRouter()

@router.post("/feedback")
def submit_feedback(feedback: FeedbackRequest):
    logger.info(f"Feedback: {feedback.transaction_id} -> {feedback.correct_decision}")
    # TODO: Send to Learning Agent (Member 2)
    return {"status": "received", "transaction_id": feedback.transaction_id}