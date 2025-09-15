"""
Calory Counter FastAPI Application
"""
from fastapi import FastAPI, Request
import logging
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from src.routers import calories, auth
from src.database.connection import init_db
from src.config.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info(f"Environment: {settings.environment.upper()}")

# Rate limit per-IP (from settings.api_rate_limit)
rate_limit_per_minute = settings.api_rate_limit
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{rate_limit_per_minute}/minute"],
)

app = FastAPI(
    title="Calory Counter API",
    description="A FastAPI backend for calorie lookup and user management",
    version="1.0.0",
)

# Init DB
init_db()

# Install rate-limit handler and middleware
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

logger.info(
    f"Rate limiting enabled: {rate_limit_per_minute} requests per minute per IP"
)

app.include_router(auth.router)
app.include_router(calories.router)


@app.get("/")
async def root():
    """Health check"""
    return {
        "message": "Calory Counter API is running",
        "status": "healthy",
        "version": "1.0.0",
    }


@app.get("/health")
async def health_check():
    """Health"""
    return {"status": "ok", "service": "calory-counter"}


# Example endpoint with per-route limit
@app.get("/rate-limit-test")
@limiter.limit(f"{rate_limit_per_minute}/minute")
async def rate_limit_test(request: Request):
    """Rate limit test"""
    return {
        "message": f"Rate limiting active: {rate_limit_per_minute} requests per minute per IP",
        "your_ip": request.client.host,
        "status": "success",
    }
