from sqlalchemy import Column, Integer, String, JSON, DateTime, func, Boolean
from sqlalchemy.orm import relationship
from ..core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    preferences = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    agents = relationship("AgentConfig", back_populates="owner", cascade="all, delete-orphan")
    experiments = relationship("Experiment", back_populates="owner")
