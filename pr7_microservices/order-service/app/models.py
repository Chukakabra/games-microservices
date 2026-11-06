import uuid
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from .database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String, nullable=False)
    game_id = Column(String, nullable=False)
    delivery_address = Column(String, nullable=False)
    total = Column(Integer, nullable=False)
    status = Column(String, default="CREATED")
    created_at = Column(DateTime, default=datetime.utcnow)
