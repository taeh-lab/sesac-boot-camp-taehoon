from datetime import datetime
from pydantic import BaseModel

# 공통 필드를 가진 기본 스키마
class TodoBase(BaseModel):
    content: str

# 새로운 Todo를 생성할 때 사용할 요청 스키마
class TodoCreate(TodoBase):
    pass

# API 응답으로 사용할 스키마
class TodoResponse(TodoBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
