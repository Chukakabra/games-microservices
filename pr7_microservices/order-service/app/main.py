from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uuid
import httpx
import os

from .database import Base, engine, get_db
from . import models

Base.metadata.create_all(bind=engine)

CATALOG_URL = os.getenv("CATALOG_URL", "http://127.0.0.1:8000")

app = FastAPI(title="Order Service")


class OrderCreate(BaseModel):
    client_id: str
    game_id: str
    delivery_address: str


class OrderResponse(BaseModel):
    id: str
    client_id: str
    game_id: str
    delivery_address: str
    total: int
    status: str


async def fetch_game(game_id: str) -> dict:
    """Вложенный вызов CatalogService."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CATALOG_URL}/games/{game_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Game not found in catalog")
        return response.json()


@app.post("/orders", response_model=OrderResponse)
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    game = await fetch_game(order.game_id)

    db_order = models.Order(
        id=str(uuid.uuid4()),
        client_id=order.client_id,
        game_id=order.game_id,
        delivery_address=order.delivery_address,
        total=game["base_price"],
        status="CREATED"
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return OrderResponse(
        id=db_order.id, client_id=db_order.client_id, game_id=db_order.game_id,
        delivery_address=db_order.delivery_address, total=db_order.total, status=db_order.status
    )


@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return OrderResponse(
        id=order.id, client_id=order.client_id, game_id=order.game_id,
        delivery_address=order.delivery_address, total=order.total, status=order.status
    )


@app.get("/orders", response_model=list[OrderResponse])
def list_orders(client_id: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Order)
    if client_id:
        query = query.filter(models.Order.client_id == client_id)
    return [
        OrderResponse(id=o.id, client_id=o.client_id, game_id=o.game_id,
                      delivery_address=o.delivery_address, total=o.total, status=o.status)
        for o in query.all()
    ]


@app.post("/orders/{order_id}/cancel", response_model=OrderResponse)
def cancel_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = "CANCELLED"
    db.commit()
    db.refresh(order)
    return OrderResponse(
        id=order.id, client_id=order.client_id, game_id=order.game_id,
        delivery_address=order.delivery_address, total=order.total, status=order.status
    )