from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import TodoCreate, TodoResponse
from app.models import Todo
from app.dependencies import get_db
from app.utils import get_current_user
from app.models import User

router = APIRouter(prefix = '/todos', tags = ['Todos'])

@router.post("", response_model= TodoResponse)
def create_todo(
    todo: TodoCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    
    ):
    new_todo = Todo(
        title = todo.title,
        completed = todo.completed,
        owner_id = current_user.id
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


@router.get("", response_model=list[TodoResponse])
def get_todos(
    db: Session = Depends(get_db),
    current_user:User = Depends(get_current_user)
              
              ):
    todos = db.query(Todo).filter(Todo.owner_id == current_user.id).all()
    return todos

@router.get('/{todo_id}', response_model=TodoResponse)
def get_todo(todo_id: int, db:Session=Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code = 404, detail = 'todo not found')
    
    return todo

@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail = 'Todo not found')
    

    db.delete(todo)
    db.commit()
    return {"message": "deleted"}
@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id:int, updated:TodoCreate, db:Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail = 'Todo not found')
    todo.title = updated.title
    todo.completed = updated.completed

    db.commit()
    db.refresh(todo)

    return todo