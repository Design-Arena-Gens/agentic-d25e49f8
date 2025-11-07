from sqlalchemy import Column, Integer, String, JSON, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base

class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String(50), default="pending", nullable=False)
    input_data = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    owner = relationship("User", back_populates="experiments")

    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False, index=True)
    agent = relationship("AgentConfig", back_populates="experiments")

    result = relationship("ExperimentResult", back_populates="experiment", uselist=False, cascade="all, delete-orphan")
