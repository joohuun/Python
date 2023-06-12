from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder

from ..models.user import (
    User,
    loginForm,
    UserReponse,
    ResponseModel,
    ErrorResponseModel,
)

from ..database import (
    get_user,
    add_user,
)

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import smtplib
from typing import Union, Any, Optional
from datetime import datetime, timedelta
import jwt

from ..env import ALGORITHM, JWT_SECRET_KEY

router = APIRouter()

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def generate_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now() + expires_delta
    else:
        expires_delta = datetime.now() + timedelta(minutes=30)
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encode_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return [encode_jwt, to_encode]


@router.post('/register')
async def register(user: User):
    user_dict = user.dict()
    email = user_dict['email']
    existing_user = await get_user(email)
    if existing_user:
        raise HTTPException(status_code=400, detail='email already registered')
    hashed_password = get_password_hash(user.password)
    user_dict['password'] = hashed_password
    new_user = await add_user(user_dict)
    return f'{new_user}'



