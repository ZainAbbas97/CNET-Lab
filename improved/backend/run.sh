#!/bin/bash
# Startup script for the backend server

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "Please edit .env file with your configuration"
fi

# Run the server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

