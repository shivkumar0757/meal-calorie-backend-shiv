Product Requirement Document (PRD)

Project: Meal Calorie Backend
Owner: Backend Team
Date: YYYY-MM-DD

---

1. Objective

Build a backend service that allows users to register/login and input a dish name with servings. The service fetches calorie data from the USDA FoodData Central API and returns structured calorie information.

---

2. Functional Requirements
	-	User Authentication
	-	/auth/register: register with first name, last name, email, and password.
	-	/auth/login: login with email + password → return JWT.
	-	Calorie Calculation
	-	/get-calories: accept dish_name and servings.
	-	Fetch data from USDA API.
	-	Return calories per serving, total calories, and source.
	-	Error Handling
	-	Handle invalid dish (return Dish not found).
	-	Handle zero/negative servings.
	-	Handle multiple matches (fuzzy match best result).

---

3. Non-Functional Requirements
	-	Security
	-	JWT authentication.
	-	Password hashing with bcrypt.
	-	Store secrets in .env.
	-	Rate limiting middleware.
	-	Performance
	-	Async DB queries (PostgreSQL with asyncpg).
	-	Async USDA API calls with httpx.
	-	In-memory cache for frequent queries (upgradeable to Redis).
	-	Reliability & Maintainability
	-	Modular file structure.
	-	Friendly error messages.
	-	Unit & integration tests.

---

4. Tech Stack
	-	Language: Python 3.11+
	-	Framework: FastAPI
	-	Database: PostgreSQL (SQLAlchemy 2.0 + asyncpg)
	-	External API: USDA FoodData Central
	-	Auth: JWT + bcrypt
	-	Testing: pytest

---

5. API Endpoints
	-	POST /auth/register → register user
	-	POST /auth/login → login user
	-	POST /get-calories → calorie lookup

Example Request

{
  "dish_name": "chicken biryani",
  "servings": 2
}

Example Response

{
  "dish_name": "chicken biryani",
  "servings": 2,
  "calories_per_serving": 280,
  "total_calories": 560,
  "source": "USDA FoodData Central"
}


---

6. Database Schema

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE meals (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    dish_name VARCHAR(100),
    servings INT,
    calories_per_serving INT,
    total_calories INT,
    source VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);


---

7. Testing Scenarios
	-	Valid dish lookup (e.g., “macaroni and cheese”).
	-	Invalid dish.
	-	Zero/negative servings.
	-	Multiple matches.

---

8. Future Enhancements
	-	Add macronutrient breakdown (carbs, protein, fat).
	-	Add meal history logging.
	-	Dockerize backend.
	-	Replace in-memory cache with Redis.

---

Success Metric: Accurate calorie responses (<2s), secure auth, responsive API, >90% tests passing.