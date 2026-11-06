from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from .database import Base, engine, get_db
from . import models

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Notification Service")

class NotificationCreate(BaseModel):
    client_id: str
    channel: str
    text: str

class NotificationResponse(BaseModel):
    id: str
    client_id: str
    channel: str
    text: str
    status: str

@app.post("/notifications", response_model=NotificationResponse)
def create_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
    if notification.channel not in ["sms", "email", "push"]:
        raise HTTPException(status_code=400, detail="Channel must be sms, email or push")
    db_notif = models.Notification(
        id=str(uuid.uuid4()),
        client_id=notification.client_id,
        channel=notification.channel,
        text=notification.text
    )
    db.add(db_notif)
    db.commit()
    db.refresh(db_notif)
    return NotificationResponse(
        id=db_notif.id, client_id=db_notif.client_id,
        channel=db_notif.channel, text=db_notif.text, status=db_notif.status
    )

@app.post("/notifications/{notification_id}/mark-sent", response_model=NotificationResponse)
def mark_sent(notification_id: str, db: Session = Depends(get_db)):
    notif = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    notif.status = "SENT"
    notif.sent_at = datetime.utcnow()
    db.commit()
    db.refresh(notif)
    return NotificationResponse(
        id=notif.id, client_id=notif.client_id,
        channel=notif.channel, text=notif.text, status=notif.status
    )

@app.get("/notifications/{notification_id}", response_model=NotificationResponse)
def get_notification(notification_id: str, db: Session = Depends(get_db)):
    notif = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    return NotificationResponse(
        id=notif.id, client_id=notif.client_id,
        channel=notif.channel, text=notif.text, status=notif.status
    )

@app.get("/notifications", response_model=list[NotificationResponse])
def list_notifications(client_id: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Notification)
    if client_id:
        query = query.filter(models.Notification.client_id == client_id)
    return [
        NotificationResponse(id=n.id, client_id=n.client_id,
                             channel=n.channel, text=n.text, status=n.status)
        for n in query.all()
    ]