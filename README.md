# Task Management System

This project implements a database schema for a task management system using SQLAlchemy and Alembic for migrations. The database schema is based on the provided diagram, and the `.env` file is used to configure the database connection.

## Database Models

The database consists of the following tables:

1. **users**: Stores user details such as username and role.
2. **roles**: Defines roles assigned to users.
3. **personal\_access\_tokens**: Manages user authentication tokens.
4. **articles**: Stores article details written by users.
5. **categories**: Categorizes articles.
6. **tags**: Allows tagging of articles.
7. **article\_tag**: Maps articles to tags.
8. **comments**: Stores comments for articles.

## Setup Instructions

### Prerequisites

1. Python installed on your system.
2. PostgreSQL database server running locally or remotely.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/salehzt100/task3.git
   cd task3
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the .env file:
   Ensure `.env` contains the following:

   ```env
   DB_CONNECTION=postgresql+psycopg2
   DB_HOST=localhost
   DB_PORT=5432
   DB_DATABASE=task3_db
   DB_USERNAME=postgres
   DB_PASSWORD=2222
   ```

### Running Migrations

1. Initialize Alembic:

   ```bash
   alembic init migrations
   ```

2. Generate a migration:

   ```bash
   alembic revision --autogenerate -m "Initial migration"
   ```

3. Apply the migration:

   ```bash
   alembic upgrade head
   ```

### Running the Application

1. Activate the virtual environment:

   ```bash
   source .venv/bin/activate
   ```

2. Start the application using Uvicorn:

   ```bash
   uvicorn main:app --reload
   ```

3. Visit `/docs` in your browser to view the Swagger UI for API documentation.

### Populating the Database

1. Run the role seeder script to populate the roles table:

   ```bash
   python database/seeder/role_seeder.py
   ```

2. (Optional) Before running the admin seeder, you can edit the admin user details in `core/config.py`. For example:

   ```python
   ADMIN_USER = {
       "name": "Admin",
       "username": "admin",
       "password": "password",
   }
   ```

3. Run the admin seeder script:

   ```bash
   python database/seeder/admin_seeder.py
   ```

## Project Structure

The project follows the structure shown below:

```
Task3/
├── .venv/
├── api/
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── api.py
├── app/
│   ├── controllers/
│   ├── enums/
│   ├── exceptions/
│   ├── models/
│   ├── repositories/
│   ├── services/
│   ├── __init__.py
├── core/
│   ├── __init__.py
│   ├── config.py
│   ├── security.py
├── database/
│   ├── migration/
│   ├── schema/
│   ├── seeder/
│   ├── __init__.py
├── utils/
│   ├── fastapi/
│   │   ├── __init__.py
│   │   ├── decorators.py
├── .env
├── .gitignore
├── alembic.ini
├── bootstrap.py
├── main.py
├── README.md
```

### Custom Exceptions

The project includes custom exceptions to handle errors gracefully. These exceptions are located in the `app/exceptions` directory. Use them to standardize error handling across the application.

Example of a custom exception:

```python
class CustomException(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
```

## Middleware for Authentication and Role-Based Authorization

The project uses a custom middleware `OAuth2Middleware` to handle Bearer token authentication, verify tokens, and attach the current user to the request. It also supports role-based authorization using dependencies.

### Middleware Implementation

```python
from fastapi import Depends, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from core.security import verify_access_token, get_current_user

class OAuth2Middleware(BaseHTTPMiddleware):
    def __init__(self, app, excluded_routes):
        super().__init__(app)
        self.excluded_routes = excluded_routes

    async def dispatch(self, request: Request, call_next):
        if request.url.path not in self.excluded_routes:
            try:
                verify_access_token(request)
                response = await call_next(request)
                return response
            except HTTPException as exc:
                return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)
            except Exception as exc:
                return JSONResponse(content={"detail": f"Error: {str(exc)}"}, status_code=500)
        else:
            response = await call_next(request)
            return response

def role_required(roles: list[str]):
    def role_checker(user=Depends(get_current_user)):
        if not any(role in [user.role.name] for role in roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted"
            )
    return role_checker
```

### Example Usage in Routes

To secure a route with role-based authorization:

```python
from fastapi import APIRouter, Depends
from app.middlewares import role_required

router = APIRouter()

@router.get("/secure-endpoint", dependencies=[Depends(role_required(["EDITOR", "ADMIN"]))])
async def secure_endpoint():
    return {"message": "This endpoint is secured and requires specific roles."}
```

### Middleware Integration

To add the middleware to your application, use the following configuration in `main.py`:

```python
from core.config import settings
from app.middlewares import OAuth2Middleware

app.add_middleware(OAuth2Middleware, excluded_routes=settings.excluded_routes)
```

In `core/config.py`, define the excluded routes:

```python
excluded_routes = [
    "/users/{user_id}",
    "/docs",
    "/openapi.json",
    "/login",
]
```

## Authentication

The project uses Bearer tokens for user authentication. Ensure that `personal_access_tokens` are properly generated and managed to secure the API endpoints.

## API Schema

### Login Endpoint
- **Request Body**:
  ```json
  {
    "username": "admin",
    "password": "password"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "username": "admin",
    "role": "ADMIN"
  }
  ```

### Role-Based Authorization Example
To secure a route with role-based authorization:

```python
from fastapi import APIRouter, Depends
from app.middlewares import role_required

router = APIRouter()

@router.get("/admin-panel", dependencies=[Depends(role_required(["ADMIN"]))])
async def admin_panel():
    return {"message": "Welcome, Admin!"}
```

## Available Roles

The application supports the following roles:
- **ADMIN**: Full access to all resources.
- **EDITOR**: Can manage articles but not user roles.
- **AUTHOR**: Can create and edit their own articles.
- **READER**: Can only read articles.

