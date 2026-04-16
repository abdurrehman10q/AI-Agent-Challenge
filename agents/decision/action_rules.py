from enum import Enum
from typing import Dict, Any
from core.constants import Decision

class ActionRule(str, Enum):
    """
    Rules that determine actions based on decision.
    """
    APPROVE = "approve"
    FLAG_FOR_REVIEW = "flag_for_review"
    BLOCK = "block"
    ESCALATE_TO_ANALYST = "escalate_to_analyst"

class ActionRules:
    """
    Maps decisions to specific actions.
    """
    
    @staticmethod
    def get_action(decision: Decision, risk_score: float) -> Dict[str, Any]:
        """
        Determines action based on decision and risk score.
        
        Args:
            decision: Decision enum
            risk_score: Risk score (0-1)
            
        Returns:
            Dict with action details
        """
        actions = {
            Decision.APPROVE: {
                "action": ActionRule.APPROVE,
                "message": "Transaction approved",
                "notify_user": False,
                "notify_analyst": False,
                "block_transaction": False,
            },
            Decision.FLAG: {
                "action": ActionRule.FLAG_FOR_REVIEW,
                "message": "Transaction flagged for review",
                "notify_user": True,
                "notify_analyst": True,
                "block_transaction": False,
            },
            Decision.ESCALATE: {
                "action": ActionRule.ESCALATE_TO_ANALYST,
                "message": "Transaction escalated to analyst",
                "notify_user": True,
                "notify_analyst": True,
                "priority": "high",
                "block_transaction": False,
            },
            Decision.BLOCK: {
                "action": ActionRule.BLOCK,
                "message": "Transaction blocked due to fraud risk",
                "notify_user": True,
                "notify_analyst": True,
                "block_transaction": True,
                "priority": "critical",
            },
        }
        
        return actions.get(decision, actions[Decision.APPROVE])