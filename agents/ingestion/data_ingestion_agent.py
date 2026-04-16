from typing import Dict, Any
from core.logger import logger
from agents.ingestion.schemas import TransactionData

class DataIngestionAgent:
    """
    Ingests and validates raw transaction data.
    """
    
    def __init__(self):
        self.name = "data_ingestion_agent"
    
    def execute(self, transaction_dict: Dict[str, Any]) -> TransactionData:
        """
        Validates and ingests transaction data.
        
        Args:
            transaction_dict: Raw transaction data
            
        Returns:
            TransactionData: Validated transaction object
        """
        try:
            transaction = TransactionData(**transaction_dict)
            logger.info(f"{self.name}: Ingested transaction {transaction.transaction_id}")
            return transaction
        except Exception as e:
            logger.error(f"{self.name}: Failed to ingest - {str(e)}")
            raise