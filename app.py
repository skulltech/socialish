from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestFormStrict
from mangum import Mangum

import models
from models import User, Token, UserForm

from security import authenticate_user, create_access_token, get_current_user, oauth2_scheme

ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()


@app.get('/token')
async def get_token(token: str = Depends(oauth2_scheme)):
    return {'token': token}


@app.post('/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestFormStrict = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'sub': user.username}, expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}


@app.get('/users/me')
async def get_user_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.get('/users/{user_id}')
async def get_user(user_id: str, current_user: User = Depends(get_current_user)):
    if not current_user.superuser and user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Insufficient rights to resource'
        )
    if user_id != current_user.user_id:
        user = models.get_user(user_id)
    else:
        user = current_user
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return user


@app.get('/users')
async def get_user_by_username(username: str, current_user: User = Depends(get_current_user)):
    if not current_user.superuser and username != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Insufficient rights to resource'
        )
    if username != current_user.username:
        user = models.get_user_by_username(username)
    else:
        user = current_user
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return user


@app.put('/users/{user_id}')
async def update_user(user_id: str, user_form: UserForm, current_user: User = Depends(get_current_user)):
    if not current_user.superuser and user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Insufficient rights to resource'
        )
    user = models.update_user(user_id, **user_form.dict())
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return user

handler = Mangum(app)
