from sqlalchemy.orm import Session
from database import get_db
from models import Role


def seed_roles():
    roles = ["ADMIN", "EDITOR", "AUTHOR", "READER"]

    # Get a database session from the generator
    db_generator = get_db()
    db: Session = next(db_generator)

    try:
        # Check existing roles in the database
        existing_roles = {role.name for role in db.query(Role).all()}
        new_roles = [Role(name=role) for role in roles if role not in existing_roles]

        if new_roles:
            db.add_all(new_roles)
            db.commit()
            print(f"Successfully added roles: {[role.name for role in new_roles]}")
        else:
            print("All roles already exist. No new roles added.")

    except Exception as e:
        db.rollback()
        print(f"Error occurred while adding roles: {str(e)}")
    finally:
        db.close()
        # Ensure generator cleanup
        db_generator.close()


# Run the script
if __name__ == "__main__":
    seed_roles()
