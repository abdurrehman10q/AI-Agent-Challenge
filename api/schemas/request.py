from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime

class DeviceInfo(BaseModel):
    device_id: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

class TransactionRequest(BaseModel):
    transaction_id: str
    user_id: str
    amount: float = Field(gt=0)
    currency: str = "USD"
    merchant: str
    merchant_category: Optional[str] = "ecommerce"
    location: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    device: DeviceInfo
    metadata: Optional[Dict] = {}