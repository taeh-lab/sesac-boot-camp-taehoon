from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repository import todo_repository
from app.models.todo import Todo as TodoModel

def create_todo(db: Session, content: str) -> TodoModel:
    return todo_repository.create_todo_db(db=db, content=content)

def get_todos(db: Session) -> list[TodoModel]:
    return todo_repository.get_all_todos_db(db=db)

def delete_todo(db: Session, todo_id: int):
    affected = todo_repository.delete_todo_db(db=db, todo_id=todo_id)
    if affected == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted"}

