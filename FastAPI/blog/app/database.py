from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

# 외부 DB와 연동하기 위한 SQLAlchemy 엔진 생성, 이 엔진은 다른곳에서 사용 될 것이다.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}, 
    # echo = True,
)
# 세션로컬 클래스 생성
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)

# 베이스 클래스 생성
Base = declarative_base()

# 종속성 생성 단일 요청에 사용될 SQLAchemy 세션 생성, 요청 완료시 종료
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()