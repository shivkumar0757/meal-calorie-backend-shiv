# High Level Design (HLD)

## System Overview

Simple 3-layer FastAPI backend that handles user auth and calorie lookups via USDA API.

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Client    │───▶│   FastAPI   │───▶│  PostgreSQL │
│ (Frontend)  │    │  Backend    │    │  Database   │
└─────────────┘    └─────┬───────┘    └─────────────┘
                         │
                         ▼
                   ┌─────────────┐
                   │  USDA API   │
                   │ (External)  │
                   └─────────────┘
```

---

## Architecture Components

### 1. API Layer (`src/routers/`)
- **auth.py** - `/auth/register`, `/auth/login` endpoints with business logic
- **calories.py** - `/get-calories` endpoint with business logic

### 2. Service Layer (`src/services/`)
- **usda_service.py** - USDA API integration with caching

### 3. Data Layer 
- **models/** - SQLAlchemy user model
- **schemas/** - Pydantic request/response schemas
- **database/** - DB connection & session management

### 4. Utilities (`src/utils/`)
- **auth.py** - JWT token management and password hashing
- **dependencies.py** - FastAPI dependency injection for authentication

---

## Request Flow

### Auth Flow
```
POST /auth/register → auth router → User model → JWT token response
POST /auth/login    → auth router → User model → JWT token response
```

### Calorie Flow
```
POST /get-calories → calories router → usda_service → USDA API (with cache)
                                    ↓
                   Response ← formatted response ← parsed nutrients
```

---

## Data Models

### Users Table
```sql
users (id, first_name, last_name, email, password_hash, created_at)
```

Note: No meals table - calorie lookups are stateless per requirements.

---

## External Dependencies

- **USDA FoodData Central API** - Food/nutrient data with caching
- **SQLite (dev) / PostgreSQL (prod)** - User storage
- **JWT** - Token-based authentication

---

## Key Design Decisions

1. **Async FastAPI** - For concurrent USDA API calls
2. **JWT Auth** - Stateless authentication
3. **SQLAlchemy 2.0** - Modern async ORM
4. **Pydantic Models** - Request/response validation
5. **Environment Config** - `.env` for secrets

This matches the PRD exactly - 3 endpoints, JWT auth, PostgreSQL, USDA integration.
