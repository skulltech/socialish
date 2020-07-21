from typing import Optional, List

from pydantic import BaseModel

import db


class User(BaseModel):
    id: str
    username: str
    joined_at: str
    email: str
    name: str
    bio: Optional[str] = None
    location: Optional[str] = None


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class Post(BaseModel):
    id: str
    created_at: str
    user: int
    text: str
    likes: List[str]


class Comment(Post):
    id: str
    parent: str
    text: str
    likes: List[str]


def get_user(id: str):
    user = db.get_user(id)
    if user:
        return UserInDB(**user)


def get_user_by_username(username: str):
    user = db.get_user_by_username(username)
    if user:
        return UserInDB(**user)
