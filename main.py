from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from core.config import settings
from api import api_router
from app.exceptions.exception_handlers import (
    not_found_exception_handler,
    custom_exception_handler,
    validation_exception_handler,
)
from app.exceptions import (
    CustomException,
    NotFoundException,
    ValidationException,
)
from utils.fastapi.middlewares.authorization import OAuth2Middleware

# Initialize FastAPI app with title
app = FastAPI(title='task3')

# Add OAuth2 middleware with excluded routes
app.add_middleware(OAuth2Middleware, settings.excluded_routes)

# Register custom exception handlers
app.add_exception_handler(NotFoundException, not_found_exception_handler)
app.add_exception_handler(CustomException, custom_exception_handler)
app.add_exception_handler(ValidationException, validation_exception_handler)

# Include the main router for the API
app.include_router(api_router)
