from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.todo import TodoResponse, TodoCreate
from app.service import todo_service
from app.core.db import get_db

router = APIRouter()

@router.post("/todos", response_model=TodoResponse)
async def create_todo_route(todo: TodoCreate, db: Session = Depends(get_db)):
    if not todo.content:
        raise HTTPException(status_code=400, detail="content is required")
    return todo_service.create_todo(db=db, content=todo.content)

@router.get("/todos", response_model=list[TodoResponse])
def get_todos_route(db: Session = Depends(get_db)):
    return todo_service.get_todos(db=db)

@router.delete("/todos/{todo_id}")
def delete_todo_route(todo_id: int, db: Session = Depends(get_db)):
    return todo_service.delete_todo(db=db, todo_id=todo_id)
