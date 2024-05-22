from sqlalchemy import Column, Integer, String
from models.base import Base

class UserTable(Base):
    __tablename__ = "user_table"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    phone = Column(String)
    name = Column(String)
    surname = Column(String)
    user_password = Column(String)
    balance = Column(Integer)
    tg_id = Column(String)
