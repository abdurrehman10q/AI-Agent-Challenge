from typing import List, Dict, Any
from core.logger import logger

class PriorityRules:
    """
    Implements priority-based rules for conflict resolution.
    """
    
    # Default priority order (index 0 = highest priority)
    DEFAULT_PRIORITY_ORDER = [
        "rule_based_agent",           # Hardcoded rules have highest priority
        "anomaly_detection_agent",     # ML-based detection
        "graph_analysis_agent",        # Network analysis
    ]
    
    @staticmethod
    def apply_priority_rule(agent_scores: Dict[str, float], priority_order: List[str] = None) -> float:
        """
        Applies priority-based aggregation.
        Higher priority agents override lower priority agents.
        
        Args:
            agent_scores: Dict of agent_name -> score
            priority_order: List of agent names in priority order
            
        Returns:
            Final score based on priority
        """
        if not agent_scores:
            return 0.0
        
        if priority_order is None:
            priority_order = PriorityRules.DEFAULT_PRIORITY_ORDER
        
        # Find highest priority agent with non-zero score
        for agent_name in priority_order:
            if agent_name in agent_scores:
                score = agent_scores[agent_name]
                if score > 0:
                    logger.info(f"Priority rule: Using {agent_name} score={score}")
                    return score
        
        # Fallback: return average if no high-priority agent has score
        avg_score = sum(agent_scores.values()) / len(agent_scores)
        logger.info(f"Priority rule: Using average score={avg_score}")
        return avg_score
    
    @staticmethod
    def enforce_rule_override(agent_scores: Dict[str, float], rule_based_score: float) -> float:
        """
        If rule-based agent flags transaction, it overrides others.
        
        Args:
            agent_scores: Dict of agent_name -> score
            rule_based_score: Score from rule-based agent
            
        Returns:
            Final score (potentially overridden)
        """
        # If rule-based score is very high, override others
        if rule_based_score > 0.7:
            logger.info(f"Rule override: Using rule_based_score={rule_based_score}")
            return rule_based_score
        
        # Otherwise, use average
        avg_score = sum(agent_scores.values()) / len(agent_scores)
        logger.info(f"No rule override: Using average={avg_score}")
        return avg_score
    
    @staticmethod
    def consensus_with_override(agent_scores: Dict[str, float], override_threshold: float = 0.75) -> float:
        """
        Use consensus but allow high-confidence agents to override.
        
        Args:
            agent_scores: Dict of agent_name -> score
            override_threshold: Threshold for override (default 0.75)
            
        Returns:
            Final score
        """
        if not agent_scores:
            return 0.0
        
        # Check for override
        for agent_name, score in agent_scores.items():
            if score >= override_threshold:
                logger.info(f"Consensus override: {agent_name} score={score} exceeds threshold")
                return score
        
        # Use weighted average as consensus
        avg_score = sum(agent_scores.values()) / len(agent_scores)
        logger.info(f"Consensus: Using average={avg_score}")
        return avg_score