from pydantic import BaseModel, EmailStr
from datetime import datetime
from fastapi.param_functions import Form


class User(BaseModel):
    email: EmailStr 
    password: str
    is_active: bool = False
    last_login: datetime = None
    expired_time: datetime = None


class loginForm():
    email:str = Form()
    password:str = Form()


class UserReponse(BaseModel):
    email: EmailStr
    is_active: bool = False

    
def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message
    }


def ErrorResponseModel(error, code, message):
    return {
        "error": error,
        "code": code, 
        "message": message
    }
