from typing import Dict, Any, Tuple, List
from core.logger import logger
from agents.ingestion.schemas import TransactionData

class GraphAnalysisAgent:
    """
    Detects fraud networks and suspicious patterns using graph analysis.
    """
    
    def __init__(self):
        self.name = "graph_analysis_agent"
    
    def execute(self, transaction: TransactionData, user_network: Dict[str, Any] = None) -> Tuple[float, str]:
        """
        Analyzes transaction in context of user's network.
        
        Args:
            transaction: TransactionData object
            user_network: Network graph data (users, merchants, devices, locations)
            
        Returns:
            Tuple of (risk_score, explanation)
        """
        if user_network is None:
            user_network = {}
        
        try:
            risk_score = 0.0
            reasons = []
            
            # Check 1: Device network - how many users used this device?
            device_users = user_network.get("device_to_users", {}).get(transaction.device.device_id, [])
            if len(device_users) > 3:
                risk_score += 0.3
                reasons.append(f"Device shared by {len(device_users)} users")
            
            # Check 2: IP network - how many users from this IP?
            ip_address = transaction.device.ip_address
            if ip_address:
                ip_users = user_network.get("ip_to_users", {}).get(ip_address, [])
                if len(ip_users) > 5:
                    risk_score += 0.25
                    reasons.append(f"IP shared by {len(ip_users)} users")
            
            # Check 3: Merchant network - is this merchant suspicious?
            merchant_fraud_rate = user_network.get("merchant_fraud_rates", {}).get(transaction.merchant, 0.0)
            if merchant_fraud_rate > 0.2:  # More than 20% fraud rate
                risk_score += merchant_fraud_rate * 0.3
                reasons.append(f"Merchant has {merchant_fraud_rate*100}% fraud rate")
            
            # Check 4: Location network - unusual location cluster?
            location = transaction.location or "unknown"
            location_fraud_users = user_network.get("location_fraud_users", {}).get(location, [])
            if len(location_fraud_users) > 10:
                risk_score += 0.2
                reasons.append(f"Location linked to {len(location_fraud_users)} fraud cases")
            
            # Check 5: Device-Merchant combination
            device_merchant_key = f"{transaction.device.device_id}_{transaction.merchant}"
            device_merchant_txns = user_network.get("device_merchant_combos", {}).get(device_merchant_key, [])
            if len(device_merchant_txns) == 0:
                risk_score += 0.15
                reasons.append("Unusual device-merchant combination")
            
            risk_score = min(risk_score, 1.0)
            explanation = " | ".join(reasons) if reasons else "No network anomalies"
            
            logger.info(f"{self.name}: Score={risk_score}, Txn={transaction.transaction_id}")
            return round(risk_score, 3), explanation
            
        except Exception as e:
            logger.error(f"{self.name}: Failed - {str(e)}")
            raise