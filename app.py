from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestFormStrict
from mangum import Mangum

from models import User, Token
from security import authenticate_user, create_access_token, get_current_user, oauth2_scheme

ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()


@app.get('/items')
async def read_items(token: str = Depends(oauth2_scheme)):
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
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


handler = Mangum(app)
