from fastapi import APIRouter
import time, random
from api.schemas.request import TransactionRequest
from api.schemas.response import TransactionResponse, AgentVote
from core.constants import Decision, RISK_THRESHOLDS
from core.logger import logger

router = APIRouter()

@router.post("/transaction/evaluate", response_model=TransactionResponse)
def evaluate_transaction(request: TransactionRequest):
    start = time.time()
    
    # --- MOCK MULTI-AGENT PIPELINE (Member 1 & 2 will replace this) ---
    rule_score = 0.9 if request.amount > 5000 else 0.2
    anomaly_score = random.uniform(0.5, 0.9) if "new" in (request.location or "").lower() else random.uniform(0.1, 0.4)
    graph_score = 0.7 if request.metadata.get("rapid") else 0.1
    
    # Coordinator Agent - Weighted Scoring
    risk_score = round(rule_score*0.4 + anomaly_score*0.4 + graph_score*0.2, 3)
    
    if risk_score >= RISK_THRESHOLDS[Decision.BLOCK]: decision = Decision.BLOCK
    elif risk_score >= RISK_THRESHOLDS[Decision.ESCALATE]: decision = Decision.ESCALATE
    elif risk_score >= RISK_THRESHOLDS[Decision.FLAG]: decision = Decision.FLAG
    else: decision = Decision.APPROVE

    votes = [
        AgentVote(agent="rule_based", score=rule_score, reason="High amount rule"),
        AgentVote(agent="anomaly_detection", score=anomaly_score, reason="IsolationForest"),
        AgentVote(agent="graph_analysis", score=graph_score, reason="Velocity check"),
    ]
    
    logger.info(f"TXN {request.transaction_id} -> {decision} ({risk_score})")
    
    return TransactionResponse(
        transaction_id=request.transaction_id,
        risk_score=risk_score,
        decision=decision,
        explanation=f"Aggregated from 3 agents. Rule={rule_score}, Anomaly={anomaly_score}",
        agent_votes=votes,
        processing_time_ms=round((time.time()-start)*1000, 2)
    )