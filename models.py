import datetime
import uuid
from typing import Optional, List

from pydantic import BaseModel

import db
import security


class User(BaseModel):
    user_id: str
    username: str
    joined_at: str
    email: str
    name: str
    superuser: Optional[bool] = False
    bio: Optional[str] = None
    location: Optional[str] = None


class UserInDB(User):
    hashed_password: str


class UserForm(BaseModel):
    username: str
    email: str
    name: str
    bio: Optional[str] = None
    location: Optional[str] = None
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class Post(BaseModel):
    post_id: str
    created_at: str
    user: int
    text: str
    likes: List[str]


class Comment(Post):
    comment_id: str
    parent: str
    text: str
    likes: List[str]


def get_user(user_id: str):
    user = db.get_user(user_id)
    if user:
        return UserInDB(**user)


def get_user_by_username(username: str):
    user = db.get_user_by_username(username)
    if user:
        return UserInDB(**user)


def create_user(username: str, email: str, name: str, bio: str, location: str, password: str,
                superuser: Optional[bool] = False):
    if get_user_by_username(username):
        return
    while True:
        user = db.create_user(user_id=uuid.uuid4().hex, username=username, email=email, name=name, bio=bio,
                              location=location, hashed_password=security.get_password_hash(password),
                              joined_at=datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat(),
                              superuser=superuser)
        if user:
            return user


def update_user(user_id: str, username: str, email: str, name: str, password: str, superuser: Optional[bool] = False,
                bio: Optional[str] = None, location: Optional[str] = None):
    return db.update_user(user_id=user_id, username=username, email=email, name=name, bio=bio or '',
                          location=location or '', superuser=superuser,
                          hashed_password=security.get_password_hash(password))


users = [
    {
        'username': 'sumit',
        'email': 'sumit.ghosh32@gmail.com',
        'name': 'Sumit Ghosh',
        'bio': 'INTP. Programmer.',
        'location': 'New Delhi',
        'password': 'secret',
        'superuser': True
    }
]
for user in users:
    create_user(**user)
