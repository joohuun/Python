from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app import schemas, database, models, token
from app.hashing import Hash
from sqlalchemy.orm import Session

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(db:Session=Depends(database.get_db), request: OAuth2PasswordRequestForm=Depends()):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid Credentials")
    if not Hash.verify_password(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Incorrect password")
        
    access_token = token.create_access_token(data={"sub":user.email})
    return {"acces_token": access_token, "token_type":"bearer"}