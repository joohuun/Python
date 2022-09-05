from pydantic import BaseModel

'''
SQLAlchemy 모델과 Pydantic 모델간의 혼동을 피하기 위해 
SQLAlchemy 모델이 있는 파일 models.py과 schemas.py Pydantic 모델이 있는 파일이 있습니다.
이 Pydantic 모델은 "스키마"(유효한 데이터 모양)를 어느 정도 정의합니다.
따라서 둘 다 사용하는 동안 혼동을 피하는 데 도움이 됩니다.
'''

class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True