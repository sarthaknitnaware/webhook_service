import uuid
from fastapi import APIRouter, Depends, HTTPException, Header, Request
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
async def ingest(
    sub_id: int,
    request: Request,
    payload: schemas.IngestPayload,
    db: Session = Depends(get_db),
    signature: str = Header(None, convert_underscores=False),
):
    sub = crud.get_subscription(db, sub_id)
    if not sub:
        raise HTTPException(404, "Subscription not found")
	
    # --- Signature verification ---
    if sub.secret:
        raw = await request.body()
        import hmac, hashlib
        # header format: "sha256=<hex>"
        try:
            algo, sent_sig = signature.split("=", 1)
        except:
            raise HTTPException(400, "Invalid signature header")
        if algo != "sha256":
            raise HTTPException(400, "Unsupported signature algorithm")
        mac = hmac.new(sub.secret.encode(), raw, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(mac, sent_sig):
            raise HTTPException(401, "Invalid signature")
    # ------------------------------

    # Before queueing:
    # --- Event type filtering ---
    # client must send X-Event-Type header:
    event_type = request.headers.get("X-Event-Type")
    if sub.event_types:
        if not event_type or event_type not in sub.event_types:
            # silently ignore or return 204 No Content
            return {}
    # ------------------------------

    webhook_id = str(uuid.uuid4())
    utils.deliver_webhook.delay(sub_id, webhook_id, payload.data)
    return {"webhook_id": webhook_id}
