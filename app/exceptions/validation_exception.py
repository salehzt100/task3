from app.exceptions import CustomException


class ValidationException(CustomException):
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, status_code=422)
