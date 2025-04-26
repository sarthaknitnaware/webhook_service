import os
from celery import Celery
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import crud, models
import httpx

# Configure Celery
celery = Celery(
    __name__,
    broker=os.getenv("REDIS_URL"),
    backend=os.getenv("REDIS_URL"),
)

@celery.task(bind=True, max_retries=5)
def deliver_webhook(self, subscription_id: int, webhook_id: str, payload: dict):
    db: Session = SessionLocal()
    sub = crud.get_subscription(db, subscription_id)
    try:
        resp = httpx.post(sub.target_url, json=payload, timeout=10)
        status = "success" if resp.status_code < 300 else "failed"
        log = models.DeliveryLog(
            subscription_id=subscription_id,
            webhook_id=webhook_id,
            attempt=self.request.retries + 1,
            status=status,
            http_status=resp.status_code,
            error=None if status=="success" else resp.text[:200]
        )
        db.add(log); db.commit()
        if status == "failed":
            raise Exception(f"HTTP {resp.status_code}")
    except Exception as exc:
        # Record failure and retry
        log = models.DeliveryLog(
            subscription_id=subscription_id,
            webhook_id=webhook_id,
            attempt=self.request.retries + 1,
            status="failed",
            http_status=None,
            error=str(exc)[:200]
        )
        db.add(log); db.commit()
        delay = 10 * (2 ** self.request.retries)
        raise self.retry(exc=exc, countdown=delay)
    finally:
        db.close()
