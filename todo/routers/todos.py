from fastapi import Depends, HTTPException,Path
import models
from typing import Annotated
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from models import Todo
from pydantic import BaseModel,Field
from routers import auth
from fastapi import APIRouter
from pyd import TodoRequest


router = APIRouter()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
db_dependency = Annotated[Session,Depends(get_db)]



# class TodoRequest(BaseModel):
#     title : str = Field(min_length=3)
#     description: str = Field(max_length=100, min_length= 3)
#     priority : int = Field(gt=0,lt=6)
#     complete: bool
    


@router.get('/get')
async def get_all_data(db:db_dependency):
    return db.query(Todo).all()


@router.get("/getid/{db_id}")
async def get_book_by_id(db:db_dependency,db_id:int = Path(gt=0)):
    db_model = db.query(Todo).filter(Todo.id == db_id).first()
    if db_model:
        return db_model
    raise HTTPException(status_code=404,detail="Not Found ID")
    
    
@router.post("/createTask/")
async def create_task(db:db_dependency, todo_Req: TodoRequest):
    todo_model = Todo(**todo_Req.dict())
    db.add(todo_model)
    db.commit()
    

@router.put("/updateTodo/{to_do_id}")
async def update_task(db: db_dependency, to_do_id: int,todo_req :TodoRequest):
    todo_model = db.query(Todo).filter(Todo.id == to_do_id).first()
    if not todo_model:
        raise HTTPException(status_code=404,detail="Not found")
    todo_model.title = todo_req.title
    todo_model.description = todo_req.description
    todo_model.complete = todo_req.complete
    todo_model.priority = todo_req.priority
    
    db.add(todo_model)
    db.commit()
    

@router.delete("/delete/{todo_id}")
async def delete(db:db_dependency, todo_id:int):
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo_model:
        raise HTTPException(status_code=404, detail="Not found id")
    db.query(Todo).filter(Todo.id == todo_id).delete()
    db.commit()
    
         