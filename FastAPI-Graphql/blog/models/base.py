from sqlalchemy import Column, Integer, String, Time
from database.database import Base


class BaseModel(Base):
    created_at = Column(Time)
    updated_at = Column
