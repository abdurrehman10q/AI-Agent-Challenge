from typing import Dict, Any, Tuple, List
from core.logger import logger
from agents.coordinator.voting import VotingMechanism
from agents.coordinator.priority_rules import PriorityRules
from agents.risk_scoring.scoring_utils import ScoringUtils
from api.schemas.response import AgentVote

class CoordinatorAgent:
    """
    Central coordinator that resolves conflicts between agents.
    Uses weighted scoring, voting mechanisms, and priority rules.
    """
    
    def __init__(self):
        self.name = "coordinator_agent"
        self.voting = VotingMechanism()
        self.priority_rules = PriorityRules()
        self.scoring_utils = ScoringUtils()
    
    def execute(self, agent_scores: Dict[str, Tuple[float, str]]) -> Tuple[float, str, List[AgentVote]]:
        """
        Coordinates outputs from multiple detection agents and produces final risk score.
        
        Uses three coordination strategies:
        1. Weighted scoring (default)
        2. Priority-based rules
        3. Voting consensus
        
        Args:
            agent_scores: Dict of agent_name -> (score, explanation)
            
        Returns:
            Tuple of (final_score, coordination_strategy, agent_votes)
        """
        try:
            # Extract scores and explanations
            scores_only = {name: score for name, (score, _) in agent_scores.items()}
            explanations = {name: explanation for name, (_, explanation) in agent_scores.items()}
            
            # Strategy 1: Weighted Scoring (DEFAULT)
            weights = {
                "rule_based_agent": 0.4,
                "anomaly_detection_agent": 0.4,
                "graph_analysis_agent": 0.2,
            }
            weighted_score = self.scoring_utils.weighted_average(scores_only, weights)
            
            # Strategy 2: Priority-based Rules
            priority_score = self.priority_rules.consensus_with_override(scores_only)
            
            # Strategy 3: Voting Consensus
            voting_decisions = {name: score > 0.5 for name, score in scores_only.items()}
            voting_consensus, voting_confidence = self.voting.majority_vote(voting_decisions)
            voting_score = 0.7 if voting_consensus else 0.3
            
            # Use weighted scoring as primary strategy
            final_score = weighted_score
            strategy_used = "weighted_scoring"
            
            # Check if priority rule overrides
            if abs(priority_score - weighted_score) > 0.2:
                # Large difference - use consensus with override
                final_score = priority_score
                strategy_used = "priority_override"
            
            # Create agent votes
            agent_votes = [
                AgentVote(
                    agent=name,
                    score=score,
                    reason=explanations.get(name, "")
                )
                for name, score in scores_only.items()
            ]
            
            final_explanation = f"Coordination via {strategy_used}: {final_score}"
            
            logger.info(f"{self.name}: Final score={final_score}, Strategy={strategy_used}")
            
            return final_score, final_explanation, agent_votes
            
        except Exception as e:
            logger.error(f"{self.name}: Failed - {str(e)}")
            raise