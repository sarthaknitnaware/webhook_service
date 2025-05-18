#!/usr/bin/env bash

# Wait for the database to be ready
/wait-for-db.sh

# Start Celery worker in background
celery -A app.utils worker --loglevel=info &

# Launch FastAPI with Uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000

