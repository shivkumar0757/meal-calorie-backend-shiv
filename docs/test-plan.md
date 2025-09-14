# 🧪 Minimal TDD Test Plan

## 📋 Test Strategy: Red-Green-Refactor

### Phase 1: Authentication Tests (RED → GREEN)

#### 1.1 User Registration Tests
```python
# RED: Write failing test first
def test_register_user_success():
    """Test successful user registration"""
    # Arrange
    user_data = {
        "first_name": "John",
        "last_name": "Doe", 
        "email": "john@example.com",
        "password": "secure123"
    }
    # Act & Assert
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    assert "access_token" in response.json()

def test_register_duplicate_email():
    """Test registration with duplicate email fails"""
    # Should return 409 Conflict
    pass
```

#### 1.2 User Login Tests
```python
def test_login_user_success():
    """Test successful user login"""
    # Arrange
    login_data = {"email": "john@example.com", "password": "secure123"}
    # Act & Assert
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_credentials():
    """Test login with wrong password fails"""
    # Should return 401 Unauthorized
    pass
```

### Phase 2: Calorie Lookup Tests (RED → GREEN)

#### 2.1 Happy Path Test
```python
def test_get_calories_success():
    """Test successful calorie lookup"""
    # Arrange
    calorie_data = {
        "dish_name": "chicken biryani",
        "servings": 2
    }
    # Act & Assert
    response = authenticated_client.post("/get-calories", json=calorie_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["dish_name"] == "chicken biryani"
    assert data["servings"] == 2
    assert "calories_per_serving" in data
    assert "total_calories" in data
    assert data["source"] == "USDA FoodData Central"
```

#### 2.2 Specific Dish Tests (Original Requirements)
```python
def test_specific_dishes_from_requirements(specific_test_dishes, authenticated_client):
    """Test specific dishes mentioned in original requirements"""
    for dish in specific_test_dishes:
        calorie_data = {"dish_name": dish, "servings": 1}
        response = authenticated_client.post("/get-calories", json=calorie_data)
        assert response.status_code == 200
        data = response.json()
        assert data["dish_name"]
        assert data["calories_per_serving"] > 0
        assert data["source"] == "USDA FoodData Central"
```

#### 2.3 Error Cases Tests
```python
def test_get_calories_dish_not_found():
    """Test calorie lookup for invalid dish"""
    calorie_data = {"dish_name": "invalidfoodxyz123", "servings": 1}
    response = authenticated_client.post("/get-calories", json=calorie_data)
    assert response.status_code == 404
    assert "Dish not found" in response.json()["detail"]

def test_get_calories_invalid_servings():
    """Test calorie lookup with zero servings"""
    calorie_data = {"dish_name": "apple", "servings": 0}
    response = authenticated_client.post("/get-calories", json=calorie_data)
    assert response.status_code == 422
```

### Phase 3: Integration Tests (Minimal)

#### 3.1 End-to-End Flow
```python
def test_complete_user_flow():
    """Test complete flow: register → login → get calories"""
    # 1. Register
    # 2. Login  
    # 3. Get calories with token
    # Assert each step works
    pass
```

## 🎯 Test Execution Order

### RED Phase (Write failing tests)
1. `test_register_user_success()` ❌
2. `test_login_user_success()` ❌  
3. `test_get_calories_success()` ❌

### GREEN Phase (Make tests pass)
1. Implement minimal auth endpoints
2. Implement minimal calorie lookup
3. Make all tests pass ✅

### REFACTOR Phase
1. Clean up code
2. Add error handling
3. Optimize structure

## 📂 Test File Structure

```
tests/
├── conftest.py              # Test fixtures & setup
├── unit/
│   ├── test_auth.py         # Auth unit tests
│   └── test_calories.py     # Calorie unit tests  
└── integration/
    └── test_api.py          # End-to-end tests
```

## ⚡ Key Test Fixtures Needed

```python
# conftest.py essentials
@pytest.fixture
def client():
    """Test client for API calls"""
    
@pytest.fixture  
def authenticated_client():
    """Client with valid JWT token"""

@pytest.fixture
def test_user():
    """Sample user data for tests"""

@pytest.fixture
def specific_test_dishes():
    """Specific dishes from original requirements"""
    return [
        "macaroni and cheese",
        "grilled salmon", 
        "paneer butter masala"
    ]
```

## 🎯 Success Criteria

- ✅ 3 core endpoints tested (register, login, get-calories)
- ✅ Happy path + 1-2 error cases each
- ✅ All tests pass after implementation
- ✅ < 50 lines of test code total (minimal!)

## 📝 Notes

- Focus on **functional testing** over unit testing initially
- Use **mocks** for USDA API calls to avoid external dependencies
- Keep tests **simple and readable**
- Add more tests later as needed

---

*This minimal test plan ensures core functionality works while keeping overhead low.*
