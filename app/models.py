from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import func
from .database import Base

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    target_url = Column(Text, nullable=False)
    secret = Column(String, nullable=True)
    event_types = Column(ARRAY(String), nullable=True) # stores list of ["order.created", "user.updated"], etc.

class DeliveryLog(Base):
    __tablename__ = "delivery_logs"
    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=False)
    webhook_id = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    attempt = Column(Integer, nullable=False)
    status = Column(String, nullable=False)   # "success" or "failed"
    http_status = Column(Integer, nullable=True)
    error = Column(Text, nullable=True)
