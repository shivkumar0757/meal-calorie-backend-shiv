"""
RED PHASE: Authentication endpoint tests (should FAIL initially)
"""
import pytest


class TestUserRegistration:
    """Test user registration endpoint"""
    
    def test_register_user_success(self, client, test_user_data):
        """RED: Test successful user registration - SHOULD FAIL initially"""
        # Act
        response = client.post("/auth/register", json=test_user_data)
        
        # Assert  
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert data["user"]["email"] == test_user_data["email"]
        assert "password" not in data["user"]  # Password should not be returned

    def test_register_duplicate_email(self, client, test_user_data):
        """RED: Test registration with duplicate email fails"""
        # Arrange - register user first
        client.post("/auth/register", json=test_user_data)
        
        # Act - try to register same email again
        response = client.post("/auth/register", json=test_user_data)
        
        # Assert
        assert response.status_code == 409
        assert "already registered" in response.json()["detail"].lower()


class TestUserLogin:
    """Test user login endpoint"""
    
    def test_login_user_success(self, client, test_user_data):
        """RED: Test successful user login - SHOULD FAIL initially"""
        # Arrange - register user first
        client.post("/auth/register", json=test_user_data)
        
        # Act
        login_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        }
        response = client.post("/auth/login", json=login_data)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_credentials(self, client, test_user_data):
        """RED: Test login with wrong password fails"""
        # Arrange - register user first
        client.post("/auth/register", json=test_user_data)
        
        # Act - try wrong password
        login_data = {
            "email": test_user_data["email"],
            "password": "wrongpassword"
        }
        response = client.post("/auth/login", json=login_data)
        
        # Assert
        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower()

    def test_login_nonexistent_user(self, client):
        """RED: Test login with non-existent email"""
        # Act
        login_data = {
            "email": "nonexistent@example.com", 
            "password": "anypassword"
        }
        response = client.post("/auth/login", json=login_data)
        
        # Assert
        assert response.status_code == 401
