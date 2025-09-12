# Meal Calorie Backend

## 📌 Overview

A backend service that allows users to register/login, input meal details (dish name + servings), and fetch calorie counts using the USDA FoodData Central API.

---

## 🚀 Tech Stack

* **Language**: Python 3.11+
* **Framework**: FastAPI
* **Database**: PostgreSQL (SQLAlchemy 2.0 + asyncpg)
* **External API**: USDA FoodData Central
* **Authentication**: JWT + bcrypt

---

## 📂 Project Structure

```
src/
  routers/       # Route definitions
  controllers/   # Business logic
  models/        # SQLAlchemy models
  schemas/       # Pydantic schemas
  services/      # USDA + DB logic
  utils/         # Helpers & error handling
  database/      # DB connection & sessions
tests/
  unit/          # Unit tests
  integration/   # Integration tests
docs/
  PRD.md         # Product Requirements Document
  HLD.md         # High Level Design
  LLD.md         # Low Level Design
  usda-api-reference.md    # USDA API documentation
  environment-setup.md     # Environment configuration
```

---

## ⚙️ Setup

1. Clone the repo:

```bash
git clone https://github.com/your-username/meal-calorie-backend.git
cd meal-calorie-backend
```

2. Create virtual environment & install dependencies:

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

3. Setup `.env` file:

```env
USDA_API_KEY=your_api_key_here
DATABASE_URL=postgresql://user:password@localhost:5432/mealcalorie
JWT_SECRET=your_jwt_secret
```

4. Run the server:

```bash
uvicorn src.main:app --reload
```

---

## 📌 API Endpoints

* **POST /auth/register** → Register new user
* **POST /auth/login** → User login
* **POST /get-calories** → Get calories by dish name + servings

Example request:

```json
{
  "dish_name": "chicken biryani",
  "servings": 2
}
```

Example response:

```json
{
  "dish_name": "chicken biryani",
  "servings": 2,
  "calories_per_serving": 280,
  "total_calories": 560,
  "source": "USDA FoodData Central"
}
```

---

## 🧪 Testing

Run tests with:

```bash
pytest
```

---

## 📜 License

MIT License
