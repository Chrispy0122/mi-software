from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from backend.app.core.database import get_session
from backend.app.modules.crm.models import Client, ClientProject

router = APIRouter(prefix="/crm", tags=["crm"])

# --- Clients ---

@router.post("/clients", response_model=Client)
def create_client(client: Client, session: Session = Depends(get_session)):
    session.add(client)
    session.commit()
    session.refresh(client)
    return client

@router.get("/clients", response_model=List[Client])
def read_clients(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    clients = session.exec(select(Client).offset(skip).limit(limit)).all()
    return clients

@router.get("/clients/{client_id}", response_model=Client)
def read_client(client_id: int, session: Session = Depends(get_session)):
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

# --- Projects ---

@router.post("/projects", response_model=ClientProject)
def create_project(project: ClientProject, session: Session = Depends(get_session)):
    try:
        session.add(project)
        session.commit()
        session.refresh(project)
        return project
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating project: {str(e)}")

@router.get("/projects", response_model=List[ClientProject])
def read_projects(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    projects = session.exec(select(ClientProject).offset(skip).limit(limit)).all()
    return projects

@router.get("/projects/{project_id}", response_model=ClientProject)
def read_project(project_id: int, session: Session = Depends(get_session)):
    project = session.get(ClientProject, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
