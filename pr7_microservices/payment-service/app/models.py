import uuid
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from .database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = Column(String, nullable=False)
    client_id = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    status = Column(String, default="PENDING")
    created_at = Column(DateTime, default=datetime.utcnow)
    paid_at = Column(DateTime, nullable=True)
