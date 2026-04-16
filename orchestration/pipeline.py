from typing import Dict, Any, Optional
from core.logger import logger
from orchestration.graph_builder import PipelineGraphBuilder
from orchestration.state import PipelineState

class FraudDetectionPipeline:
    """
    Main fraud detection pipeline interface.
    Provides simple API to run transactions through the multi-agent system.
    """
    
    def __init__(self):
        self.graph_builder = PipelineGraphBuilder()
        self.logger = logger
    
    def process_transaction(self, transaction_dict: Dict[str, Any], 
                          user_history: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Processes a transaction through the entire fraud detection pipeline.
        
        Args:
            transaction_dict: Raw transaction data
            user_history: User's historical data (optional)
            
        Returns:
            Result dict with decision, risk score, and explanations
        """
        try:
            # Execute pipeline
            state = self.graph_builder.execute_pipeline(transaction_dict, user_history)
            
            # Return structured result
            result = {
                "transaction_id": state.transaction_id,
                "risk_score": state.final_risk_score,
                "decision": state.final_decision.value if state.final_decision else "unknown",
                "explanation": state.decision_explanation,
                "agent_votes": [
                    {
                        "agent": vote.agent,
                        "score": vote.score,
                        "reason": vote.reason
                    }
                    for vote in state.agent_votes
                ],
                "processing_time_ms": state.processing_time_ms,
                "action_details": state.action_details,
            }
            
            self.logger.info(f"Pipeline result: {result['transaction_id']} -> {result['decision']}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Pipeline processing failed: {str(e)}")
            raise
    
    def get_pipeline_status(self) -> Dict[str, str]:
        """
        Returns the status of all agents in the pipeline.
        
        Returns:
            Dict with agent statuses
        """
        return {
            "ingestion_agent": "active",
            "feature_engineering_agent": "active",
            "rule_based_agent": "active",
            "anomaly_detection_agent": "active",
            "graph_analysis_agent": "active",
            "risk_scoring_agent": "active",
            "decision_agent": "active",
            "coordinator_agent": "active",
            "learning_agent": "active",
        }