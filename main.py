from fastapi import FastAPI
import pathlib
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Boolean
import datetime


load_dotenv()
# Get environment variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

print(f"DB_USER: {DB_USER}")
print(f"DB_PASSWORD: {DB_PASSWORD}")
print(f"DB_NAME: {DB_NAME}")
print(f"DB_HOST: {DB_HOST}")
print(f"DB_PORT: {DB_PORT}")


# Database URI string
DB_URI: str = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


""" 
engine = create_engine(DB_URI)
SessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False)


BASE = declarative_base()


class Clients(BASE):
    __tablename__ = "clients"

    id = Column(Integer, autoincrement=True, unique=True,
                nullable=False, primary_key=True)
    name = Column(String(50), nullable=False)
    timestamp = Column(DateTime, nullable=False,
                       default=datetime.datetime.now())

"""


class requestModel(BaseModel):
    clientName: str


app = FastAPI()


@app.post('/')
def hello_world(request: requestModel):

    path = pathlib.Path(__file__).parent.absolute()
    file_path = path / 'data' / 'data.txt'
    print(file_path)
    print(request.clientName)
    with open(file_path, 'w') as f:
        f.write(request.clientName)
    return {'response': f'clientName : {request.clientName}'}
