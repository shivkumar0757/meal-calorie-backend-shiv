"""
RED PHASE: Integration tests (should FAIL initially)
"""
import pytest


class TestCompleteUserFlow:
    """Test end-to-end user flows"""
    
    def test_complete_user_journey(self, client):
        """RED: Test complete flow: register → login → get calories"""
        
        # Step 1: Register new user
        user_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@test.com", 
            "password": "mypassword123"
        }
        
        register_response = client.post("/auth/register", json=user_data)
        assert register_response.status_code == 201
        
        # Step 2: Login with registered user
        login_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        login_response = client.post("/auth/login", json=login_data)
        assert login_response.status_code == 200
        
        token = login_response.json()["access_token"]
        
        # Step 3: Get calories with authentication
        headers = {"Authorization": f"Bearer {token}"}
        calorie_data = {
            "dish_name": "banana", 
            "servings": 1
        }
        
        calorie_response = client.post(
            "/get-calories", 
            json=calorie_data,
            headers=headers
        )
        assert calorie_response.status_code == 200
        
        # Verify complete response
        data = calorie_response.json()
        assert data["dish_name"] == "banana"
        assert data["servings"] == 1
        assert data["calories_per_serving"] > 0
        assert data["total_calories"] == data["calories_per_serving"]
