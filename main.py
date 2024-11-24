from datetime import datetime
from enum import Enum

from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional, Union

app = FastAPI()

''' AUTH Apis '''

class LoginRequestBody(BaseModel):
    username: str
    password: str

@app.post("/login", tags=['Auth'])
async def login(body: LoginRequestBody):
    pass

@app.post("/logout", tags=['Auth'])
async def logout():
    pass

''' USER APIs '''

class UserRequestBody(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str
    role_id: int

class UserResponse(BaseModel):
    id: int
    full_name: str
    role: str
    created_at: datetime



@app.get('/users', response_model=List[UserResponse], tags=["Users"])
async def list_users():
    """
    Retrieve a list of users.
    """
    pass

@app.get('/users/{user_id}', response_model=UserResponse, tags=["Users"])
async def show_user(user_id: int):
    """
    Retrieve details of a specific user by ID.
    """
    pass

@app.post('/users', response_model=UserResponse, tags=["Users"])
async def create_user(user_body: UserRequestBody):
    """
    Create a new user.
    """
    pass

@app.put('/users/{user_id}', response_model=UserResponse, tags=["Users"])
async def update_user(user_id: int, user_body: UserRequestBody):
    """
    Update an existing user's details.
    """
    pass

@app.delete('/users/{user_id}', response_model=dict, tags=["Users"])
async def delete_user(user_id: int):
    """
    Delete a user by ID.
    """
    pass

''' TAGS APIs '''

class TagRequestBody(BaseModel):
    name: str

class TagResponse(BaseModel):
    id: int
    name: str



@app.get('/tags', response_model=List[TagResponse], tags=["Tags"])
async def list_tag():
    """
    Retrieve a list of tags.
    """
    pass

@app.get('/tags/{tags_id}', response_model=TagResponse, tags=["Tags"])
async def show_tag(tags_id: int):
    """
    Retrieve details of a specific tag by ID.
    """
    pass

@app.post('/tags', response_model=TagResponse, tags=["Tags"])
async def create_tag(tag_body: TagRequestBody):
    """
    Create a new tag.
    """
    pass

@app.put('/tags/{tag_id}', response_model=TagResponse, tags=["Tags"])
async def update_tag(tag_id: int, tag_body: TagRequestBody):
    """
    Update an existing tag's details.
    """
    pass

@app.delete('/tags/{tag_id}', response_model=dict, tags=["Tags"])
async def delete_tag(tag_id: int):
    """
    Delete a tag by ID.
    """
    pass

''' CATEGORY APIs '''

class CategoryRequestBody(BaseModel):
    name: str

class CategoryResponse(BaseModel):
    id: int
    name: str



@app.get('/categories', response_model=List[CategoryResponse], tags=["Categories"])
async def list_category():
    """
    Retrieve a list of categories.
    """
    pass

@app.get('/categories/{category_id}', response_model=CategoryResponse, tags=["Categories"])
async def show_category(category_id: int):
    """
    Retrieve details of a specific category by ID.
    """
    pass

@app.post('/categories', response_model=CategoryResponse, tags=["Categories"])
async def create_category(category_body: CategoryRequestBody):
    """
    Create a new category.
    """
    pass

@app.put('/categories/{category_id}', response_model=CategoryResponse, tags=["Categories"])
async def update_category(category_id: int, category_body: CategoryRequestBody):
    """
    Update an existing category's details.
    """
    pass

@app.delete('/categories/{category_id}', response_model=dict, tags=["Categories"])
async def delete_category(category_id: int):
    """
    Delete a category by ID.
    """
    pass

''' ARTICLES APIs '''

class ArticleStatus(str, Enum):
    draft = "draft"
    in_review = "in_review"
    published = "published"
    rejected = "rejected"

class FilterType(str, Enum):
    status = "status"
    author = "author"
    date = "date"

class ArticleRequestBody(BaseModel):
    title: str
    body: str
    user_id: int
    status: ArticleStatus
    category_id: int

class ArticleResponse(BaseModel):
    id: int
    title: str
    body: str
    created_at: datetime
    status: ArticleStatus
    user: UserResponse
    category: CategoryResponse




@app.get('/articles', response_model=List[ArticleResponse], tags=["Articles"])
async def list_articles(
    search:Optional[str] = Query(None,
                                 description="Search"),
    filter_type: Optional[FilterType] = Query(None,
                                              description="Type of filter"),
    filter_value: Optional[Union[str, ArticleStatus, datetime]] = Query(
        None,
        description="value for the selected filter type"),
):
    """
    Retrieve a list of articles.
    """
    pass
@app.get('/articles/{article_id}', response_model=ArticleResponse, tags=["Articles"])
async def show_article(article_id: int):
    """
    Retrieve details of a specific article by ID.
    """
    pass

@app.post('/articles', response_model=ArticleResponse, tags=["Articles"])
async def create_article(article_body: ArticleRequestBody):
    """
    Create a new article.
    """
    pass

@app.put('/articles/{article_id}', response_model=ArticleResponse, tags=["Articles"])
async def update_article(article_id: int, article_body: ArticleRequestBody):
    """
    Update an existing article's details.
    """
    pass

@app.delete('/articles/{article_id}', response_model=dict, tags=["Articles"])
async def delete_article(article_id: int):
    """
    Delete an article by ID.
    """

    pass



''' Comments APIs '''


class CommentRequestBody(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: int
    content: str
    user: UserResponse
    article_id: int
    created_at: datetime

@app.get('/articles/{article_id}/comments', response_model=List[CommentResponse], tags=["Comments"])
async def list_comments(article_id: int):
    """
    Retrieve comments for a specific article.
    """
    pass

@app.post('/articles/{article_id}/comments', response_model=CommentResponse, tags=["Comments"])
async def create_comment(article_id: int,body: CommentRequestBody):
    """
    Add a comment to a specific article.
    """
    pass


''' ROLES APIs '''

class RoleRequestBody(BaseModel):
    name: str

class RoleResponse(BaseModel):
    id: int
    name: str


@app.get('/roles', response_model=List[RoleResponse], tags=["Roles"])
async def list_role():
    """
    Retrieve a list of roles.
    """
    pass

@app.get('/roles/{role_id}', response_model=RoleResponse, tags=["Roles"])
async def show_role(role_id: int):
    """
    Retrieve details of a specific role by ID.
    """
    pass

@app.post('/roles', response_model=RoleResponse, tags=["Roles"])
async def create_role(role_body: RoleRequestBody):
    """
    Create a new role.
    """
    pass

@app.put('/roles/{role_id}', response_model=RoleResponse, tags=["Roles"])
async def update_role(role_id: int, role_body: RoleRequestBody):
    """
    Update an existing role's details.
    """
    pass

@app.delete('/roles/{role_id}', response_model=dict, tags=["Roles"])
async def delete_role(role_id: int):
    """
    Delete a role by ID.
    """
    pass

''' PERMISSIONS APIs '''

class PermissionResponse(BaseModel):
    id: int
    name: str

class RolePermissionRequestBody(BaseModel):
    role_id: int
    permissions: List[int]


@app.get('/permissions', response_model=List[PermissionResponse], tags=["Permissions"])
async def list_permission():
    """
    Retrieve a list of permissions.
    """
    pass

@app.get('/roles/{role_id}/permissions', response_model=List[PermissionResponse], tags=["Permissions"])
async def list_permissions_assigned_to_role(role_id: int):
    """
    List permissions assigned to a specific role by ID.
    """
    pass

@app.post('/roles/{role_id}/permissions', response_model=dict, tags=["Permissions"])
async def assign_permissions_to_role(role_id: int, body: RolePermissionRequestBody):
    """
    Assign a permission to a role.
    """
    pass

@app.patch('/roles/{role_id}/permissions', response_model=dict, tags=["Permissions"])
async def async_permission_to_role(role_id: int, body: RolePermissionRequestBody):
    """
     Update permissions for a specific role by ID.
     """
    pass

@app.delete('/roles/{role_id}/permissions', response_model=dict, tags=["Permissions"])
async def revoke_permission_from_role(role_id: int, body: RolePermissionRequestBody):

    """
      Revoke permissions from a specific role by ID.
      """
    pass




