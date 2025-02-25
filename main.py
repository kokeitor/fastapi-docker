from fastapi import FastAPI, Depends
import pathlib
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker, Session
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

    def __repr__(self):
        return f"Clients(id={self.id}, name='{self.name}', timestamp='{self.timestamp}')"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "timestamp": self.timestamp
        }


BASE.metadata.create_all(engine)


class requestModel(BaseModel):
    clientName: str


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/')
def hello_world(request: requestModel,  db: Session = Depends(get_db)):

    client = Clients(name=request.clientName)
    print(
        f"Before insert >> Searching for name {client.name} in bbdd >> {db.query(Clients).filter(Clients.name == request.clientName).first()})")
    db.add(client)
    print(
        f"After insert >> Searching for name {client.name} in bbdd >> {db.query(Clients).filter(Clients.name == request.clientName).first()})")

    path = pathlib.Path(__file__).parent.absolute()
    file_path = path / 'data' / 'data.txt'
    print(f"Writing to file {file_path} >> {client.name}")
    with open(file_path, 'w') as f:
        f.write(client.name)
    return {'response': f'Created client >> {client}'}
