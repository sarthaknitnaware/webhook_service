from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.SubscriptionOut)
def create_sub(sub: schemas.SubscriptionCreate, db: Session = Depends(get_db)):
    return crud.create_subscription(db, sub)

@router.get("/{sub_id}", response_model=schemas.SubscriptionOut)
def read_sub(sub_id: int, db: Session = Depends(get_db)):
    obj = crud.get_subscription(db, sub_id)
    if not obj:
        raise HTTPException(404, "Not found")
    return obj

@router.get("/", response_model=list[schemas.SubscriptionOut])
def list_subs(db: Session = Depends(get_db)):
    return crud.list_subscriptions(db)

@router.put("/{sub_id}", response_model=schemas.SubscriptionOut)
def update_sub(sub_id: int, sub: schemas.SubscriptionCreate, db: Session = Depends(get_db)):
    return crud.update_subscription(db, sub_id, sub)

@router.delete("/{sub_id}", response_model=schemas.SubscriptionOut)
def delete_sub(sub_id: int, db: Session = Depends(get_db)):
    return crud.delete_subscription(db, sub_id)
