from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from agents.ingestion.schemas import TransactionData
from api.schemas.response import AgentVote
from core.constants import Decision

@dataclass
class PipelineState:
    """
    Represents the state of a transaction as it flows through the multi-agent pipeline.
    """
    
    # Transaction Data
    transaction: Optional[TransactionData] = None
    transaction_id: str = ""
    
    # Ingestion Stage
    ingestion_status: str = "pending"  # pending, success, failed
    ingestion_error: Optional[str] = None
    
    # Feature Engineering Stage
    engineered_features: Dict[str, float] = field(default_factory=dict)
    feature_engineering_status: str = "pending"
    
    # Detection Stage
    rule_based_score: float = 0.0
    rule_based_explanation: str = ""
    
    anomaly_detection_score: float = 0.0
    anomaly_detection_explanation: str = ""
    
    graph_analysis_score: float = 0.0
    graph_analysis_explanation: str = ""
    
    detection_status: str = "pending"
    
    # Risk Scoring Stage
    final_risk_score: float = 0.0
    risk_scoring_status: str = "pending"
    
    # Coordination Stage
    coordinator_strategy: str = ""
    coordination_status: str = "pending"
    
    # Decision Stage
    final_decision: Optional[Decision] = None
    decision_explanation: str = ""
    action_details: Dict[str, Any] = field(default_factory=dict)
    decision_status: str = "pending"
    
    # Agent Votes
    agent_votes: List[AgentVote] = field(default_factory=list)
    
    # Metadata
    processing_start_time: Optional[datetime] = None
    processing_end_time: Optional[datetime] = None
    processing_time_ms: float = 0.0
    
    def get_summary(self) -> Dict[str, Any]:
        """Returns a summary of the current state."""
        return {
            "transaction_id": self.transaction_id,
            "risk_score": self.final_risk_score,
            "decision": self.final_decision,
            "explanation": self.decision_explanation,
            "processing_time_ms": self.processing_time_ms,
            "agent_votes": self.agent_votes,
        }
    
    def __repr__(self) -> str:
        return f"PipelineState(txn={self.transaction_id}, decision={self.final_decision}, risk={self.final_risk_score})"