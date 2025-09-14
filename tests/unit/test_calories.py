"""
RED PHASE: Calorie lookup endpoint tests (should FAIL initially)
"""
import pytest


class TestCalorieLookup:
    """Test calorie lookup endpoint"""
    
    def test_get_calories_success(self, authenticated_client, test_calorie_data):
        """RED: Test successful calorie lookup - SHOULD FAIL initially"""
        # Act
        response = authenticated_client.post("/get-calories", json=test_calorie_data)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure matches PRD
        assert data["dish_name"] == test_calorie_data["dish_name"]
        assert data["servings"] == test_calorie_data["servings"]
        assert "calories_per_serving" in data
        assert "total_calories" in data
        assert data["source"] == "USDA FoodData Central"
        
        # Verify calculations
        expected_total = data["calories_per_serving"] * test_calorie_data["servings"]
        assert data["total_calories"] == expected_total

    def test_get_calories_requires_auth(self, client, test_calorie_data):
        """RED: Test that calorie endpoint requires authentication"""
        # Act - call without auth token
        response = client.post("/get-calories", json=test_calorie_data)
        
        # Assert - FastAPI HTTPBearer returns 403 when no token provided
        assert response.status_code == 403

    def test_get_calories_dish_not_found(self, authenticated_client):
        """RED: Test calorie lookup for invalid dish"""
        # Arrange
        invalid_data = {
            "dish_name": "invalidfoodxyz123notfound",
            "servings": 1
        }
        
        # Act
        response = authenticated_client.post("/get-calories", json=invalid_data)
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_get_calories_invalid_servings(self, authenticated_client):
        """RED: Test calorie lookup with invalid servings"""
        # Arrange
        invalid_data = {
            "dish_name": "apple",
            "servings": 0  # Invalid: zero servings
        }
        
        # Act
        response = authenticated_client.post("/get-calories", json=invalid_data)
        
        # Assert
        assert response.status_code == 422  # Validation error

    def test_get_calories_negative_servings(self, authenticated_client):
        """RED: Test calorie lookup with negative servings"""
        # Arrange
        invalid_data = {
            "dish_name": "apple", 
            "servings": -1  # Invalid: negative servings
        }
        
        # Act
        response = authenticated_client.post("/get-calories", json=invalid_data)
        
        # Assert
        assert response.status_code == 422  # Validation error

    def test_specific_dishes_from_requirements(self, authenticated_client, specific_test_dishes):
        """Test specific dishes mentioned in original requirements"""
        for dish in specific_test_dishes:
            # Arrange
            calorie_data = {
                "dish_name": dish,
                "servings": 1
            }
            
            # Act
            response = authenticated_client.post("/get-calories", json=calorie_data)
            
            # Assert
            assert response.status_code == 200, f"Failed for dish: {dish}"
            data = response.json()
            assert data["dish_name"], f"Missing dish_name for: {dish}"
            assert data["servings"] == 1, f"Wrong servings for: {dish}"
            assert data["calories_per_serving"] > 0, f"No calories found for: {dish}"
            assert data["total_calories"] == data["calories_per_serving"], f"Wrong calculation for: {dish}"
            assert data["source"] == "USDA FoodData Central", f"Wrong source for: {dish}"
