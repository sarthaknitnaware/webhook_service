from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import database, models, schemas

router = APIRouter(tags=["status"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/status/{webhook_id}", response_model=list[schemas.DeliveryLogOut])
def get_status(webhook_id: str, db: Session = Depends(get_db)):
    logs = db.query(models.DeliveryLog).filter(models.DeliveryLog.webhook_id == webhook_id).all()
    if not logs:
        raise HTTPException(404, "Webhook ID not found")
    return logs

@router.get("/logs/{sub_id}", response_model=list[schemas.DeliveryLogOut])
def get_logs(sub_id: int, db: Session = Depends(get_db)):
    return (
      db.query(models.DeliveryLog)
        .filter(models.DeliveryLog.subscription_id == sub_id)
        .order_by(models.DeliveryLog.timestamp.desc())
        .limit(20)
        .all()
    )
