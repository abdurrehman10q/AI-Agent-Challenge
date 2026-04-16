from fastapi import APIRouter
import time
from api.schemas.request import TransactionRequest
from api.schemas.response import TransactionResponse, AgentVote
from core.logger import logger
from orchestration.pipeline import FraudDetectionPipeline

router = APIRouter()

# Initialize pipeline once
pipeline = FraudDetectionPipeline()

@router.post("/transaction/evaluate", response_model=TransactionResponse)
def evaluate_transaction(request: TransactionRequest):
    """
    Evaluates a transaction for fraud using the multi-agent pipeline.
    
    The pipeline:
    1. Ingests and validates transaction data
    2. Engineers features from raw data
    3. Runs 3 parallel detection agents (rule-based, anomaly, graph)
    4. Coordinates results using voting and priority rules
    5. Scores risk using weighted aggregation
    6. Makes final decision (approve/flag/block/escalate)
    7. Records feedback for continuous learning
    
    Args:
        request: TransactionRequest with transaction details
        
    Returns:
        TransactionResponse with decision, risk score, and agent votes
    """
    start_time = time.time()
    
    try:
        logger.info(f"API: Processing transaction {request.transaction_id}")
        
        # Convert request to dict for pipeline
        transaction_dict = request.model_dump()
        
        # Optional: Add user history (can be fetched from database)
        # For now, we'll use empty history - in production, fetch from DB
        user_history = {
            "recent_transactions": [],
            "last_location": request.location,
            "avg_transaction_amount": 100,
            "known_devices": [],
        }
        
        # Execute pipeline
        pipeline_result = pipeline.process_transaction(transaction_dict, user_history)
        
        # Extract and format response
        response = TransactionResponse(
            transaction_id=pipeline_result["transaction_id"],
            risk_score=pipeline_result["risk_score"],
            decision=pipeline_result["decision"],
            explanation=pipeline_result["explanation"],
            agent_votes=[
                AgentVote(
                    agent=vote["agent"],
                    score=vote["score"],
                    reason=vote["reason"]
                )
                for vote in pipeline_result["agent_votes"]
            ],
            processing_time_ms=pipeline_result["processing_time_ms"],
        )
        
        logger.info(
            f"API: Transaction {request.transaction_id} evaluated - "
            f"Decision: {response.decision}, Risk: {response.risk_score}, "
            f"Time: {response.processing_time_ms:.2f}ms"
        )
        
        return response
        
    except Exception as e:
        logger.error(f"API: Failed to evaluate transaction {request.transaction_id} - {str(e)}")
        raise


@router.post("/transaction/batch-evaluate")
def batch_evaluate_transactions(requests: list[TransactionRequest]):
    """
    Evaluates multiple transactions in batch.
    
    Args:
        requests: List of TransactionRequest objects
        
    Returns:
        List of TransactionResponse objects
    """
    try:
        logger.info(f"API: Batch processing {len(requests)} transactions")
        
        results = []
        for request in requests:
            response = evaluate_transaction(request)
            results.append(response)
        
        logger.info(f"API: Batch processing complete - {len(results)} transactions evaluated")
        
        return {
            "total": len(results),
            "results": results,
        }
        
    except Exception as e:
        logger.error(f"API: Batch evaluation failed - {str(e)}")
        raise


@router.get("/transaction/pipeline-status")
def get_pipeline_status():
    """
    Gets the status of all agents in the pipeline.
    
    Returns:
        Dict with status of each agent
    """
    try:
        status = pipeline.get_pipeline_status()
        
        return {
            "pipeline_status": "healthy",
            "agents": status,
        }
        
    except Exception as e:
        logger.error(f"API: Failed to get pipeline status - {str(e)}")
        raise