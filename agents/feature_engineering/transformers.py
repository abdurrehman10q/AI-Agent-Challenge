from typing import Dict, Any
from datetime import datetime
import math

class FeatureTransformers:
    """
    Transforms raw transaction data into meaningful features.
    """
    
    @staticmethod
    def calculate_transaction_velocity(user_id: str, current_time: datetime, recent_transactions: list = None) -> float:
        """
        Calculates how many transactions a user made in the last hour.
        Higher velocity = higher risk
        """
        if recent_transactions is None:
            recent_transactions = []
        
        # Count transactions in last hour
        one_hour_ago = datetime.utcnow().timestamp() - 3600
        recent_count = sum(1 for txn in recent_transactions if txn.get("timestamp", 0) > one_hour_ago)
        
        # Normalize: 0-1 scale (10+ transactions = 1.0)
        velocity_score = min(recent_count / 10.0, 1.0)
        return round(velocity_score, 3)
    
    @staticmethod
    def calculate_geolocation_shift(previous_location: str, current_location: str) -> float:
        """
        Detects if user is in a new location.
        New location = higher risk
        """
        if not previous_location or not current_location:
            return 0.0
        
        if previous_location.lower() == current_location.lower():
            return 0.0  # Same location
        else:
            return 1.0  # New location detected
    
    @staticmethod
    def calculate_amount_deviation(amount: float, user_avg_amount: float = 100) -> float:
        """
        Calculates how much transaction amount deviates from user average.
        Large deviation = higher risk
        """
        if user_avg_amount == 0:
            return 0.5
        
        deviation = abs(amount - user_avg_amount) / user_avg_amount
        # Normalize: cap at 1.0
        return min(deviation, 1.0)
    
    @staticmethod
    def calculate_merchant_risk_score(merchant: str, merchant_category: str = "ecommerce") -> float:
        """
        Assigns risk score based on merchant category.
        High-risk categories: casino, crypto, foreign_atm
        """
        high_risk_categories = ["casino", "crypto", "foreign_atm", "money_transfer"]
        
        if merchant_category.lower() in high_risk_categories:
            return 0.8
        elif merchant_category.lower() in ["restaurant", "grocery", "gas"]:
            return 0.1
        else:
            return 0.3  # Default medium risk
    
    @staticmethod
    def calculate_time_of_day_risk(timestamp: datetime) -> float:
        """
        Higher risk during unusual hours (2 AM - 5 AM)
        """
        hour = timestamp.hour
        
        if 2 <= hour <= 5:
            return 0.7  # Unusual hours
        elif 22 <= hour or hour <= 6:
            return 0.4  # Late/early morning
        else:
            return 0.1  # Normal hours