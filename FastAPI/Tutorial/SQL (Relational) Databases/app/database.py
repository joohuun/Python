from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# SQLALCHEMY_DATABASE_URL = "sqlite:///./폴더이름/디비이름.db"
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app/sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postdb"

# Mysql
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:5781@localhost:3306/testdb?charset=utf8"

# 외부 DB와 연동하기 위한 SQLAlchemy 엔진 생성, 이 엔진은 다른곳에서 사용 될 것이다.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # connect_args={"check_same_thread": False}, 
    echo = True,
)
# 세션로컬 클래스 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 베이스 클래스 생성
Base = declarative_base()