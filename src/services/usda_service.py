"""
USDA FoodData Central API service for calorie lookup
"""

import asyncio
import httpx
import time
from typing import Optional, Dict, Any
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)


class USDAService:
    """Service for interacting with USDA FoodData Central API"""

    def __init__(self):
        from src.config.settings import settings

        self.api_key = settings.usda_api_key
        self.base_url = "https://api.nal.usda.gov/fdc/v1"
        
        # Simple in-memory cache with TTL
        self._cache = {}
        self._cache_ttl = settings.cache_ttl  # seconds

    def _get_cache_key(self, query: str) -> str:
        """Generate cache key for query"""
        return f"food_search:{query.lower().strip()}"
    
    def _is_cache_valid(self, timestamp: float) -> bool:
        """Check if cache entry is still valid"""
        return time.time() - timestamp < self._cache_ttl
    
    def _get_from_cache(self, query: str) -> Optional[Dict[str, Any]]:
        """Get cached result if valid"""
        cache_key = self._get_cache_key(query)
        if cache_key in self._cache:
            data, timestamp = self._cache[cache_key]
            if self._is_cache_valid(timestamp):
                logger.info(f"Cache hit for query: {query}")
                return data
            else:
                # Remove expired cache entry
                del self._cache[cache_key]
                logger.info(f"Cache expired for query: {query}")
        return None
    
    def _set_cache(self, query: str, data: Dict[str, Any]) -> None:
        """Cache the result"""
        cache_key = self._get_cache_key(query)
        self._cache[cache_key] = (data, time.time())
        logger.info(f"Cached result for query: {query}")

    async def search_food(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Search for food items and return the best match with calorie data
        Uses caching to improve performance and reduce API calls.

        Args:
            query: Food name to search for

        Returns:
            Dictionary with food data including calories, or None if not found
        """
        # Check cache first
        cached_result = self._get_from_cache(query)
        if cached_result:
            return cached_result
            
        try:
            timeout = httpx.Timeout(10.0, connect=5.0)
            async with httpx.AsyncClient(timeout=timeout) as client:
                url = f"{self.base_url}/foods/search"
                params = {
                    "query": query,
                    "api_key": self.api_key,
                    "pageSize": 3,
                    "dataType": ["Foundation", "SR Legacy", "Branded"],
                }

                logger.info(f"Searching USDA API for: {query}")

                # Simple retry logic
                for attempt in range(2):
                    try:
                        response = await client.get(url, params=params)
                        response.raise_for_status()
                        break
                    except (httpx.TimeoutException, httpx.ConnectError) as e:
                        if attempt == 1:  # Last attempt
                            raise
                        logger.warning(f"USDA API attempt {attempt + 1} failed: {e}")
                        await asyncio.sleep(0.5)

                data = response.json()

                # Check if we have results
                if not data.get("foods"):
                    logger.warning(f"No foods found for query: {query}")
                    return None

                # Find the best match with calorie data
                best_food = self._find_best_food_match(data["foods"], query)

                if not best_food:
                    logger.warning(f"No suitable food match found for: {query}")
                    return None

                # Extract calorie information
                calorie_info = self._extract_calories(best_food)

                if calorie_info is None:
                    logger.warning(f"No calorie data found for: {query}")
                    return None

                # Only extract the essential fields we need
                result = {
                    "description": best_food.get("description", query),
                    "calories_per_100g": calorie_info,
                    "serving_size": best_food.get("servingSize", 100),
                    "serving_unit": best_food.get("servingSizeUnit", "g"),
                    "data_type": best_food.get("dataType"),
                    "source": "USDA FoodData Central",
                }
                
                # Cache the successful result
                self._set_cache(query, result)
                return result

        except httpx.HTTPStatusError as e:
            logger.error(f"USDA API HTTP error: {e.response.status_code}")
            raise HTTPException(
                status_code=503, detail="External food database temporarily unavailable"
            )
        except httpx.RequestError as e:
            logger.error(f"USDA API request error: {e}")
            raise HTTPException(
                status_code=503, detail="Unable to connect to food database"
            )
        except Exception as e:
            logger.error(f"Unexpected error in USDA service: {e}")
            raise HTTPException(
                status_code=500, detail="Internal error while fetching food data"
            )

    def _find_best_food_match(
        self, foods: list, query: str
    ) -> Optional[Dict[str, Any]]:
        """
        Find the best matching food item from USDA results
        Priority: Foundation > SR Legacy > Branded
        """
        # Sort by data type preference and score
        data_type_priority = {"Foundation": 1, "SR Legacy": 2, "Branded": 3}

        def sort_key(food):
            data_type = food.get("dataType", "Branded")
            priority = data_type_priority.get(data_type, 4)
            score = food.get("score", 0)
            return (
                priority,
                -score,
            )  # Lower priority number = better, higher score = better

        sorted_foods = sorted(foods, key=sort_key)

        # Return first food that has calorie data
        for food in sorted_foods:
            if self._has_calorie_data(food):
                return food

        return None

    def _has_calorie_data(self, food: Dict[str, Any]) -> bool:
        """Check if food item has calorie data - optimized for early exit"""
        nutrients = food.get("foodNutrients", [])
        # Early exit - stop at first calorie nutrient found
        for nutrient in nutrients:
            if nutrient.get("nutrientId") == 1008:  # Energy (calories)
                return True
        return False

    def _extract_calories(self, food: Dict[str, Any]) -> Optional[int]:
        """Extract calorie value from food nutrients - optimized for single extraction"""
        nutrients = food.get("foodNutrients", [])

        # Early exit - return immediately when calorie nutrient found
        for nutrient in nutrients:
            if nutrient.get("nutrientId") == 1008:  # Energy (calories)
                value = nutrient.get("value")
                if value is not None and value > 0:  # Ensure positive calorie value
                    return int(round(value))
                break  # Stop searching once we find the calorie nutrient

        return None

    def calculate_serving_calories(
        self, calories_per_100g: int, serving_size_g: float = 100
    ) -> int:
        """
        Calculate calories for a specific serving size

        Args:
            calories_per_100g: Calories per 100g from USDA
            serving_size_g: Serving size in grams (default: 100g)

        Returns:
            Calories for the specified serving size
        """
        return int(round(calories_per_100g * (serving_size_g / 100)))


# Global service instance (lazy-loaded)
_usda_service_instance = None


def get_usda_service() -> USDAService:
    """Get or create USDA service instance"""
    global _usda_service_instance
    if _usda_service_instance is None:
        _usda_service_instance = USDAService()
    return _usda_service_instance
