# Environment Configuration

## 📌 Overview

This document outlines the environment variables required for the Meal Calorie Backend application.

---

## 🔧 Environment Variables

### Required Variables

Create a `.env` file in the project root with the following variables:

```bash
# USDA FoodData Central API Key
USDA_API_KEY=your-usda-api-key-here

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/mealcalorie

# JWT Configuration
JWT_SECRET=your-super-secure-jwt-secret-key-here-change-this-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Configuration - Original Requirement: 15 requests per minute from same IP
API_RATE_LIMIT=15  # requests per minute per IP address

# Cache Configuration  
CACHE_TTL=3600  # Cache TTL in seconds (1 hour)

# Environment
ENVIRONMENT=development

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

---

## 🚀 Quick Setup

### Step 1: Create Environment File

```bash
# Copy the template and customize
cat > .env << 'EOF'
USDA_API_KEY=your-usda-api-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/mealcalorie
JWT_SECRET=your-super-secure-jwt-secret-key-here-change-this-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
API_RATE_LIMIT=100
CACHE_TTL=3600
ENVIRONMENT=development
HOST=0.0.0.0
PORT=8000
EOF
```

### Step 2: Verify Configuration

```bash
# Test USDA API connectivity
curl -f "https://api.nal.usda.gov/fdc/v1/foods/search?query=apple&api_key=$USDA_API_KEY&pageSize=1"
```

---

## 🔒 Security Best Practices

### Production Environment

```bash
# Generate a strong JWT secret
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Use strong database credentials
DATABASE_URL=postgresql://meal_user:$(openssl rand -base64 32)@localhost:5432/mealcalorie_prod

# Set production environment
ENVIRONMENT=production
```

### Environment-Specific Configurations

#### Development
```bash
ENVIRONMENT=development
DATABASE_URL=postgresql://dev_user:dev_pass@localhost:5432/mealcalorie_dev
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60  # Longer for development
```

#### Testing
```bash
ENVIRONMENT=testing
DATABASE_URL=postgresql://test_user:test_pass@localhost:5432/mealcalorie_test
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=5   # Shorter for tests
```

#### Production
```bash
ENVIRONMENT=production
DATABASE_URL=postgresql://prod_user:secure_pass@db.example.com:5432/mealcalorie
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15  # Shorter for security
```

---

## 📊 Configuration Validation

### Python Script to Validate

```python
# config_validator.py
import os
from dotenv import load_dotenv

def validate_config():
    load_dotenv()
    
    required_vars = [
        'USDA_API_KEY',
        'DATABASE_URL', 
        'JWT_SECRET'
    ]
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print(f"❌ Missing required variables: {', '.join(missing)}")
        return False
        
    print("✅ All required environment variables are set")
    return True

if __name__ == "__main__":
    validate_config()
```

### Usage
```bash
python config_validator.py
```

---

## 🗄️ Database Setup

### PostgreSQL Setup

```bash
# Install PostgreSQL (macOS)
brew install postgresql
brew services start postgresql

# Create database and user
createdb mealcalorie
psql mealcalorie
```

```sql
-- Create user and grant permissions
CREATE USER meal_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE mealcalorie TO meal_user;
ALTER USER meal_user CREATEDB;  -- For running tests
```

### Connection String Examples

```bash
# Local PostgreSQL
DATABASE_URL=postgresql://meal_user:password@localhost:5432/mealcalorie

# Docker PostgreSQL
DATABASE_URL=postgresql://meal_user:password@localhost:5433/mealcalorie

# Cloud PostgreSQL (example)
DATABASE_URL=postgresql://user:pass@host:5432/dbname?sslmode=require
```

---

## 🔧 Docker Environment

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: mealcalorie
      POSTGRES_USER: meal_user
      POSTGRES_PASSWORD: dev_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    env_file:
      - .env
    environment:
      DATABASE_URL: postgresql://meal_user:dev_password@db:5432/mealcalorie

volumes:
  postgres_data:
```

---

## 🧪 Testing Configuration

### Test Environment Variables

```bash
# .env.test
USDA_API_KEY=your-usda-api-key-here
DATABASE_URL=postgresql://test_user:test_pass@localhost:5432/mealcalorie_test
JWT_SECRET=test-jwt-secret-do-not-use-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=5
API_RATE_LIMIT=1000
CACHE_TTL=60
ENVIRONMENT=testing
HOST=127.0.0.1
PORT=8001
```

### Load Test Configuration

```python
# conftest.py
import pytest
from dotenv import load_dotenv

@pytest.fixture(scope="session", autouse=True)
def load_test_env():
    load_dotenv(".env.test")
```

---

## ⚠️ Common Issues

### Issue 1: Database Connection Failed
```bash
# Check PostgreSQL service
brew services list | grep postgresql

# Test connection
psql -h localhost -U meal_user -d mealcalorie -c "SELECT 1;"
```

### Issue 2: Invalid USDA API Key
```bash
# Test API key
curl -f "https://api.nal.usda.gov/fdc/v1/foods/search?query=apple&api_key=$USDA_API_KEY&pageSize=1" || echo "Invalid API key"
```

### Issue 3: JWT Secret Too Short
```python
# Generate secure JWT secret
import secrets
print(f"JWT_SECRET={secrets.token_urlsafe(64)}")
```

---

## 📚 References

- [FastAPI Environment Variables](https://fastapi.tiangolo.com/advanced/settings/)
- [SQLAlchemy Database URLs](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls)
- [python-dotenv Documentation](https://pypi.org/project/python-dotenv/)
- [PostgreSQL Connection Strings](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING)
