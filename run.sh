#!/bin/bash

echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
  source venv/Scripts/activate
else
  source venv/bin/activate
fi

echo "Starting backend..."
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload &
BACKEND_PID=$!

echo "Starting frontend..."
cd frontend || { echo "Frontend folder not found"; exit 1; }
npm start &
FRONTEND_PID=$!

wait $BACKEND_PID $FRONTEND_PID