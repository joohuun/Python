from sqlalchemy import Column, Integer, String
from database.database import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    
