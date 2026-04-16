from typing import Dict, Any, Tuple
from core.logger import logger
from agents.ingestion.schemas import TransactionData
import random

class AnomalyDetectionAgent:
    """
    Detects anomalies using statistical/ML models (Isolation Forest, etc).
    """
    
    def __init__(self):
        self.name = "anomaly_detection_agent"
    
    def execute(self, transaction: TransactionData, features: Dict[str, float] = None) -> Tuple[float, str]:
        """
        Detects anomalies in transaction data.
        
        Args:
            transaction: TransactionData object
            features: Engineered features from Feature Engineering Agent
            
        Returns:
            Tuple of (risk_score, explanation)
        """
        if features is None:
            features = {}
        
        try:
            # For now: weighted combination of features
            # Member 1 will replace this with actual ML model (Isolation Forest, XGBoost)
            
            risk_score = 0.0
            reasons = []
            
            # Use engineered features
            if "transaction_velocity" in features:
                vel = features["transaction_velocity"]
                if vel > 0.5:
                    risk_score += vel * 0.3
                    reasons.append(f"High velocity anomaly: {vel}")
            
            if "amount_deviation" in features:
                dev = features["amount_deviation"]
                if dev > 0.5:
                    risk_score += dev * 0.3
                    reasons.append(f"Amount deviation: {dev}")
            
            if "geolocation_shift" in features:
                geo = features["geolocation_shift"]
                if geo > 0.5:
                    risk_score += geo * 0.2
                    reasons.append("Unusual geolocation")
            
            # TODO: Replace with actual Isolation Forest model from Member 1
            # model_score = isolation_forest.predict(features)
            # risk_score = model_score
            
            risk_score = min(risk_score, 1.0)
            explanation = " | ".join(reasons) if reasons else "No anomalies detected"
            
            logger.info(f"{self.name}: Score={risk_score}, Txn={transaction.transaction_id}")
            return round(risk_score, 3), explanation
            
        except Exception as e:
            logger.error(f"{self.name}: Failed - {str(e)}")
            raise