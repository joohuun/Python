from pydantic import BaseModel
from typing import List

class AuthorBase(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class BookBase(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True
        
class BookCreate(BookBase):
    pass

class BookSchema(BookBase):
    authors: List[AuthorBase]

class AuthorSchema(AuthorBase):
    books: List[BookBase]
