from functools import wraps
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.exceptions.custom_response import custom_response_error


def exception_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IntegrityError as e:
            return JSONResponse(
                content={
                    "success": False,
                    "error": custom_response_error(str(e)),
                },
                status_code=500,
            )
        except Exception as e:
            return JSONResponse(
                content={
                    "success": False,
                    "error": f"An unexpected error occurred: {str(e)}",
                },
                status_code=500,
            )
    return wrapper