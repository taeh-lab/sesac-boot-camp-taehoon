from fastapi import FastAPI
from app.api.routes import todos
from app.models.todo import Base  # SQLAlchemy Base 모델 가져오기
from app.core.db import engine    # DB 엔진 가져오기

# SQLAlchemy 모델에 정의된 모든 테이블을 데이터베이스에 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(todos.router)
