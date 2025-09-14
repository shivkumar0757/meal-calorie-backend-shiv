"""
Test configuration and fixtures for Calory Counter API
"""
import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

# Set test environment
os.environ["PYTEST_CURRENT_TEST"] = "test"

# Import after setting environment
from main import app
from src.database.connection import get_db
from src.models.user import Base


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test"""
    # Create a fresh in-memory database for each test
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session: Session):
    """Test client for API calls with fresh database"""
    
    def override_get_db():
        try:
            yield db_session
        except:
            db_session.rollback()
            raise
    
    # Override the dependency
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up
    app.dependency_overrides.clear()


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
def specific_test_dishes():
    """Specific dishes from original requirements for testing"""
    return [
        "macaroni and cheese",
        "grilled salmon", 
        "paneer butter masala"
    ]


@pytest.fixture
def authenticated_client(client, test_user_data):
    """Client with valid JWT token"""
    # First register user
    register_response = client.post("/auth/register", json=test_user_data)
    assert register_response.status_code == 201, f"Registration failed: {register_response.json()}"
    
    # Extract token from registration response
    token = register_response.json()["access_token"]
    
    # Return client with auth header
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client
