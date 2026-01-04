# Import necessary modules and classes
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String,text
import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from sqlalchemy.pool import StaticPool
# from todo.database import Base,SessionLocal,engine
from todo.main import app
from todo.routers.users import get_db,get_current_user
from fastapi.testclient import TestClient
from starlette import status
from fastapi import FastAPI
from todo import models
from todo.database import Base
import pytest
from todo.models import Todo

# FastAPI app instance
# app = FastAPI()

# Database setup
DATABASE_URL = "sqlite:///./test.db"
# DATABASE_URL = "sqlite://"
# DATABASE_URL = "sqlite://"
# SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(DATABASE_URL,connect_args={'check_same_thread':False},poolclass=StaticPool)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = sqlalchemy.orm.declarative_base()

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {'username':'Abhishek','id':1,'user_role':'admin'}

        
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


client = TestClient(app)


@pytest.fixture
def test_todo():
    todo = Todo(
        title='Learn code',
        description='need to learn everyday',
        priority=5,
        complete = False,
        owner_id = 1,
        
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("Delete from todos"))
        connection.commit()



def test_read_all_authenticated(test_todo):
    response = client.get('/get')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete':False,'title':'Learn code','description':'need to learn everyday',
                                'id':1,
                                'priority':5,
                                'owner_id':1}]



def test_read_one_authenticated(test_todo):
    response = client.get('/getid/1')
    assert response.status_code == status.HTTP_200_OK
    data =  response.json()
 
    assert data["title"] == "Learn code"
    assert data["description"] == "need to learn everyday"
    assert data["priority"] == 5
    assert data["complete"] is False
    assert data["owner_id"] == 1
    
    
def test_create_todo(test_todo):
    request_data = {
        'title':'new todo',
        'description':'new todo desc',
        'complete':False,
        'priority':5,
    }
    response = client.post('/todo/',json=request_data)
   
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "new todo"
    assert data["priority"] == 5
    assert data["owner_id"] == 1
    
    
    
def test_update_todo(test_todo):
    request_data = {
        'title':'updating existing todo',
        'description':'new todo desc',
        'complete':False,
        'priority':5,
    }
    response = client.put('/updateTodo/1',json=request_data)
   
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "updating existing todo"
    assert data["priority"] == 5
    assert data["owner_id"] == 1
  
  
  
    
def test_delete_todo(test_todo):
    response = client.delete("/delete/1")
    assert response.status_code == status.HTTP_200_OK

    response = client.get("/getid/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    
  