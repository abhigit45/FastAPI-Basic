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
    prefix='/todos',
    tags=['todos']
)



# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
    
db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]



# class TodoRequest(BaseModel):
#     title : str = Field(min_length=3)
#     description: str = Field(max_length=100, min_length= 3)
#     priority : int = Field(gt=0,lt=6)
#     complete: bool
    


@router.get('/get')
async def get_all_data(user:user_dependency,db:db_dependency):
    if user is None:
        HTTPException(detail="User Not authenticate")
    return db.query(Todo).filter(Todo.owner_id == user.get('id')).all()


@router.get("/getid/{db_id}")
async def get_book_by_id(user:user_dependency,db:db_dependency,db_id:int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User not found")
    
    db_model = db.query(Todo).filter(Todo.id == db_id).filter(Todo.owner_id == user.get('id')).first()
    if db_model:
        return db_model
    raise HTTPException(status_code=404,detail="Not Found ID")
    
    
@router.post("/todo")
async def create_task(user:user_dependency,db:db_dependency, todo_Req: TodoRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User not found")
    todo_model = Todo(**todo_Req.dict(),owner_id = user.get('id'))
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model
    

@router.put("/updateTodo/{to_do_id}")
async def update_task(user:user_dependency,db: db_dependency, to_do_id: int,todo_req :TodoRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User not found")
    
    todo_model = db.query(Todo).filter(Todo.id == to_do_id).filter(Todo.owner_id == user.get('id')).first()
    if not todo_model:
        raise HTTPException(status_code=404,detail="Not found")
    todo_model.title = todo_req.title
    todo_model.description = todo_req.description
    todo_model.complete = todo_req.complete
    todo_model.priority = todo_req.priority
    
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model
    

@router.delete("/delete/{todo_id}")
async def delete(user: user_dependency,db:db_dependency, todo_id:int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User not found")
    
    todo_model = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user.get('id')).first()
    if not todo_model:
        raise HTTPException(status_code=404, detail="Not found id")
    db.query(Todo).filter(Todo.id == todo_id).delete()
    db.commit()
    
         