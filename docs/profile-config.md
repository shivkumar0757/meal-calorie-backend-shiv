# 🔧 Profile-Based Configuration Guide

## Overview

The Calory Counter API now supports **profile-based configuration** for different environments:
- **DEV**: Development with SQLite (fast, no setup)
- **LOCAL**: Local development with PostgreSQL (production-like)
- **PROD**: Production with PostgreSQL (secure settings)

## 📂 Configuration Files

```
.env.dev      # Development profile (SQLite)
.env.local    # Local profile (PostgreSQL)  
.env.prod     # Production profile (PostgreSQL)
```

## 🚀 Running with Profiles

### Method 1: Environment Variable
```bash
# DEV profile (SQLite)
ENVIRONMENT=dev uvicorn main:app --reload

# LOCAL profile (PostgreSQL)
ENVIRONMENT=local uvicorn main:app --reload

# PROD profile (PostgreSQL)
ENVIRONMENT=prod uvicorn main:app
```

### Method 2: Convenience Scripts
```bash
# Development
./scripts/run_dev.sh

# Local PostgreSQL
./scripts/run_local.sh

# Production
./scripts/run_prod.sh
```

## 🗄️ Database Configuration

### DEV Profile (Default)
- **Database**: SQLite (`app_dev.db`)
- **Rate Limit**: 1000/min (generous for testing)
- **JWT Expiry**: 60 minutes
- **Perfect for**: Development, testing, quick prototyping

### LOCAL Profile
- **Database**: PostgreSQL (`mealcalorie`)
- **Rate Limit**: 100/min
- **JWT Expiry**: 30 minutes  
- **Perfect for**: Production-like local testing

### PROD Profile
- **Database**: PostgreSQL (`mealcalorie_prod`)
- **Rate Limit**: 60/min (strict)
- **JWT Expiry**: 15 minutes (secure)
- **Perfect for**: Production deployment

## 📊 Profile Comparison

| Feature | DEV | LOCAL | PROD |
|---------|-----|-------|------|
| Database | SQLite | PostgreSQL | PostgreSQL |
| Setup Required | ❌ None | ✅ PostgreSQL | ✅ PostgreSQL + Secrets |
| Rate Limit | 1000/min | 100/min | 60/min |
| JWT Expiry | 60 min | 30 min | 15 min |
| Auto-reload | ✅ Yes | ✅ Yes | ❌ No |
| Security | Basic | Medium | High |

## 🔒 Security by Profile

### DEV Profile
- Basic JWT secret
- Generous rate limits
- Long token expiry
- **⚠️ NOT for production**

### LOCAL Profile  
- Stronger JWT secret
- Moderate rate limits
- Standard token expiry
- **✅ Good for local testing**

### PROD Profile
- **⚠️ CHANGE ALL SECRETS**
- Strict rate limits
- Short token expiry
- **✅ Production ready**

## 🛠️ PostgreSQL Setup

### 1. Start PostgreSQL (if using LOCAL/PROD)
```bash
brew services start postgresql@16
```

### 2. Create Database & User
```bash
createdb mealcalorie
psql mealcalorie -c "CREATE USER meal_user WITH PASSWORD 'dev_password';"
psql mealcalorie -c "GRANT ALL PRIVILEGES ON DATABASE mealcalorie TO meal_user;"
```

### 3. Verify Connection
```bash
ENVIRONMENT=local python -c "from src.config.settings import settings; print(f'Database: {settings.effective_database_url}')"
```

## 🧪 Testing with Profiles

### Run Tests (always uses in-memory SQLite)
```bash
pytest  # Automatically uses test database
```

### Test Specific Profile
```bash
# Test DEV profile
ENVIRONMENT=dev python -c "from main import app; print('DEV OK')"

# Test LOCAL profile  
ENVIRONMENT=local python -c "from main import app; print('LOCAL OK')"
```

## 🎯 Quick Start

### For Development (Recommended)
```bash
# Uses SQLite, no setup required
./scripts/run_dev.sh
```

### For Production Testing  
```bash
# Uses PostgreSQL, requires setup
./scripts/run_local.sh
```

## 📝 Notes

- **Default**: DEV profile if no `ENVIRONMENT` is set
- **Auto-detection**: App automatically loads correct `.env.*` file
- **Fallback**: Uses main `.env` if profile file doesn't exist
- **Testing**: Always uses in-memory SQLite regardless of profile
- **Logging**: Shows which profile and database type on startup

**Perfect for different development stages while keeping the same codebase!** 🚀
