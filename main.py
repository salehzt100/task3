from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from api import api_router
from app.exceptions.exception_handlers import (
    not_found_exception_handler,
    custom_exception_handler,
    validation_exception_handler,
)
from app.exceptions import (
    CustomException,
    NotFoundException,
    ValidationException
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(title='task3')

# register exception handlers
app.add_exception_handler(NotFoundException, not_found_exception_handler)
app.add_exception_handler(CustomException, custom_exception_handler)
app.add_exception_handler(ValidationException, validation_exception_handler)



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(api_router)

