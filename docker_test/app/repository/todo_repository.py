from sqlalchemy.orm import Session
from app.models.todo import Todo as TodoModel

def create_todo_db(db: Session, content: str) -> TodoModel:
    new_todo = TodoModel(content=content)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

def get_all_todos_db(db: Session) -> list[TodoModel]:
    return db.query(TodoModel).all()

def delete_todo_db(db: Session, todo_id: int) -> int:
    todo_to_delete = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo_to_delete:
        return 0
    
    db.delete(todo_to_delete)
    db.commit()
    return 1
