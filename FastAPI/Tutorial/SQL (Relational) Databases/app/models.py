from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(200), unique=True, index=True)
    hashed_password = Column(String(200))
    is_active = Column(Boolean, default=True)
    # relationship 속성을 이용하여 다른 테이블의 값에 포함시켜 준다.
    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True)
    description = Column(String(200), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    # relationship 속성을 이용하여 다른 테이블의 값에 포함시켜 준다.
    owner = relationship("User", back_populates="items")