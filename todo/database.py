from fastapi import FastAPI
# Import necessary modules and classes
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base


app = FastAPI()

# Database setup
DATABASE_URL = "sqlite:///./todoapp.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()