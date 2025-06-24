#!/bin/bash

set -e

echo "=== Building backend ==="

if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
  echo "Error: Python is not installed or not in PATH"
  exit 1
fi

if command -v python3 &> /dev/null; then
  PYTHON_CMD=python3
else
  PYTHON_CMD=python
fi

activate_venv() {
  if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
  else
    source venv/bin/activate
  fi
}

if [ -d "venv" ]; then
  echo "Activating existing virtual environment..."
  activate_venv
else
  echo "Virtual environment not found, creating..."
  $PYTHON_CMD -m venv venv
  activate_venv
fi

if [ -f "requirements.txt" ]; then
  echo "Installing backend dependencies..."
  pip install --upgrade pip
  pip install -r requirements.txt
else
  echo "Warning: requirements.txt not found, skipping backend dependencies installation"
fi

echo "=== Building frontend ==="

if [ ! -d "frontend" ]; then
  echo "Error: Frontend folder not found"
  exit 1
fi

cd frontend

if ! command -v node &> /dev/null; then
  echo "Error: Node.js is not installed or not in PATH"
  exit 1
fi

if ! command -v npm &> /dev/null; then
  echo "Error: npm is not installed or not in PATH"
  exit 1
fi

echo "Installing frontend dependencies..."
npm install

echo "Building frontend..."
npm run build

cd ..

echo "=== Build completed successfully ==="