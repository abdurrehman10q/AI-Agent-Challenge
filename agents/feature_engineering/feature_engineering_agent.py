from typing import Dict, Any
from core.logger import logger
from agents.feature_engineering.transformers import FeatureTransformers
from agents.ingestion.schemas import TransactionData

class FeatureEngineeringAgent:
    """
    Transforms raw transaction data into meaningful features.
    """
    
    def __init__(self):
        self.name = "feature_engineering_agent"
        self.transformers = FeatureTransformers()
    
    def execute(self, transaction: TransactionData, user_history: Dict[str, Any] = None) -> Dict[str, float]:
        """
        Extracts and transforms features from transaction data.
        
        Args:
            transaction: TransactionData object
            user_history: Historical data about user (optional)
            
        Returns:
            Dict of engineered features
        """
        if user_history is None:
            user_history = {}
        
        try:
            features = {
                "transaction_velocity": self.transformers.calculate_transaction_velocity(
                    transaction.user_id,
                    transaction.timestamp,
                    user_history.get("recent_transactions", [])
                ),
                "geolocation_shift": self.transformers.calculate_geolocation_shift(
                    user_history.get("last_location", ""),
                    transaction.location
                ),
                "amount_deviation": self.transformers.calculate_amount_deviation(
                    transaction.amount,
                    user_history.get("avg_transaction_amount", 100)
                ),
                "merchant_risk": self.transformers.calculate_merchant_risk_score(
                    transaction.merchant,
                    transaction.merchant_category
                ),
                "time_of_day_risk": self.transformers.calculate_time_of_day_risk(
                    transaction.timestamp
                ),
            }
            
            logger.info(f"{self.name}: Engineered {len(features)} features for txn {transaction.transaction_id}")
            return features
            
        except Exception as e:
            logger.error(f"{self.name}: Failed to engineer features - {str(e)}")
            raise