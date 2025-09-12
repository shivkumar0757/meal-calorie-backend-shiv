# 🚦 TDD Test Suite - Ready to Use

## ✅ What We've Created

### Test Files Structure
```
tests/
├── conftest.py              ✅ Test fixtures & setup
├── unit/
│   ├── test_auth.py         ✅ 6 auth tests (register/login)  
│   └── test_calories.py     ✅ 5 calorie lookup tests
├── integration/
│   └── test_api.py          ✅ 1 end-to-end test
└── run_tests.py             ✅ TDD test runner
```

### Test Coverage (12 Total Tests)
- **Authentication**: 6 tests
  - Register success ✅
  - Register duplicate email ✅  
  - Login success ✅
  - Login wrong password ✅
  - Login non-existent user ✅
  
- **Calorie Lookup**: 5 tests
  - Get calories success ✅
  - Requires authentication ✅
  - Dish not found ✅
  - Invalid servings (zero) ✅
  - Negative servings ✅

- **Integration**: 1 test  
  - Complete user flow ✅

## 🚦 TDD Workflow

### Phase 1: RED (Tests Should FAIL)
```bash
cd /Users/shivkumar/PycharmProjects/CaloryCounter
python run_tests.py red
```
**Expected**: All 12 tests FAIL (endpoints don't exist yet)

### Phase 2: GREEN (Implement to Pass)
1. Implement minimal endpoints:
   - `POST /auth/register`
   - `POST /auth/login` 
   - `POST /get-calories`

2. Run tests:
```bash
python run_tests.py green
```
**Goal**: Make all tests PASS with minimal code

### Phase 3: REFACTOR
- Clean up code
- Improve structure
- Tests should still pass

## 🎯 Minimal Implementation Checklist

To make tests pass, you need:

### 1. Auth Endpoints (`src/routers/auth.py`)
```python
@router.post("/register", status_code=201)
async def register(user_data: UserCreate):
    # Hash password, save to DB, return JWT
    
@router.post("/login")  
async def login(credentials: UserLogin):
    # Verify credentials, return JWT
```

### 2. Calorie Endpoint (`src/routers/calories.py`)
```python
@router.post("/get-calories", dependencies=[Depends(get_current_user)])
async def get_calories(request: CalorieRequest):
    # Call USDA API, return formatted response
```

### 3. Data Models (`src/models/`)
- User model (SQLAlchemy)
- Request/Response schemas (Pydantic)

### 4. Services (`src/services/`)
- USDA API integration
- Auth utilities (JWT, password hashing)

## 🚀 Next Steps

1. **Run RED phase** first to see failing tests
2. **Install dependencies** (if not done):
   ```bash
   pip install -r requirements.txt
   ```
3. **Implement endpoints** one by one
4. **Run GREEN phase** until all pass
5. **Refactor** for better design

## 📊 Test Summary

- **Simple & Focused**: Only 12 essential tests
- **Fast Feedback**: Quick to run and understand  
- **Complete Coverage**: All 3 core endpoints tested
- **TDD Ready**: Designed to fail first, then pass

Ready to start the RED-GREEN-REFACTOR cycle! 🎯
