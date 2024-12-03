from functools import wraps
from fastapi.responses import JSONResponse

def exception_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return JSONResponse(
                content={
                    "success": False,
                    "error": f"An unexpected error occurred: {str(e)}",
                },
                status_code=500,
            )
    return wrapper