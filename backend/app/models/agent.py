from sqlalchemy import Column, Integer, String, JSON, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base

class AgentConfig(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    framework = Column(String(50), nullable=False)  # crewai | langchain | openai
    params = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    owner = relationship("User", back_populates="agents")

    experiments = relationship("Experiment", back_populates="agent", cascade="all, delete-orphan")
