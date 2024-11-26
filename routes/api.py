from fastapi import FastAPI, Query, Depends
from typing import List, Optional, Union
from datetime import datetime
from sqlalchemy.orm import Session
from database import get_db

from schema import (
    RegisterRequestBody,
    LoginRequestBody,
    UserRequestBody,
    UserResponse,
    TagRequestBody,
    TagResponse,
    CategoryRequestBody,
    CategoryResponse,
    ArticleRequestBody,
    ArticleResponse,
    ArticleStatus,
    CommentRequestBody,
    CommentResponse,
    RoleRequestBody,
    RoleResponse,
    PermissionResponse,
    RolePermissionRequestBody,
)

from Controllers import (
    AuthController,
)

app = FastAPI()

''' AUTH APIs '''
@app.post("/register", tags=['Auth'])
async def register( user: RegisterRequestBody, db: Session = Depends(get_db)):

    return AuthController.register(user, db )

@app.post("/login", tags=['Auth'])
async def login(body: LoginRequestBody):
    pass

@app.post("/logout", tags=['Auth'])
async def logout():
    pass

''' USER APIs '''
@app.get('/users', response_model=List[UserResponse], tags=["Users"])
async def list_users():
    pass

@app.get('/users/{user_id}', response_model=UserResponse, tags=["Users"])
async def show_user(user_id: int):
    pass

@app.post('/users', response_model=UserResponse, tags=["Users"])
async def create_user(user_body: UserRequestBody):
    pass

@app.put('/users/{user_id}', response_model=UserResponse, tags=["Users"])
async def update_user(user_id: int, user_body: UserRequestBody):
    pass

@app.delete('/users/{user_id}', response_model=dict, tags=["Users"])
async def delete_user(user_id: int):
    pass

''' TAGS APIs '''
@app.get('/tags', response_model=List[TagResponse], tags=["Tags"])
async def list_tags():
    pass

@app.get('/tags/{tags_id}', response_model=TagResponse, tags=["Tags"])
async def show_tag(tags_id: int):
    pass

@app.post('/tags', response_model=TagResponse, tags=["Tags"])
async def create_tag(tag_body: TagRequestBody):
    pass

@app.put('/tags/{tag_id}', response_model=TagResponse, tags=["Tags"])
async def update_tag(tag_id: int, tag_body: TagRequestBody):
    pass

@app.delete('/tags/{tag_id}', response_model=dict, tags=["Tags"])
async def delete_tag(tag_id: int):
    pass

''' CATEGORIES APIs '''
@app.get('/categories', response_model=List[CategoryResponse], tags=["Categories"])
async def list_category():
    pass

@app.get('/categories/{category_id}', response_model=CategoryResponse, tags=["Categories"])
async def show_category(category_id: int):
    pass

@app.post('/categories', response_model=CategoryResponse, tags=["Categories"])
async def create_category(category_body: CategoryRequestBody):
    pass

@app.put('/categories/{category_id}', response_model=CategoryResponse, tags=["Categories"])
async def update_category(category_id: int, category_body: CategoryRequestBody):
    pass

@app.delete('/categories/{category_id}', response_model=dict, tags=["Categories"])
async def delete_category(category_id: int):
    pass

''' ARTICLES APIs '''
@app.get('/articles', response_model=List[ArticleResponse], tags=["Articles"])
async def list_articles(
    search: Optional[str] = Query(None, description="Search"),
    filter_type: Optional[str] = Query(None, description="Type of filter"),
    filter_value: Optional[Union[str, ArticleStatus, datetime]] = Query(None, description="Value for the selected filter type"),
):
    pass

@app.get('/articles/{article_id}', response_model=ArticleResponse, tags=["Articles"])
async def show_article(article_id: int):
    pass

@app.post('/articles', response_model=ArticleResponse, tags=["Articles"])
async def create_article(article_body: ArticleRequestBody):
    pass

@app.put('/articles/{article_id}', response_model=ArticleResponse, tags=["Articles"])
async def update_article(article_id: int, article_body: ArticleRequestBody):
    pass

@app.delete('/articles/{article_id}', response_model=dict, tags=["Articles"])
async def delete_article(article_id: int):
    pass

''' COMMENTS APIs '''
@app.get('/articles/{article_id}/comments', response_model=List[CommentResponse], tags=["Comments"])
async def list_comments(article_id: int):
    pass

@app.post('/articles/{article_id}/comments', response_model=CommentResponse, tags=["Comments"])
async def create_comment(article_id: int, body: CommentRequestBody):
    pass

''' ROLES APIs '''
@app.get('/roles', response_model=List[RoleResponse], tags=["Roles"])
async def list_role():
    pass

@app.get('/roles/{role_id}', response_model=RoleResponse, tags=["Roles"])
async def show_role(role_id: int):
    pass

@app.post('/roles', response_model=RoleResponse, tags=["Roles"])
async def create_role(role_body: RoleRequestBody):
    pass

@app.put('/roles/{role_id}', response_model=RoleResponse, tags=["Roles"])
async def update_role(role_id: int, role_body: RoleRequestBody):
    pass

@app.delete('/roles/{role_id}', response_model=dict, tags=["Roles"])
async def delete_role(role_id: int):
    pass

''' PERMISSIONS APIs '''
@app.get('/permissions', response_model=List[PermissionResponse], tags=["Permissions"])
async def list_permission():
    pass

@app.get('/roles/{role_id}/permissions', response_model=List[PermissionResponse], tags=["Permissions"])
async def list_permissions_assigned_to_role(role_id: int):
    pass

@app.post('/roles/{role_id}/permissions', response_model=dict, tags=["Permissions"])
async def assign_permissions_to_role(role_id: int, body: RolePermissionRequestBody):
    pass

@app.patch('/roles/{role_id}/permissions', response_model=dict, tags=["Permissions"])
async def update_permissions_for_role(role_id: int, body: RolePermissionRequestBody):
    pass

@app.delete('/roles/{role_id}/permissions', response_model=dict, tags=["Permissions"])
async def revoke_permission_from_role(role_id: int, body: RolePermissionRequestBody):
    pass
