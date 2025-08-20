#!/bin/bash

# Apply database migrations
alembic upgrade head

# Start FastAPI server
uvicorn main:app --host 0.0.0.0 --port $PORT
