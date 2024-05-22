from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from models.users import UserTable
from models.base import Base

user = UserTable()

class DataTable(Base):
    __tablename__ = "data_table"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user_table.id"))
    user = relationship(UserTable, primaryjoin=user_id == UserTable.id)
    request_date = Column(TIMESTAMP)
    input_data = Column(String)
    output_data = Column(String)
