from fastapi import FastAPI
from .database import Base, engine
from .api import subscriptions, ingest, status

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Webhook Delivery Service")

app.include_router(subscriptions.router)
app.include_router(ingest.router)
app.include_router(status.router)
