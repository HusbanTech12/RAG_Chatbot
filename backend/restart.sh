#!/bin/bash
# Restart script for backend with Gemini

echo "🔄 Restarting RAG Chatbot Backend with Gemini..."

# Stop existing backend
echo "Stopping existing backend..."
pkill -f "fastapi dev main.py" || echo "No existing process found"
sleep 2

# Navigate to backend directory
cd "$(dirname "$0")"

# Activate virtual environment and start
echo "Starting backend on port 8001..."
.venv/bin/fastapi dev main.py --host 0.0.0.0 --port 8001

echo "✅ Backend started with Gemini!"
echo "📍 API: http://localhost:8001"
echo "📚 Docs: http://localhost:8001/docs"
