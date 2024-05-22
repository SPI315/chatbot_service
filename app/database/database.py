import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from models.base import Base
from models.users import UserTable
from models.data import DataTable
from models.transactions import TransactionsTable

env_path = os.path.join(sys.path[0], ".env")
load_dotenv(env_path)
url = os.getenv("SQLALCHEMY_DATABASE_URL")
engine = create_engine(url)
SessionLocal = sessionmaker(autoflush=False, bind=engine)

def get_db():
    with SessionLocal() as session:
        yield session

def db_init():
    Base.metadata.create_all(bind=engine)