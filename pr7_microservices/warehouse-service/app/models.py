import uuid
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from .database import Base

class Supply(Base):
    __tablename__ = "supplies"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    game_id = Column(String, nullable=False)
    qty = Column(Integer, nullable=False)
    supplier = Column(String, nullable=False)
    status = Column(String, default="EXPECTED")
    created_at = Column(DateTime, default=datetime.utcnow)
    received_at = Column(DateTime, nullable=True)
