from typing import Dict, Any, List
from datetime import datetime
from core.logger import logger
from core.constants import Decision

class FeedbackLoop:
    """
    Manages feedback collection and model retraining signals.
    """
    
    def __init__(self):
        self.feedback_history: List[Dict[str, Any]] = []
    
    def record_feedback(self, transaction_id: str, predicted_decision: Decision, 
                       actual_decision: Decision, confidence: float, feedback_text: str = "") -> Dict[str, Any]:
        """
        Records feedback about a prediction.
        
        Args:
            transaction_id: Transaction ID
            predicted_decision: What the system predicted
            actual_decision: What actually happened (from analyst)
            confidence: System's confidence in prediction
            feedback_text: Analyst's notes
            
        Returns:
            Feedback record dict
        """
        feedback_record = {
            "transaction_id": transaction_id,
            "predicted_decision": predicted_decision,
            "actual_decision": actual_decision,
            "was_correct": predicted_decision == actual_decision,
            "confidence": confidence,
            "feedback_text": feedback_text,
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        self.feedback_history.append(feedback_record)
        
        logger.info(f"Feedback recorded: txn={transaction_id}, correct={feedback_record['was_correct']}")
        
        return feedback_record
    
    def get_accuracy_metrics(self) -> Dict[str, Any]:
        """
        Calculates accuracy metrics from feedback history.
        
        Returns:
            Dict with accuracy, precision, recall metrics
        """
        if not self.feedback_history:
            return {
                "total_feedback": 0,
                "accuracy": 0.0,
                "correct_predictions": 0,
                "incorrect_predictions": 0,
            }
        
        total = len(self.feedback_history)
        correct = sum(1 for fb in self.feedback_history if fb["was_correct"])
        incorrect = total - correct
        
        accuracy = correct / total if total > 0 else 0.0
        
        metrics = {
            "total_feedback": total,
            "correct_predictions": correct,
            "incorrect_predictions": incorrect,
            "accuracy": round(accuracy, 3),
            "precision": round(correct / total, 3) if total > 0 else 0.0,
        }
        
        logger.info(f"Accuracy metrics: {metrics}")
        
        return metrics
    
    def identify_retraining_triggers(self) -> Dict[str, Any]:
        """
        Identifies when models need retraining based on feedback.
        
        Returns:
            Dict with retraining recommendations
        """
        if len(self.feedback_history) < 10:
            return {"should_retrain": False, "reason": "Insufficient feedback data"}
        
        recent_feedback = self.feedback_history[-100:]  # Last 100 feedback records
        recent_accuracy = sum(1 for fb in recent_feedback if fb["was_correct"]) / len(recent_feedback)
        
        trigger_reasons = []
        should_retrain = False
        
        # Trigger 1: Accuracy dropped below 80%
        if recent_accuracy < 0.8:
            trigger_reasons.append(f"Accuracy dropped to {recent_accuracy:.2%}")
            should_retrain = True
        
        # Trigger 2: Too many false positives
        false_positives = sum(1 for fb in recent_feedback 
                            if fb["predicted_decision"] == Decision.BLOCK 
                            and fb["actual_decision"] != Decision.BLOCK)
        if false_positives > len(recent_feedback) * 0.3:
            trigger_reasons.append(f"High false positives: {false_positives}")
            should_retrain = True
        
        # Trigger 3: Too many false negatives
        false_negatives = sum(1 for fb in recent_feedback 
                             if fb["predicted_decision"] != Decision.BLOCK 
                             and fb["actual_decision"] == Decision.BLOCK)
        if false_negatives > len(recent_feedback) * 0.2:
            trigger_reasons.append(f"High false negatives: {false_negatives}")
            should_retrain = True
        
        return {
            "should_retrain": should_retrain,
            "recent_accuracy": round(recent_accuracy, 3),
            "trigger_reasons": trigger_reasons,
            "feedback_sample_size": len(recent_feedback),
        }
    
    def get_feedback_summary(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Gets summary of recent feedback.
        
        Args:
            limit: Number of recent records to return
            
        Returns:
            List of feedback records
        """
        return self.feedback_history[-limit:]