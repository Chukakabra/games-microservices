import uuid
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from .database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String, nullable=False)
    game_id = Column(String, nullable=False)
    text = Column(String, nullable=False)
    rating = Column(Integer, default=0)
    status = Column(String, default="PUBLISHED")
    created_at = Column(DateTime, default=datetime.utcnow)
