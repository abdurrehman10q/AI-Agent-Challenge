from typing import Dict, Any, Tuple
from datetime import datetime
from core.logger import logger
from orchestration.state import PipelineState
from agents.ingestion.data_ingestion_agent import DataIngestionAgent
from agents.feature_engineering.feature_engineering_agent import FeatureEngineeringAgent
from agents.detection.rule_based_agent import RuleBasedAgent
from agents.detection.anomaly_detection_agent import AnomalyDetectionAgent
from agents.detection.graph_analysis_agent import GraphAnalysisAgent
from agents.risk_scoring.risk_scoring_agent import RiskScoringAgent
from agents.decision.decision_agent import DecisionAgent
from agents.coordinator.coordinator_agent import CoordinatorAgent
from agents.learning.learning_agent import LearningAgent

class PipelineGraphBuilder:
    """
    Builds and executes the multi-agent fraud detection pipeline.
    Orchestrates all agents in the correct order.
    """
    
    def __init__(self):
        self.logger = logger
        
        # Initialize all agents
        self.ingestion_agent = DataIngestionAgent()
        self.feature_engineering_agent = FeatureEngineeringAgent()
        self.rule_based_agent = RuleBasedAgent()
        self.anomaly_detection_agent = AnomalyDetectionAgent()
        self.graph_analysis_agent = GraphAnalysisAgent()
        self.risk_scoring_agent = RiskScoringAgent()
        self.decision_agent = DecisionAgent()
        self.coordinator_agent = CoordinatorAgent()
        self.learning_agent = LearningAgent()
    
    def execute_pipeline(self, transaction_dict: Dict[str, Any], user_history: Dict[str, Any] = None) -> PipelineState:
        """
        Executes the complete fraud detection pipeline.
        
        Flow:
        1. Ingestion → Validate raw data
        2. Feature Engineering → Extract features
        3. Detection (Parallel) → Run 3 detection agents
        4. Coordination → Resolve conflicts
        5. Risk Scoring → Aggregate scores
        6. Decision → Make final decision
        7. Learning → Record feedback
        
        Args:
            transaction_dict: Raw transaction data dict
            user_history: User's historical data (optional)
            
        Returns:
            PipelineState with complete results
        """
        
        state = PipelineState(transaction_id=transaction_dict.get("transaction_id", "unknown"))
        state.processing_start_time = datetime.utcnow()
        
        try:
            # ==================== STAGE 1: INGESTION ====================
            self.logger.info(f"Pipeline: Starting ingestion for {state.transaction_id}")
            state.transaction = self.ingestion_agent.execute(transaction_dict)
            state.ingestion_status = "success"
            
            # ==================== STAGE 2: FEATURE ENGINEERING ====================
            self.logger.info(f"Pipeline: Feature engineering for {state.transaction_id}")
            state.engineered_features = self.feature_engineering_agent.execute(
                state.transaction, 
                user_history
            )
            state.feature_engineering_status = "success"
            
            # ==================== STAGE 3: DETECTION (PARALLEL) ====================
            self.logger.info(f"Pipeline: Running detection agents for {state.transaction_id}")
            
            # Rule-Based Detection
            state.rule_based_score, state.rule_based_explanation = self.rule_based_agent.execute(
                state.transaction,
                user_history
            )
            
            # Anomaly Detection
            state.anomaly_detection_score, state.anomaly_detection_explanation = self.anomaly_detection_agent.execute(
                state.transaction,
                state.engineered_features
            )
            
            # Graph Analysis
            state.graph_analysis_score, state.graph_analysis_explanation = self.graph_analysis_agent.execute(
                state.transaction,
                user_history.get("network_graph", {}) if user_history else {}
            )
            
            state.detection_status = "success"
            
            # ==================== STAGE 4: COORDINATION ====================
            self.logger.info(f"Pipeline: Coordinating detection results for {state.transaction_id}")
            
            agent_scores = {
                "rule_based_agent": (state.rule_based_score, state.rule_based_explanation),
                "anomaly_detection_agent": (state.anomaly_detection_score, state.anomaly_detection_explanation),
                "graph_analysis_agent": (state.graph_analysis_score, state.graph_analysis_explanation),
            }
            
            state.final_risk_score, state.coordinator_strategy, state.agent_votes = self.coordinator_agent.execute(agent_scores)
            state.coordination_status = "success"
            
            # ==================== STAGE 5: RISK SCORING ====================
            self.logger.info(f"Pipeline: Risk scoring for {state.transaction_id}")
            
            # Risk scoring already done by coordinator, but we can add more here if needed
            state.risk_scoring_status = "success"
            
            # ==================== STAGE 6: DECISION ====================
            self.logger.info(f"Pipeline: Making decision for {state.transaction_id}")
            
            decision_result = self.decision_agent.execute(
                state.final_risk_score,
                state.coordinator_strategy
            )
            
            state.final_decision = decision_result["decision"]
            state.decision_explanation = decision_result["explanation"]
            state.action_details = decision_result
            state.decision_status = "success"
            
            # ==================== STAGE 7: LEARNING ====================
            self.logger.info(f"Pipeline: Recording for learning for {state.transaction_id}")
            state.learning_status = "queued"  # Will be processed asynchronously
            
            # Calculate processing time
            state.processing_end_time = datetime.utcnow()
            state.processing_time_ms = (state.processing_end_time - state.processing_start_time).total_seconds() * 1000
            
            self.logger.info(f"Pipeline: Complete for {state.transaction_id} - Decision: {state.final_decision}, Time: {state.processing_time_ms:.2f}ms")
            
            return state
            
        except Exception as e:
            self.logger.error(f"Pipeline: Failed for {state.transaction_id} - {str(e)}")
            state.decision_status = "failed"
            state.decision_explanation = f"Pipeline error: {str(e)}"
            raise