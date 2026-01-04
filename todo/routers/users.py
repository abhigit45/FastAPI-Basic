from fastapi import Depends, HTTPException,Path

from typing import Annotated
from todo.database import SessionLocal, engine,get_db
from sqlalchemy.orm import Session
from todo.models import Todo,Users
from pydantic import BaseModel,Field
# from routers import auth
from fastapi import APIRouter
from todo.pyd import UserVerification
from .auth import get_current_user
from starlette import status
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

router = APIRouter(
    prefix='/Users',tags=['Users']
)



# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
    
db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]


@router.get('/grtCurrentUsers')
async def get_active_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User not found")
    return db.query(Users).filter(Users.is_active == "true").first()



@router.get('/myProfile')
async def myProfile(user:user_dependency, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User not found")
    return db.query(Users).filter(Users.id == user.get('id')).first()




@router.put('/changePassword')
async def changePass(user:user_dependency,db:db_dependency,user_ver: UserVerification):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User not found")
    todo_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if not bcrypt_context.verify(user_ver.password,todo_model.hash_password):
        raise HTTPException(status_code=401,detail="current password is wrong")
    todo_model.hash_password = user_ver.new_password
    db.add(todo_model)
    db.commit()
    
    
@router.put('/changesNumber')
async def changeNumber(user:user_dependency,db:db_dependency,num:str):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User not found")  
    number = db.query(Users).filter(Users.id == user.get('id')).first()
    if number is None:
        raise HTTPException(status_code=401,detail="number not found")
    number.phone_number = num
    db.add(number)
    db.commit()
        
    

    
    
    
        
    