from fastapi import Depends, HTTPException,Path

from typing import Annotated
from todo.database import SessionLocal, engine,get_db
from sqlalchemy.orm import Session
from todo.models import Todo
from pydantic import BaseModel,Field
# from routers import auth
from fastapi import APIRouter
from todo.pyd import TodoRequest
from .auth import get_current_user
from starlette import status



router = APIRouter(
    prefix='/admin',tags=['admin']
)



# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
    
db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]


@router.get('/todo')
async def read_all_admin(user:user_dependency,db:db_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=404, detail="Authentication failed")
    return db.query(Todo).all()
    

@router.delete('/delete/{todo_id}')
async def delete_todo(user: user_dependency, db:db_dependency,todo_id:int):
    if user is None or user.get('user_role') != 'Admin':
        raise HTTPException(status_code=404, detail="You are not authorized to delete this task")
    todo_model = db.query(Todo).filter(Todo.id==todo_id).first()
    if not todo_model:
        raise HTTPException(status_code=401,detail="To do not found")
    db.query(Todo).filter(Todo.id == todo_id).delete()
    db.commit()
    