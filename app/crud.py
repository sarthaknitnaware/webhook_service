from sqlalchemy.orm import Session
from . import models, schemas

def get_subscription(db: Session, sub_id: int):
    return db.query(models.Subscription).filter(models.Subscription.id == sub_id).first()

def create_subscription(db: Session, sub: schemas.SubscriptionCreate):
    data = sub.dict()
    # convert HttpUrl to string
    data["target_url"] = str(data["target_url"])
    db_obj = models.Subscription(**data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def list_subscriptions(db: Session):
    return db.query(models.Subscription).all()

def update_subscription(db: Session, sub_id: int, sub: schemas.SubscriptionCreate):
    obj = get_subscription(db, sub_id)
    for k, v in sub.dict().items():
        # cast URL field back to string
        if k == "target_url":
            setattr(obj, k, str(v))
        else:
            setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

def delete_subscription(db: Session, sub_id: int):
    obj = get_subscription(db, sub_id)
    db.delete(obj); db.commit()
    return obj
