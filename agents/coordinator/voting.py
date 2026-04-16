from typing import Dict, List, Tuple
from core.logger import logger

class VotingMechanism:
    """
    Implements voting mechanisms to resolve conflicts between agents.
    """
    
    @staticmethod
    def majority_vote(agent_decisions: Dict[str, bool], threshold: float = 0.5) -> Tuple[bool, float]:
        """
        Simple majority voting.
        
        Args:
            agent_decisions: Dict of agent_name -> decision (True/False)
            threshold: Threshold for majority (default 0.5 = 50%)
            
        Returns:
            Tuple of (final_decision, confidence)
        """
        if not agent_decisions:
            return False, 0.0
        
        votes_yes = sum(1 for decision in agent_decisions.values() if decision)
        total_votes = len(agent_decisions)
        confidence = votes_yes / total_votes
        
        final_decision = confidence >= threshold
        
        logger.info(f"Majority vote: {votes_yes}/{total_votes} = {confidence:.2%} confidence")
        
        return final_decision, round(confidence, 3)
    
    @staticmethod
    def weighted_vote(agent_decisions: Dict[str, bool], weights: Dict[str, float]) -> Tuple[bool, float]:
        """
        Weighted voting where some agents have more influence.
        
        Args:
            agent_decisions: Dict of agent_name -> decision (True/False)
            weights: Dict of agent_name -> weight (0-1)
            
        Returns:
            Tuple of (final_decision, confidence)
        """
        if not agent_decisions:
            return False, 0.0
        
        total_weight = sum(weights.get(name, 1.0) for name in agent_decisions)
        if total_weight == 0:
            return False, 0.0
        
        weighted_yes = sum(
            weights.get(name, 1.0) for name, decision in agent_decisions.items() if decision
        )
        
        confidence = weighted_yes / total_weight
        final_decision = confidence >= 0.5
        
        logger.info(f"Weighted vote: confidence={confidence:.2%}")
        
        return final_decision, round(confidence, 3)
    
    @staticmethod
    def unanimous_vote(agent_decisions: Dict[str, bool]) -> Tuple[bool, float]:
        """
        Unanimous voting - all agents must agree.
        
        Args:
            agent_decisions: Dict of agent_name -> decision (True/False)
            
        Returns:
            Tuple of (final_decision, confidence)
        """
        if not agent_decisions:
            return False, 0.0
        
        all_yes = all(agent_decisions.values())
        all_no = not any(agent_decisions.values())
        
        if all_yes:
            confidence = 1.0
            final_decision = True
        elif all_no:
            confidence = 1.0
            final_decision = False
        else:
            confidence = 0.0
            final_decision = False
        
        logger.info(f"Unanimous vote: decision={final_decision}, confidence={confidence:.2%}")
        
        return final_decision, round(confidence, 3)