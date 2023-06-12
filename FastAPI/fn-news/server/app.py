from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from pymongo import MongoClient
# from pydantic.networks import EmailError
import smtplib
from typing import Union, Any, Optional
from datetime import datetime, timedelta
import jwt
from email.message import EmailMessage
from fastapi.param_functions import Form

# from env import (
#     smtp_email,
#     smtp_pw,
#     ALGORITHM,
#     JWT_SECRET_KEY,
#     MONGO_URI
# )

import os

app = FastAPI()

JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY')
ALGORITHM=os.environ.get('ALGORITHM')
smtp_email=os.environ.get('SMTP_EMAIL')
smtp_pw=os.environ.get('SMTP_PW')


# MongoDB setup
client = MongoClient(os.environ.get("MONGO_URI"))
db = client['mydatabase']
users_collection = db['users']

# Password hashing setup
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# OAuth2 password bearer setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


class User(BaseModel):
    email: EmailStr 
    password: str
    is_active: bool = False
    last_login: datetime = None
    expired_time: datetime = None


class OAuth2PasswordRequestForm():
    def __init__(
        self,
        # grant_type: str = Form(default=None, regex="password"),
        email: str = Form(),
        password: str = Form(), 
        scope: str = Form(default=""),
        client_id: Optional[str] = Form(default=None),
        client_secret: Optional[str] = Form(default=None),
    ):
        # self.grant_type = grant_type
        self.email = email
        self.password = password
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(email):
    return users_collection.find_one({'email':email})


def generate_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now() + expires_delta
    else:
        expires_delta = datetime.now() + timedelta(minutes=30)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encode_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return [encode_jwt, to_encode]


@app.post('/register')
async def register(user: User):
    existing_user = get_user(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail='email already registered')

    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
    user_dict['password'] = hashed_password
    users_collection.insert_one(user_dict)
    send_verification_email(user.email)
    return {'message': 'User registered successfully'}


def send_verification_email(email):
    verification_url = "http://localhost:8000/verify?email=" + email
    msg = EmailMessage()
    msg["Subject"] = "fn-news Email Verification"
    msg["From"] = "noreply@example.com"
    msg["To"] = email
    msg.set_content(f"Click the link to verify your email: {verification_url}")

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(smtp_email, smtp_pw)
        smtp.send_message(msg)


@app.get("/verify")
async def verify_email(email: str):
    user = users_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    users_collection.update_one({"email": email}, {"$set": {"is_active": True}})
    return {"message": "Email verified successfully"}


@app.post('/login')
async def login(user: OAuth2PasswordRequestForm = Depends()):
    email = user.email
    password = user.password
    user = get_user(email)
    if not user or not verify_password(password, user['password']):
        raise HTTPException(status_code=400, detail='Incorrect email or password')

    if not user['is_active']:
        raise HTTPException(status_code=400, detail='User is not active')
    users_collection.update_one({'email': email}, {"$set": {'last_login': datetime.now()}})
    token = generate_token(user['email'])
    exp = token[1]['exp']
    users_collection.update_one({'email': email}, {"$set": {'expired_time': exp}})
    return {'access_token': token, 'token_type': 'bearer'}