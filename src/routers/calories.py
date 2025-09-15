"""
Calorie lookup endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from src.schemas.calories import CalorieRequest, CalorieResponse, ErrorResponse
from src.services.usda_service import get_usda_service
from src.utils.dependencies import get_current_user
from src.models.user import User
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="", tags=["calories"])


@router.post(
    "/get-calories",
    response_model=CalorieResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Authentication required"},
        404: {"model": ErrorResponse, "description": "Dish not found"},
        422: {"model": ErrorResponse, "description": "Validation error"},
        503: {"model": ErrorResponse, "description": "External service unavailable"},
    },
)
async def get_calories(
    request: CalorieRequest, current_user: User = Depends(get_current_user)
):
    """
    Get calorie information for a dish with specified servings

    This endpoint searches the USDA FoodData Central database for the specified dish
    and returns calorie information per serving and total calories.
    """
    try:
        logger.info(
            f"Calorie lookup request: {request.dish_name} x {request.servings} for user {current_user.email}"
        )

        # Search for food in USDA database
        usda_service = get_usda_service()
        food_data = await usda_service.search_food(request.dish_name)

        if not food_data:
            logger.warning(f"Food not found: {request.dish_name}")
            raise HTTPException(
                status_code=404,
                detail=f"Dish '{request.dish_name}' not found in food database",
            )

        # Calculate calories per serving using actual serving size data
        calories_per_100g = food_data["calories_per_100g"]
        serving_size_g = food_data.get("serving_size", 100)

        # Calculate calories per actual serving
        if serving_size_g != 100:
            calories_per_serving = int(
                round(calories_per_100g * (serving_size_g / 100))
            )
        else:
            calories_per_serving = calories_per_100g

        total_calories = calories_per_serving * request.servings

        response = CalorieResponse(
            dish_name=request.dish_name,
            servings=request.servings,
            calories_per_serving=calories_per_serving,
            total_calories=total_calories,
            source=food_data["source"],
        )

        logger.info(f"Calorie lookup successful: {response.model_dump()}")
        return response

    except HTTPException:
        # Re-raise HTTP exceptions from service
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_calories: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error while processing calorie request",
        )
