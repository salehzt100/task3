from app.exceptions import CustomException


class NotFoundException(CustomException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)

