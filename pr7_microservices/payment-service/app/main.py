from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
import httpx
import os

from .database import Base, engine, get_db
from . import models

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Payment Service")

CLIENT_URL = os.getenv("CLIENT_URL", "http://127.0.0.1:8002")

class PaymentCreate(BaseModel):
    order_id: str
    client_id: str
    amount: int

class PaymentResponse(BaseModel):
    id: str
    order_id: str
    client_id: str
    amount: int
    status: str

async def fetch_client(client_id: str) -> dict:
    """Вложенный вызов ClientService для проверки статуса клиента."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CLIENT_URL}/clients/{client_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Client not found")
        return response.json()

@app.post("/payments", response_model=PaymentResponse)
async def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    client = await fetch_client(payment.client_id)
    if client["status"] == "BLOCKED":
        raise HTTPException(status_code=403, detail="Client is blocked")

    db_payment = models.Payment(
        id=str(uuid.uuid4()),
        order_id=payment.order_id,
        client_id=payment.client_id,
        amount=payment.amount,
        status="PENDING"
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return PaymentResponse(
        id=db_payment.id, order_id=db_payment.order_id, client_id=db_payment.client_id,
        amount=db_payment.amount, status=db_payment.status
    )

@app.post("/payments/{payment_id}/pay", response_model=PaymentResponse)
def pay(payment_id: str, db: Session = Depends(get_db)):
    payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    payment.status = "PAID"
    payment.paid_at = datetime.utcnow()
    db.commit()
    db.refresh(payment)
    return PaymentResponse(
        id=payment.id, order_id=payment.order_id, client_id=payment.client_id,
        amount=payment.amount, status=payment.status
    )

@app.get("/payments/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return PaymentResponse(
        id=payment.id, order_id=payment.order_id, client_id=payment.client_id,
        amount=payment.amount, status=payment.status
    )

@app.get("/payments", response_model=list[PaymentResponse])
def list_payments(client_id: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Payment)
    if client_id:
        query = query.filter(models.Payment.client_id == client_id)
    return [
        PaymentResponse(id=p.id, order_id=p.order_id, client_id=p.client_id,
                        amount=p.amount, status=p.status)
        for p in query.all()
    ]