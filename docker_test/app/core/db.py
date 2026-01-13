from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.settings import settings

# MySQL 연결 문자열 (PyMySQL 드라이버 사용)
# f"mysql+pymysql://{user}:{password}@{host}/{database}"
DATABASE_URL = (
    f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}/{settings.DB_NAME}"
)

# SQLAlchemy 엔진 생성
# pool_pre_ping=True는 연결이 끊어졌을 때 자동으로 재연결 시도
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# 세션 생성기
# autocommit=False는 변경사항을 명시적으로 commit해야 함을 의미 (권장)
# autoflush=False는 세션이 닫힐 때까지 변경사항을 DB에 즉시 동기화하지 않음
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# FastAPI 의존성 주입을 위한 제너레이터 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
