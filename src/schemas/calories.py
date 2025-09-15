"""
Pydantic schemas for calorie-related requests and responses
"""

from pydantic import BaseModel, Field


class CalorieRequest(BaseModel):
    """Request schema for calorie lookup"""

    dish_name: str = Field(
        ..., min_length=1, max_length=100, description="Name of the dish"
    )
    servings: int = Field(
        ..., gt=0, description="Number of servings (must be positive)"
    )


class CalorieResponse(BaseModel):
    """Response schema for calorie lookup"""

    dish_name: str
    servings: int
    calories_per_serving: int
    total_calories: int
    source: str = "USDA FoodData Central"


class ErrorResponse(BaseModel):
    """Error response schema"""

    detail: str
