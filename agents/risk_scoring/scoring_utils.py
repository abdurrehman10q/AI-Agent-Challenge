from typing import Dict, List, Tuple
from core.constants import Decision, RISK_THRESHOLDS

class ScoringUtils:
    """
    Utility functions for risk scoring and aggregation.
    """
    
    @staticmethod
    def weighted_average(scores: Dict[str, float], weights: Dict[str, float] = None) -> float:
        """
        Calculates weighted average of multiple scores.
        
        Args:
            scores: Dict of agent_name -> score
            weights: Dict of agent_name -> weight (defaults to equal weights)
            
        Returns:
            Weighted average score (0-1)
        """
        if not scores:
            return 0.0
        
        if weights is None:
            # Equal weights
            weights = {name: 1.0 / len(scores) for name in scores}
        
        total_weight = sum(weights.values())
        if total_weight == 0:
            return 0.0
        
        weighted_sum = sum(scores.get(name, 0) * weight for name, weight in weights.items())
        return round(weighted_sum / total_weight, 3)
    
    @staticmethod
    def voting_consensus(scores: Dict[str, float], threshold: float = 0.5) -> Tuple[float, int]:
        """
        Determines consensus score through voting.
        
        Args:
            scores: Dict of agent_name -> score
            threshold: Risk threshold for "voting yes" (default 0.5)
            
        Returns:
            Tuple of (consensus_score, vote_count)
        """
        if not scores:
            return 0.0, 0
        
        votes = sum(1 for score in scores.values() if score > threshold)
        consensus = votes / len(scores) if scores else 0.0
        
        return round(consensus, 3), votes
    
    @staticmethod
    def priority_based_aggregation(scores: Dict[str, float], priority_order: List[str] = None) -> float:
        """
        Aggregates scores based on priority order.
        Higher priority agents have more influence.
        
        Args:
            scores: Dict of agent_name -> score
            priority_order: List of agent names in priority order
            
        Returns:
            Priority-based score
        """
        if not scores:
            return 0.0
        
        if priority_order is None:
            priority_order = list(scores.keys())
        
        # Assign weights: first has highest weight
        weights = {}
        for i, agent_name in enumerate(priority_order):
            if agent_name in scores:
                weights[agent_name] = 1.0 / (i + 1)
        
        return ScoringUtils.weighted_average(scores, weights)
    
    @staticmethod
    def get_decision_from_score(risk_score: float) -> Decision:
        """
        Maps risk score to decision.
        
        Args:
            risk_score: Risk score (0-1)
            
        Returns:
            Decision enum
        """
        if risk_score >= RISK_THRESHOLDS[Decision.BLOCK]:
            return Decision.BLOCK
        elif risk_score >= RISK_THRESHOLDS[Decision.ESCALATE]:
            return Decision.ESCALATE
        elif risk_score >= RISK_THRESHOLDS[Decision.FLAG]:
            return Decision.FLAG
        else:
            return Decision.APPROVE