from typing import Dict, Any, Tuple
from core.logger import logger
from agents.ingestion.schemas import TransactionData

class RuleBasedAgent:
    """
    Detects fraud using predefined business rules.
    """
    
    def __init__(self):
        self.name = "rule_based_agent"
    
    def execute(self, transaction: TransactionData, user_history: Dict[str, Any] = None) -> Tuple[float, str]:
        """
        Evaluates transaction against fraud rules.
        
        Args:
            transaction: TransactionData object
            user_history: Historical data about user (optional)
            
        Returns:
            Tuple of (risk_score, explanation)
        """
        if user_history is None:
            user_history = {}
        
        try:
            risk_score = 0.0
            reasons = []
            
            # Rule 1: High amount transaction
            if transaction.amount > 5000:
                risk_score += 0.3
                reasons.append(f"High amount: ${transaction.amount}")
            
            # Rule 2: Multiple transactions in short time
            recent_txns = user_history.get("recent_transactions", [])
            if len(recent_txns) > 5:
                risk_score += 0.25
                reasons.append(f"High velocity: {len(recent_txns)} txns in 1 hour")
            
            # Rule 3: New device
            if user_history.get("known_devices", []):
                if transaction.device.device_id not in user_history["known_devices"]:
                    risk_score += 0.2
                    reasons.append("New device detected")
            
            # Rule 4: Unusual merchant category
            high_risk_merchants = ["casino", "crypto", "foreign_atm", "money_transfer"]
            if transaction.merchant_category and transaction.merchant_category.lower() in high_risk_merchants:
                risk_score += 0.25
                reasons.append(f"High-risk merchant category: {transaction.merchant_category}")
            
            # Rule 5: Transaction from new country/location
            if user_history.get("last_location") and transaction.location:
                if user_history["last_location"].lower() != transaction.location.lower():
                    risk_score += 0.2
                    reasons.append(f"New location: {transaction.location}")
            
            # Cap score at 1.0
            risk_score = min(risk_score, 1.0)
            explanation = " | ".join(reasons) if reasons else "No rules triggered"
            
            logger.info(f"{self.name}: Score={risk_score}, Txn={transaction.transaction_id}")
            return round(risk_score, 3), explanation
            
        except Exception as e:
            logger.error(f"{self.name}: Failed - {str(e)}")
            raise