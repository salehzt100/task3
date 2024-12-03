from fastapi import APIRouter
from .routes import article, auth, category, comment, role, tag, user

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(article.router)
api_router.include_router(comment.router)
api_router.include_router(category.router)
api_router.include_router(role.router)
api_router.include_router(tag.router)
api_router.include_router(user.router)

