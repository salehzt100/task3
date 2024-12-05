from uuid import UUID

from app.repositories.user_repository import UserRepository


class UserServices:
    @staticmethod
    def activate_user(db, user_id: UUID):
     return UserRepository.activate_user(db, user_id)

