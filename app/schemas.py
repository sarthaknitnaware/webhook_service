from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict
from datetime import datetime

class SubscriptionCreate(BaseModel):
    target_url: HttpUrl
    secret: Optional[str]
    event_types: Optional[list[str]] = None

class SubscriptionOut(SubscriptionCreate):
    id: int
    class Config:
        orm_mode = True

class IngestPayload(BaseModel):
    data: Dict

class DeliveryLogOut(BaseModel):
    id: int
    subscription_id: int
    webhook_id: str
    timestamp: datetime
    attempt: int
    status: str
    http_status: Optional[int]
    error: Optional[str]
    class Config:
        orm_mode = True
