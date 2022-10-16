from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app import token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# get_current_user의 종속성 생성, 하위 종속성에 oauth2_scheme 받는다.
async def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return token.verify_token(data, credentials_exception)