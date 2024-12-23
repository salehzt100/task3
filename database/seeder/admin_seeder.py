from sqlalchemy.orm import Session
from app.models import User
from bootstrap import get_db
from core.security import hash_password
from core.config import settings


def seed_admin_user():
    # Define the admin user details
    admin_user = {
        'name': settings.ADMIN_USER['name'],
        "username": settings.ADMIN_USER['username'],
        "password": settings.ADMIN_USER['password'],
        'is_active': True,
        "role_id": 1
    }

    # Get a database session from the generator
    db_generator = get_db()
    db: Session = next(db_generator)

    try:
        # Check if the admin user already exists
        existing_user = db.query(User).filter_by(username=admin_user["username"]).first()

        if existing_user is None:
            # Create a new admin user
            new_user = User(
                name=admin_user["name"],
                username=admin_user["username"],
                password=hash_password(admin_user["password"]),
                is_active=True,
                role_id=admin_user["role_id"]
            )
            db.add(new_user)
            db.commit()
            print(f"Successfully added admin user: {new_user.username}")
        else:
            print("Admin user already exists. No new user added.")

    except Exception as e:
        db.rollback()
        print(f"Error occurred while adding admin user: {str(e)}")
    finally:
        db.close()
        # Ensure generator cleanup
        db_generator.close()


# Run the script
if __name__ == "__main__":
    seed_admin_user()