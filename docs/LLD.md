# Low Level Design (LLD)

## 📁 File Structure
```
src/
├── main.py                 # FastAPI app entry point
├── routers/
│   ├── auth.py            # Auth endpoints
│   └── calories.py        # Calorie endpoints  
├── controllers/
│   ├── auth_controller.py # User auth logic
│   └── calorie_controller.py # Calorie logic
├── models/
│   ├── user.py           # User SQLAlchemy model
│   └── meal.py           # Meal SQLAlchemy model
├── schemas/
│   ├── auth_schemas.py   # Pydantic auth models
│   └── calorie_schemas.py # Pydantic calorie models
├── services/
│   └── usda_service.py   # USDA API client
├── database/
│   └── connection.py     # DB setup & sessions
└── utils/
    ├── auth_utils.py     # JWT & password helpers
    └── exceptions.py     # Custom exceptions
```

---

## 🔑 Core Implementation

### 1. Authentication Flow

**Router** (`routers/auth.py`)
```python
@router.post("/register")
async def register(user_data: RegisterRequest) -> TokenResponse:
    return await auth_controller.register_user(user_data)
```

**Controller** (`controllers/auth_controller.py`)
```python
async def register_user(user_data: RegisterRequest) -> TokenResponse:
    # 1. Hash password
    # 2. Create user in DB
    # 3. Generate JWT token
    # 4. Return token
```

**Key Functions:**
- `hash_password(password: str) -> str`
- `verify_password(password: str, hashed: str) -> bool`
- `create_jwt_token(user_id: int) -> str`

### 2. Calorie Lookup Flow

**Router** (`routers/calories.py`)
```python
@router.post("/get-calories")
async def get_calories(request: CalorieRequest) -> CalorieResponse:
    return await calorie_controller.calculate_calories(request)
```

**Controller** (`controllers/calorie_controller.py`)
```python
async def calculate_calories(request: CalorieRequest) -> CalorieResponse:
    # 1. Call USDA API
    # 2. Parse nutrients (find calories)
    # 3. Calculate total calories
    # 4. Format response
```

**USDA Service** (`services/usda_service.py`)
```python
async def search_food(query: str) -> USDAResponse:
    # GET request to USDA API
    # Return parsed response

def extract_calories(usda_data: dict) -> float:
    # Find nutrient ID 1008 (calories)
    # Return calories per 100g
```

---

## 📊 Data Models

### SQLAlchemy Models

**User Model** (`models/user.py`)
```python
class User(Base):
    __tablename__ = "users"
    
    id: int = Column(Integer, primary_key=True)
    first_name: str = Column(String(50))
    last_name: str = Column(String(50))
    email: str = Column(String(100), unique=True)
    password_hash: str = Column(Text)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
```

### Pydantic Schemas

**Request/Response Models** (`schemas/`)
```python
class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class CalorieRequest(BaseModel):
    dish_name: str
    servings: int = Field(gt=0)

class CalorieResponse(BaseModel):
    dish_name: str
    servings: int
    calories_per_serving: float
    total_calories: float
    source: str = "USDA FoodData Central"
```

---

## 🌐 API Integration

### USDA API Client
```python
# services/usda_service.py
class USDAService:
    BASE_URL = "https://api.nal.usda.gov/fdc/v1"
    
    async def search_food(self, query: str) -> dict:
        url = f"{self.BASE_URL}/foods/search"
        params = {
            "query": query,
            "api_key": settings.USDA_API_KEY,
            "pageSize": 5
        }
        # Return first match with calories
```

### Error Handling Strategy
```python
# utils/exceptions.py
class FoodNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Dish not found")

class InvalidServingsError(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Servings must be positive")
```

---

## 🔒 Security Implementation

### JWT Configuration
```python
# utils/auth_utils.py
SECRET_KEY = settings.JWT_SECRET
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
```

### Password Security
```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
```

---

## ⚡ Performance Considerations

1. **Async Database** - All DB operations are async
2. **HTTP Client Pooling** - Reuse connections for USDA API
3. **Basic Caching** - Cache frequent food lookups (optional)
4. **Input Validation** - Pydantic validates all requests

---

This LLD covers exactly what's in the PRD - no more, no less. Ready to implement!
