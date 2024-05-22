import os
import sys
from dotenv import load_dotenv
import pytest
from fastapi.testclient import TestClient
from fastapi.security import OAuth2PasswordRequestForm
from api import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from database.database import get_db
from sqlalchemy.pool import StaticPool
from auth.authenticate import authenticate

from models.users import UserTable
from models.data import DataTable
from models.transactions import TransactionsTable

env_path = os.path.join(sys.path[0], ".env")
load_dotenv(env_path)
url = os.getenv("SQLALCHEMY_DATABASE_URL")
engine = create_engine(url, poolclass=StaticPool)
Session = sessionmaker(autoflush=False, bind=engine)


@pytest.fixture(name="session")
def session_fixture():
    Base.metadata.create_all(bind=engine)
    with Session() as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override
    app.dependency_overrides[OAuth2PasswordRequestForm] = lambda: OAuth2PasswordRequestForm(
        username="test_3@mail.ru", password="123"
    )
    app.dependency_overrides[authenticate] = lambda: "test_3@mail.ru"

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
