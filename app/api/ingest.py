import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, crud, utils

router = APIRouter(tags=["ingest"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/ingest/{sub_id}", status_code=202)
def ingest(sub_id: int, payload: schemas.IngestPayload, db: Session = Depends(get_db)):
    sub = crud.get_subscription(db, sub_id)
    if not sub:
        raise HTTPException(404, "Subscription not found")
    webhook_id = str(uuid.uuid4())
    utils.deliver_webhook.delay(sub_id, webhook_id, payload.data)
    return {"webhook_id": webhook_id}
