from pydantic import BaseModel, Field
from typing import Literal, Optional, Dict, Any

FrameworkLiteral = Literal["crewai", "langchain", "openai"]

class AgentBase(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    framework: FrameworkLiteral
    params: Optional[Dict[str, Any]] = None

class AgentCreate(AgentBase):
    pass

class AgentUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    framework: Optional[FrameworkLiteral] = None
    params: Optional[Dict[str, Any]] = None

class AgentOut(AgentBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
