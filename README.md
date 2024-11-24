# Task Management System

This project implements a database schema for a task management system using SQLAlchemy and Alembic for migrations. The database schema is based on the provided diagram, and the `.env` file is used to configure the database connection.

## Database Models

The database consists of the following tables:

1. **users**: Stores user details such as username and role.
2. **roles**: Defines roles assigned to users.
3. **permissions**: Specifies various permissions.
4. **role_permission**: Links roles with permissions.
5. **personal_access_tokens**: Manages user authentication tokens.
6. **articles**: Stores article details written by users.
7. **categories**: Categorizes articles.
8. **tags**: Allows tagging of articles.
9. **article_tag**: Maps articles to tags.
10. **comments**: Stores comments for articles.

## Setup Instructions

### Prerequisites

1. Python installed on your system.
2. PostgreSQL database server running locally or remotely.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/task-management-system.git
   cd task-management-system
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   
3. Install the required dependencies:
   
   ```bash
   pip install -r requirements.txt
4. Set up the .env file: Ensure .env contains the following:
   
   ```bash
   DB_CONNECTION=postgresql+psycopg2
   DB_HOST=localhost
   DB_PORT=5432
   DB_DATABASE=task3_db
   DB_USERNAME=postgres
   DB_PASSWORD=2222
   
### Running Migrations

1. Initialize Alembic:
   
   ```bash
   alembic init migrations

2. Generate a migration:
   
   ```bash
    alembic revision --autogenerate -m "Initial migration"
   
3. Apply the migration:
   
   ```bash
    alembic upgrade head

### Database Models Diagram: 

<img width="1391" alt="Screenshot 2024-11-24 at 12 45 54 PM" src="https://github.com/user-attachments/assets/c00c20be-c99e-4ce1-898c-a2d855bd173a">


