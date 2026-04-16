from typing import Dict, Any, Tuple
from core.logger import logger
from core.constants import Decision
from agents.learning.feedback_loop import FeedbackLoop

class LearningAgent:
    """
    Continuously improves the fraud detection system using feedback from past decisions.
    Manages:
    - Feedback collection
    - Performance metrics
    - Retraining triggers
    - Model updates
    """
    
    def __init__(self):
        self.name = "learning_agent"
        self.feedback_loop = FeedbackLoop()
        self.model_version = "1.0"
        self.last_retrain_time = None
    
    def process_feedback(self, transaction_id: str, predicted_decision: Decision,
                        actual_decision: Decision, confidence: float, 
                        analyst_notes: str = "") -> Dict[str, Any]:
        """
        Processes feedback from analysts about model predictions.
        
        Args:
            transaction_id: Transaction ID
            predicted_decision: System's prediction
            actual_decision: Analyst's correction (if any)
            confidence: System's confidence score
            analyst_notes: Analyst's notes
            
        Returns:
            Feedback processing result
        """
        try:
            # Record feedback
            feedback = self.feedback_loop.record_feedback(
                transaction_id,
                predicted_decision,
                actual_decision,
                confidence,
                analyst_notes
            )
            
            # Check if prediction was correct
            is_correct = feedback["was_correct"]
            
            logger.info(f"{self.name}: Processed feedback for {transaction_id}, correct={is_correct}")
            
            return {
                "status": "feedback_recorded",
                "transaction_id": transaction_id,
                "was_correct": is_correct,
                "feedback_id": transaction_id,
            }
            
        except Exception as e:
            logger.error(f"{self.name}: Failed to process feedback - {str(e)}")
            raise
    
    def evaluate_model_performance(self) -> Dict[str, Any]:
        """
        Evaluates overall model performance based on accumulated feedback.
        
        Returns:
            Performance metrics dict
        """
        try:
            metrics = self.feedback_loop.get_accuracy_metrics()
            
            logger.info(f"{self.name}: Model performance - Accuracy={metrics.get('accuracy', 0)}")
            
            return metrics
            
        except Exception as e:
            logger.error(f"{self.name}: Failed to evaluate performance - {str(e)}")
            raise
    
    def check_retrain_requirements(self) -> Dict[str, Any]:
        """
        Checks if models need retraining based on performance.
        
        Returns:
            Retraining requirements dict with recommendations
        """
        try:
            retrain_info = self.feedback_loop.identify_retraining_triggers()
            
            if retrain_info["should_retrain"]:
                logger.warning(f"{self.name}: Retraining REQUIRED - Reasons: {retrain_info['trigger_reasons']}")
            else:
                logger.info(f"{self.name}: No retraining needed, accuracy={retrain_info.get('recent_accuracy', 0)}")
            
            return retrain_info
            
        except Exception as e:
            logger.error(f"{self.name}: Failed to check retrain requirements - {str(e)}")
            raise
    
    def get_learning_insights(self) -> Dict[str, Any]:
        """
        Provides insights from learned patterns.
        
        Returns:
            Dict with insights and recommendations
        """
        try:
            metrics = self.feedback_loop.get_accuracy_metrics()
            retrain_status = self.feedback_loop.identify_retraining_triggers()
            recent_feedback = self.feedback_loop.get_feedback_summary(limit=20)
            
            # Analyze patterns
            insights = {
                "model_version": self.model_version,
                "total_feedback_records": metrics.get("total_feedback", 0),
                "current_accuracy": metrics.get("accuracy", 0),
                "needs_retrain": retrain_status.get("should_retrain", False),
                "recent_errors": [
                    {
                        "transaction_id": fb["transaction_id"],
                        "predicted": fb["predicted_decision"],
                        "actual": fb["actual_decision"],
                    }
                    for fb in recent_feedback if not fb["was_correct"]
                ],
                "recommendations": self._generate_recommendations(metrics, retrain_status),
            }
            
            logger.info(f"{self.name}: Learning insights generated")
            
            return insights
            
        except Exception as e:
            logger.error(f"{self.name}: Failed to generate insights - {str(e)}")
            raise
    
    @staticmethod
    def _generate_recommendations(metrics: Dict[str, Any], retrain_info: Dict[str, Any]) -> list:
        """
        Generates recommendations based on metrics.
        
        Args:
            metrics: Performance metrics
            retrain_info: Retrain requirements
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        if retrain_info.get("should_retrain"):
            recommendations.append("Retrain models with new feedback data")
        
        if metrics.get("accuracy", 1.0) < 0.85:
            recommendations.append("Review model parameters - accuracy below 85%")
        
        if metrics.get("incorrect_predictions", 0) > 20:
            recommendations.append("Increase negative sample training data")
        
        if not recommendations:
            recommendations.append("System performing well - continue monitoring")
        
        return recommendations