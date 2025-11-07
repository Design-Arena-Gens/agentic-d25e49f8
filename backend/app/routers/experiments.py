from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..auth.deps import get_current_user
from ..models.user import User
from ..models.agent import AgentConfig
from ..models.experiment import Experiment
from ..models.result import ExperimentResult
from ..schemas.experiment import ExperimentCreate, ExperimentOut, ExperimentResultOut
from ..services.agent_engine import AgentEngine

router = APIRouter(prefix="/experiments", tags=["experiments"]) 

@router.post("/", response_model=ExperimentOut)
def create_experiment(exp_in: ExperimentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    agent = db.query(AgentConfig).filter(AgentConfig.id == exp_in.agent_id, AgentConfig.owner_id == current_user.id).first()
    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")

    exp = Experiment(status="running", input_data=exp_in.input_data or {}, owner_id=current_user.id, agent_id=agent.id)
    db.add(exp)
    db.commit()
    db.refresh(exp)

    # Execute synchronously (stubbed)
    engine = AgentEngine(agent.framework, agent.params)
    result = engine.run(exp_in.input_data or {})

    # Persist result
    exp_result = ExperimentResult(experiment_id=exp.id, output_data={"output": result.get("output")}, metrics=result.get("metrics"))
    db.add(exp_result)
    exp.status = "completed"
    db.add(exp)
    db.commit()
    db.refresh(exp)

    return exp

@router.get("/{experiment_id}")
def get_experiment(experiment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    exp = db.query(Experiment).filter(Experiment.id == experiment_id, Experiment.owner_id == current_user.id).first()
    if not exp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiment not found")
    resp = {
        "id": exp.id,
        "status": exp.status,
        "agent_id": exp.agent_id,
        "owner_id": exp.owner_id,
        "input_data": exp.input_data,
    }
    if exp.result:
        resp["result"] = {
            "output_data": exp.result.output_data,
            "metrics": exp.result.metrics,
        }
    return resp
