from pydantic import BaseModel
from typing import Optional, Dict, Any

class ExperimentCreate(BaseModel):
    agent_id: int
    input_data: Optional[Dict[str, Any]] = None

class ExperimentOut(BaseModel):
    id: int
    status: str
    agent_id: int
    owner_id: int
    input_data: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

class ExperimentResultOut(BaseModel):
    experiment_id: int
    output_data: Optional[Dict[str, Any]]
    metrics: Optional[Dict[str, Any]]
