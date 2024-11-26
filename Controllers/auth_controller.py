import hashlib
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from starlette import status
from Enums import RoleEnum
from models import User
from schema import RegisterRequestBody

class AuthController:
    @staticmethod
    def register(user: RegisterRequestBody, db: Session):
        """
        Register a new user.

        Parameters:
            user (RegisterRequestBody): The user details provided in the request body.
            db (Session): The SQLAlchemy database session.

        Returns:
            JSONResponse: A FastAPI response with the status code and message.
        """
        try:
            # Hash the user's password
            hashed_password = hashlib.sha256(user.password.encode('utf-8')).hexdigest()

            # Create a new user instance
            new_user = User(
                name=user.name,
                username=user.username,
                password=hashed_password,
                role_id=user.role_id.value,
                is_active=True if user.role_id.value == RoleEnum.READER.value else False,
            )

            # Add the user to the database
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            # Response handling based on the user's role
            if user.role_id.value == RoleEnum.AUTHOR.value:
                return JSONResponse(
                    content={
                        "success": True,
                        "message": "User created successfully. Please wait for admin approval.",
                    },
                    status_code=status.HTTP_201_CREATED
                )
            elif user.role_id.value == RoleEnum.READER.value:
                return JSONResponse(
                    content={
                        "success": True,
                        "message": "User created successfully.",
                        "data": {
                            "id": new_user.id,
                            "name": new_user.name,
                            "username": new_user.username,
                            "role": new_user.role.name,
                        },
                    },
                    status_code=status.HTTP_201_CREATED
                )
        except Exception as e:
            db.rollback()
            return JSONResponse(
                content={
                    "success": False,
                    "error": str(e),
                },
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        finally:
            db.close()
