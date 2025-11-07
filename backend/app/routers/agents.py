from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..core.database import get_db
from ..auth.deps import get_current_user
from ..models.agent import AgentConfig
from ..schemas.agent import AgentCreate, AgentUpdate, AgentOut
from ..models.user import User

router = APIRouter(prefix="/agents", tags=["agents"]) 

@router.post("/", response_model=AgentOut)
def create_agent(agent_in: AgentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if agent_in.framework not in {"crewai", "langchain", "openai"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported framework")
    agent = AgentConfig(
        name=agent_in.name,
        framework=agent_in.framework,
        params=agent_in.params or {},
        owner_id=current_user.id,
    )
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent

@router.get("/", response_model=List[AgentOut])
def list_agents(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    agents = db.query(AgentConfig).filter(AgentConfig.owner_id == current_user.id).all()
    return agents

@router.get("/{agent_id}", response_model=AgentOut)
def get_agent(agent_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    agent = db.query(AgentConfig).filter(AgentConfig.id == agent_id, AgentConfig.owner_id == current_user.id).first()
    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    return agent

@router.put("/{agent_id}", response_model=AgentOut)
def update_agent(agent_id: int, agent_upd: AgentUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    agent = db.query(AgentConfig).filter(AgentConfig.id == agent_id, AgentConfig.owner_id == current_user.id).first()
    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    if agent_upd.name is not None:
        agent.name = agent_upd.name
    if agent_upd.framework is not None:
        if agent_upd.framework not in {"crewai", "langchain", "openai"}:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported framework")
        agent.framework = agent_upd.framework
    if agent_upd.params is not None:
        agent.params = agent_upd.params
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent

@router.delete("/{agent_id}")
def delete_agent(agent_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    agent = db.query(AgentConfig).filter(AgentConfig.id == agent_id, AgentConfig.owner_id == current_user.id).first()
    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    db.delete(agent)
    db.commit()
    return {"detail": "Deleted"}
