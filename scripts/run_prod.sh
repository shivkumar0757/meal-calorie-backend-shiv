#!/bin/bash
# Run application in PROD profile (PostgreSQL)
export ENVIRONMENT=prod
echo "🚀 Starting Calory Counter API in PROD mode (PostgreSQL)"
echo "📁 Profile: PROD"
echo "🗄️  Database: PostgreSQL (Production)"
echo "⚡ Rate Limit: 60/min"
echo "🌐 Server: http://localhost:8000"
echo ""
echo "⚠️  WARNING: Ensure production secrets are configured!"
uvicorn main:app --host 0.0.0.0 --port 8000
