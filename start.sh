#!/bin/bash

# Start backend
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Start frontend
cd ../frontend
npm run dev &
FRONTEND_PID=$!

# Handle shutdown
trap 'kill $BACKEND_PID $FRONTEND_PID' EXIT

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
