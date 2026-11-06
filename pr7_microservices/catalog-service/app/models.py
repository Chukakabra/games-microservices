import uuid
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from .database import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    base_price = Column(Integer, nullable=False)
    status = Column(String, default="AVAILABLE")
    created_at = Column(DateTime, default=datetime.utcnow)
