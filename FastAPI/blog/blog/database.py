from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# import pymsql

# SQLALCHAMY_DATABASE_URL = 'mysql://root@localhost:3306/tset_db?charset=utf8'
SQLALCHAMY_DATABASE_URL = "postgresql://juhoon:8105@localhost:5433/blog"

# engine = create_engine(SQLALCHAMY_DATABASE_URL, connect_args={
#                        "check_same_thread": False})

engine = create_engine(
    SQLALCHAMY_DATABASE_URL,
    # connect_args={"check_same_thread": False}, 
    echo = True,
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()