from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 데이터베이스 엔진 생성 (설정 파일의 DATABASE_URL 사용)
engine = create_engine(settings.DATABASE_URL)

# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    FastAPI의 Dependency Injection을 위한 데이터베이스 세션 생성 및 종료 함수.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
