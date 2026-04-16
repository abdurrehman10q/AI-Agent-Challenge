from typing import Dict, Any
from core.logger import logger
from core.constants import Decision
from agents.decision.action_rules import ActionRules
from agents.risk_scoring.scoring_utils import ScoringUtils

class DecisionAgent:
    """
    Makes final decision on transaction based on risk score.
    Determines action: Approve, Flag, Escalate, or Block.
    """
    
    def __init__(self):
        self.name = "decision_agent"
        self.scoring_utils = ScoringUtils()
        self.action_rules = ActionRules()
    
    def execute(self, risk_score: float, explanation: str = "") -> Dict[str, Any]:
        """
        Makes final decision on transaction.
        
        Args:
            risk_score: Final risk score from Risk Scoring Agent
            explanation: Explanation of risk score
            
        Returns:
            Dict with decision, action, and rationale
        """
        try:
            # Map score to decision
            decision = self.scoring_utils.get_decision_from_score(risk_score)
            
            # Get action details
            action_details = self.action_rules.get_action(decision, risk_score)
            
            result = {
                "decision": decision,
                "risk_score": risk_score,
                "explanation": explanation or f"Risk score {risk_score} triggers {decision.value} decision",
                "action": action_details.get("action"),
                "message": action_details.get("message"),
                "notify_user": action_details.get("notify_user", False),
                "notify_analyst": action_details.get("notify_analyst", False),
                "block_transaction": action_details.get("block_transaction", False),
                "priority": action_details.get("priority", "normal"),
            }
            
            logger.info(f"{self.name}: Decision={decision}, Risk={risk_score}, Action={action_details.get('action')}")
            
            return result
            
        except Exception as e:
            logger.error(f"{self.name}: Failed - {str(e)}")
            raise