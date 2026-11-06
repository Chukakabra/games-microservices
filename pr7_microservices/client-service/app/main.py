from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uuid

from .database import Base, engine, get_db
from . import models

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Client Service")

class ClientCreate(BaseModel):
    email: str
    display_name: str

class ClientResponse(BaseModel):
    id: str
    email: str
    display_name: str
    bonus_balance: int
    status: str

@app.post("/clients", response_model=ClientResponse)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    if db.query(models.Client).filter(models.Client.email == client.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    db_client = models.Client(
        id=str(uuid.uuid4()),
        email=client.email,
        display_name=client.display_name
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return ClientResponse(
        id=db_client.id, email=db_client.email, display_name=db_client.display_name,
        bonus_balance=db_client.bonus_balance, status=db_client.status
    )

@app.get("/clients/{client_id}", response_model=ClientResponse)
def get_client(client_id: str, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return ClientResponse(
        id=client.id, email=client.email, display_name=client.display_name,
        bonus_balance=client.bonus_balance, status=client.status
    )

@app.get("/clients", response_model=list[ClientResponse])
def list_clients(db: Session = Depends(get_db)):
    return [
        ClientResponse(id=c.id, email=c.email, display_name=c.display_name,
                       bonus_balance=c.bonus_balance, status=c.status)
        for c in db.query(models.Client).all()
    ]

@app.post("/clients/{client_id}/bonus", response_model=ClientResponse)
def add_bonus(client_id: str, amount: int, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    client.bonus_balance += amount
    db.commit()
    db.refresh(client)
    return ClientResponse(
        id=client.id, email=client.email, display_name=client.display_name,
        bonus_balance=client.bonus_balance, status=client.status
    )