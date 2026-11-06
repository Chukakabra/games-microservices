from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from .database import Base, engine, get_db
from . import models

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Warehouse Service")

class SupplyCreate(BaseModel):
    game_id: str
    qty: int
    supplier: str

class SupplyResponse(BaseModel):
    id: str
    game_id: str
    qty: int
    supplier: str
    status: str

@app.post("/supplies", response_model=SupplyResponse)
def create_supply(supply: SupplyCreate, db: Session = Depends(get_db)):
    db_supply = models.Supply(
        id=str(uuid.uuid4()),
        game_id=supply.game_id,
        qty=supply.qty,
        supplier=supply.supplier
    )
    db.add(db_supply)
    db.commit()
    db.refresh(db_supply)
    return SupplyResponse(
        id=db_supply.id, game_id=db_supply.game_id,
        qty=db_supply.qty, supplier=db_supply.supplier, status=db_supply.status
    )

@app.post("/supplies/{supply_id}/receive", response_model=SupplyResponse)
def receive_supply(supply_id: str, db: Session = Depends(get_db)):
    supply = db.query(models.Supply).filter(models.Supply.id == supply_id).first()
    if not supply:
        raise HTTPException(status_code=404, detail="Supply not found")
    supply.status = "RECEIVED"
    supply.received_at = datetime.utcnow()
    db.commit()
    db.refresh(supply)
    return SupplyResponse(
        id=supply.id, game_id=supply.game_id,
        qty=supply.qty, supplier=supply.supplier, status=supply.status
    )

@app.get("/supplies/{supply_id}", response_model=SupplyResponse)
def get_supply(supply_id: str, db: Session = Depends(get_db)):
    supply = db.query(models.Supply).filter(models.Supply.id == supply_id).first()
    if not supply:
        raise HTTPException(status_code=404, detail="Supply not found")
    return SupplyResponse(
        id=supply.id, game_id=supply.game_id,
        qty=supply.qty, supplier=supply.supplier, status=supply.status
    )

@app.get("/supplies", response_model=list[SupplyResponse])
def list_supplies(game_id: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Supply)
    if game_id:
        query = query.filter(models.Supply.game_id == game_id)
    return [
        SupplyResponse(id=s.id, game_id=s.game_id, qty=s.qty,
                       supplier=s.supplier, status=s.status)
        for s in query.all()
    ]