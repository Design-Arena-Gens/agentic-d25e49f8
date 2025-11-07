from sqlalchemy import Column, Integer, JSON, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base

class ExperimentResult(Base):
    __tablename__ = "experiment_results"

    id = Column(Integer, primary_key=True, index=True)
    output_data = Column(JSON, nullable=True)
    metrics = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    experiment_id = Column(Integer, ForeignKey("experiments.id"), nullable=False, unique=True)
    experiment = relationship("Experiment", back_populates="result")
