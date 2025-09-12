"""
Test configuration and fixtures for Calory Counter API
"""
import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Test client for API calls"""
    return TestClient(app)


@pytest.fixture
def test_user_data():
    """Sample user data for testing"""
    return {
        "first_name": "John",
        "last_name": "Doe", 
        "email": "test@example.com",
        "password": "secure123"
    }


@pytest.fixture
def test_calorie_data():
    """Sample calorie request data"""
    return {
        "dish_name": "chicken biryani",
        "servings": 2
    }


@pytest.fixture
def authenticated_client(client, test_user_data):
    """Client with valid JWT token"""
    # First register user
    client.post("/auth/register", json=test_user_data)
    
    # Then login to get token
    login_data = {
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    }
    response = client.post("/auth/login", json=login_data)
    token = response.json()["access_token"]
    
    # Return client with auth header
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client
