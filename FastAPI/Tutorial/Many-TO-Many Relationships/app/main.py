from unittest import skip
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import models, crud, schemas
from app.database import SessionLocal, engine

# 디비 테이블 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@app.post("/items/", response_model=schemas.BookSchema)
def create_book_for_user(
    book:schemas.BookCreate, db:Session=Depends(get_db)
):
    return crud.create_book(db=db, book=book)

@app.get("/books/", response_model=list[schemas.BookSchema])
async def get_book(limit: int=100, db:Session=Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books