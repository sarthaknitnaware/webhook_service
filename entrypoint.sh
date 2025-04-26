#!/usr/bin/env bash

# 1. Start Celery worker in background
celery -A app.utils worker --loglevel=info &

# 2. Launch FastAPI with Uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000
