from fastapi import APIRouter,Depends,HTTPException,Security
from todo.pyd import CreateUser, Token
from todo.models import Users,Todo
from passlib.context import CryptContext
from todo.database import SessionLocal,get_db
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt,JWTError
from pydantic import BaseModel
from datetime import timedelta,timezone,datetime
from starlette import status


SECRET_KEY = '3322a5f0e8c22da32e0818f8d05bdb715ee5f4705dc4c01218f944dbdb1d312a'
ALGORITHM = 'HS256'


router = APIRouter(
    prefix='/auth',tags=['auth']
)


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
# oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


    
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
    
db_dependency = Annotated[Session,Depends(get_db)]



def authenticate_user(username: str, password: str, db:db_dependency):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hash_password):
        return False
    return user


def create_access_token(username:str,user_id:int,role:str,expires_delta:timedelta):
    encode = {'sub':username,'id':user_id,'role':role}
    # expires = datetime.now(timezone.utc)
    expire = datetime.now(timezone.utc) + expires_delta 
    encode.update({'exp':expire})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)



async def get_current_user(token:Annotated[str,Security(oauth2_bearer)]):

    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str = payload.get('sub')
        user_id:str = payload.get('id')
        user_role:str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate user")
        return {'username':username,
                'id':user_id,
                'user_role':user_role}
    except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate user")

        




# @router.get("/userdemo/")
# async def auth():
#     return {"User":"Auth Page"}


    
@router.post("/")
async def create_user(db: db_dependency,create_user_req: CreateUser):
    user = Users(
        email = create_user_req.email,
        username = create_user_req.username,
        first_name = create_user_req.first_name,
        last_name = create_user_req.last_name,
        hash_password = bcrypt_context.hash(create_user_req.password),
        phone_number = create_user_req.phone_number,
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
# @router.get("/getUser/{user_id}")
# async def get_user_by_id(db:db_dependency,user_id:int):
#     todo_model = db.query(Users).filter(Users.id == user_id).first()
#     if not todo_model:
#         raise HTTPException(status_code=404, detail="Not found user")
#     return todo_model


@router.post("/token",response_model=Token)
async def login_Access_token(form_data: Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return "Authentication Failed"
    
    token = create_access_token(user.username,user.id,user.role,timedelta(minutes=20))
    
    
    return {'access_token': token,
            'token_type':'bearer'}