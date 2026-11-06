import uuid
from sqlalchemy import Column, String, DateTime
from datetime import datetime
from .database import Base

class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = Column(String, nullable=False)
    courier_id = Column(String, nullable=False)
    address = Column(String, nullable=False)
    status = Column(String, default="COURIER_ASSIGNED")
    created_at = Column(DateTime, default=datetime.utcnow)
    delivered_at = Column(DateTime, nullable=True)
