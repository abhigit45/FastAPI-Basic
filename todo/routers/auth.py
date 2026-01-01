from fastapi import APIRouter,Depends,HTTPException
from pyd import CreateUser
from models import Users
from passlib.context import CryptContext
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated

router = APIRouter()


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
db_dependency = Annotated[Session,Depends(get_db)]

@router.get("/auth/")
async def auth():
    return {"User":"Auth Page"}


    
@router.post("/createUser/")
async def create_user(db: db_dependency,create_user_req: CreateUser):
    user = Users(
        email = create_user_req.email,
        username = create_user_req.username,
        first_name = create_user_req.first_name,
        last_name = create_user_req.last_name,
        hash_password = bcrypt_context.hash(create_user_req.password),
        role = create_user_req.role,
        is_active = True
        
        
    )
    db.add(user)
    db.commit()

#get all users
@router.get("/getUsers/")
async def get_Users(db: db_dependency):
    todo_model = db.query(Users).all()
    return todo_model
    

#get user by id
@router.get("/getUser/{user_id}")
async def get_user_by_id(db:db_dependency,user_id:int):
    todo_model = db.query(Users).filter(Users.id == user_id).first()
    if not todo_model:
        raise HTTPException(status_code=404, detail="Not found user")
    return todo_model
    