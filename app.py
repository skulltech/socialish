from typing import Optional, List

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


class User(BaseModel):
    id: int
    username: str
    joined_at: str
    email: str
    name: str
    bio: Optional[str] = None
    location: Optional[str] = None


class Post(BaseModel):
    id: int
    created_at: str
    user: int
    text: str
    likes: List[int]


class Comment(Post):
    parent: int


@app.get('/')
def read_root():
    return {'Hello': 'World'}


@app.get('/items/{item_id}')
def read_item(item_id: int, q: Optional[str] = None):
    return {'item_id': item_id, 'q': q}


@app.put('/items/{item_id}')
def update_item(item_id: int, item: Item):
    return {'item_name': item.name, 'item_id': item_id}
