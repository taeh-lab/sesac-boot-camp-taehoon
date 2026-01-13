from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# SQLAlchemy 모델의 기본 클래스
Base = declarative_base()

# 'todo' 테이블과 매핑될 SQLAlchemy 모델
class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
