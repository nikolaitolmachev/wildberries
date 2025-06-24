#!/bin/bash

echo "Starting backend..."
cd backend || { echo "Backend folder not found"; exit 1; }

uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload &
BACKEND_PID=$!

cd ../frontend || { echo "Frontend folder not found"; exit 1; }

echo "Starting frontend..."
npm start &
FRONTEND_PID=$!

wait $BACKEND_PID $FRONTEND_PID