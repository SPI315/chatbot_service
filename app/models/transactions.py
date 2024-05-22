from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from models.users import UserTable
from models.base import Base

user = UserTable()

class TransactionsTable(Base):
    __tablename__ = "transactions_table"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user_table.id"))
    user = relationship(UserTable, primaryjoin=user_id == UserTable.id)
    date = Column(TIMESTAMP)
    replenishment = Column(Integer)
    write_off = Column(Integer)
