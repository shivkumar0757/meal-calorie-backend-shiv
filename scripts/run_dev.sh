#!/bin/bash
# Run application in DEV profile (SQLite)
export ENVIRONMENT=dev
echo "🚀 Starting Calory Counter API in DEV mode (SQLite)"
echo "📁 Profile: DEV"
echo "🗄️  Database: SQLite"
echo "⚡ Rate Limit: 1000/min"
echo "🌐 Server: http://localhost:8000"
echo ""
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
