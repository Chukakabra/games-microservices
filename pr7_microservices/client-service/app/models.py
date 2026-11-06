import uuid
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from .database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    display_name = Column(String, nullable=False)
    bonus_balance = Column(Integer, default=0)
    status = Column(String, default="ACTIVE")
    created_at = Column(DateTime, default=datetime.utcnow)
