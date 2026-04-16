from pydantic import BaseModel
from typing import List
from core.constants import Decision

class AgentVote(BaseModel):
    agent: str
    score: float
    reason: str

class TransactionResponse(BaseModel):
    transaction_id: str
    risk_score: float
    decision: Decision
    explanation: str
    agent_votes: List[AgentVote]
    processing_time_ms: float

class FeedbackRequest(BaseModel):
    transaction_id: str
    correct_decision: Decision
    analyst_notes: str = ""