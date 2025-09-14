#!/bin/bash
# Run application in LOCAL profile (PostgreSQL)
export ENVIRONMENT=local
echo "🚀 Starting Calory Counter API in LOCAL mode (PostgreSQL)"
echo "📁 Profile: LOCAL"
echo "🗄️  Database: PostgreSQL"
echo "⚡ Rate Limit: 100/min"
echo "🌐 Server: http://localhost:8000"
echo ""
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
