# High Level Design (HLD)

## 🎯 System Overview

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

## 🏗️ Architecture Components

### 1. API Layer (`src/routers/`)
- **auth.py** - `/auth/register`, `/auth/login` endpoints
- **calories.py** - `/get-calories` endpoint

### 2. Business Layer (`src/controllers/`)
- **auth_controller.py** - User registration/login logic
- **calorie_controller.py** - Calorie calculation logic

### 3. Data Layer 
- **models/** - SQLAlchemy user & meal models
- **services/usda_service.py** - USDA API integration
- **database/** - DB connection & session management

---

## 🔄 Request Flow

### Auth Flow
```
POST /auth/register → auth_controller → User model → JWT token
POST /auth/login    → auth_controller → User model → JWT token
```

### Calorie Flow
```
POST /get-calories → calorie_controller → usda_service → USDA API
                                      ↓
                   Response ← format_response ← parse_nutrients
```

---

## 🗄️ Data Models

### Users Table
```sql
users (id, first_name, last_name, email, password_hash, created_at)
```

### Meals Table (Optional History)
```sql
meals (id, user_id, dish_name, servings, calories_per_serving, total_calories, created_at)
```

---

## 🔧 External Dependencies

- **USDA FoodData Central API** - Food/nutrient data
- **PostgreSQL** - User & meal storage
- **JWT** - Token-based authentication

---

## ⚡ Key Design Decisions

1. **Async FastAPI** - For concurrent USDA API calls
2. **JWT Auth** - Stateless authentication
3. **SQLAlchemy 2.0** - Modern async ORM
4. **Pydantic Models** - Request/response validation
5. **Environment Config** - `.env` for secrets

This matches the PRD exactly - 3 endpoints, JWT auth, PostgreSQL, USDA integration.
