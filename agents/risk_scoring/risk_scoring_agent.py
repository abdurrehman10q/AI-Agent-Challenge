from typing import Dict, Any, Tuple, List
from core.logger import logger
from agents.risk_scoring.scoring_utils import ScoringUtils
from api.schemas.response import AgentVote

class RiskScoringAgent:
    """
    Aggregates outputs from detection agents and assigns a final fraud risk score.
    """
    
    def __init__(self):
        self.name = "risk_scoring_agent"
        self.scoring_utils = ScoringUtils()
        
        # Default weights for each detection agent
        self.default_weights = {
            "rule_based_agent": 0.4,
            "anomaly_detection_agent": 0.4,
            "graph_analysis_agent": 0.2,
        }
    
    def execute(self, agent_scores: Dict[str, Tuple[float, str]]) -> Tuple[float, List[AgentVote]]:
        """
        Aggregates detection agent scores into final risk score.
        
        Args:
            agent_scores: Dict of agent_name -> (score, explanation)
            
        Returns:
            Tuple of (final_risk_score, agent_votes)
        """
        try:
            # Extract scores only
            scores_only = {name: score for name, (score, _) in agent_scores.items()}
            
            # Extract explanations
            explanations = {name: explanation for name, (_, explanation) in agent_scores.items()}
            
            # Calculate weighted average
            final_score = self.scoring_utils.weighted_average(scores_only, self.default_weights)
            
            # Create agent votes
            agent_votes = [
                AgentVote(
                    agent=name,
                    score=score,
                    reason=explanations.get(name, "")
                )
                for name, score in scores_only.items()
            ]
            
            logger.info(f"{self.name}: Final score={final_score} from {len(agent_scores)} agents")
            
            return final_score, agent_votes
            
        except Exception as e:
            logger.error(f"{self.name}: Failed - {str(e)}")
            raise