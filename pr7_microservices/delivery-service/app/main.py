from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from .database import Base, engine, get_db
from . import models

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Delivery Service")

class DeliveryCreate(BaseModel):
    order_id: str
    courier_id: str
    address: str

class DeliveryResponse(BaseModel):
    id: str
    order_id: str
    courier_id: str
    address: str
    status: str

@app.post("/deliveries", response_model=DeliveryResponse)
def create_delivery(delivery: DeliveryCreate, db: Session = Depends(get_db)):
    db_delivery = models.Delivery(
        id=str(uuid.uuid4()),
        order_id=delivery.order_id,
        courier_id=delivery.courier_id,
        address=delivery.address
    )
    db.add(db_delivery)
    db.commit()
    db.refresh(db_delivery)
    return DeliveryResponse(
        id=db_delivery.id, order_id=db_delivery.order_id,
        courier_id=db_delivery.courier_id, address=db_delivery.address,
        status=db_delivery.status
    )

@app.post("/deliveries/{delivery_id}/complete", response_model=DeliveryResponse)
def complete_delivery(delivery_id: str, db: Session = Depends(get_db)):
    delivery = db.query(models.Delivery).filter(models.Delivery.id == delivery_id).first()
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    delivery.status = "DELIVERED"
    delivery.delivered_at = datetime.utcnow()
    db.commit()
    db.refresh(delivery)
    return DeliveryResponse(
        id=delivery.id, order_id=delivery.order_id,
        courier_id=delivery.courier_id, address=delivery.address,
        status=delivery.status
    )

@app.get("/deliveries/{delivery_id}", response_model=DeliveryResponse)
def get_delivery(delivery_id: str, db: Session = Depends(get_db)):
    delivery = db.query(models.Delivery).filter(models.Delivery.id == delivery_id).first()
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return DeliveryResponse(
        id=delivery.id, order_id=delivery.order_id,
        courier_id=delivery.courier_id, address=delivery.address,
        status=delivery.status
    )

@app.get("/deliveries", response_model=list[DeliveryResponse])
def list_deliveries(order_id: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Delivery)
    if order_id:
        query = query.filter(models.Delivery.order_id == order_id)
    return [
        DeliveryResponse(id=d.id, order_id=d.order_id,
                         courier_id=d.courier_id, address=d.address, status=d.status)
        for d in query.all()
    ]