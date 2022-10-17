from sqlalchemy.orm import Session
from app import models, schemas

def get_book(db:Session, book_id:int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_books(db:Session, skip:int=0, limit:int=100):
    return db.query(models.Book).offset(skip).limit(limit).all()

def create_book(db:Session, book:schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
    