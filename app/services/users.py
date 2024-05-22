from models.users import UserTable
from database.database import SessionLocal
from loguru import logger


# класс для пользователей
class User:
    def __init__(
        self,
        user_id="",
        email="",
        phone="",
        user_name="",
        user_surname="",
        user_password="",
        balance=0,
        tg_id="",
    ) -> None:

        self.user_id = user_id
        self.email = email
        self.phone = phone
        self.user_name = user_name
        self.user_surname = user_surname
        self.user_password = user_password
        self.balance = balance
        self.tg_id = tg_id

    def user_add(self, session):
        user_add = UserTable(
            email=self.email,
            phone=self.phone,
            name=self.user_name,
            surname=self.user_surname,
            user_password=self.user_password,
            balance=self.balance,
            tg_id=self.tg_id,
        )
        session.add(user_add)
        session.commit()
        self.user_id = user_add.id

    def get_user_by_email(self, session, email):
        user = session.query(UserTable).filter(UserTable.email == email).first()
        if user:
            return user
        else:
            return None

    def user_del(self, session):
        user = session.query(UserTable).filter(UserTable.id == self.user_id).first()
        session.delete(user)
        session.commit()
        logger.info(f"Пользователь с id{self.user_id} удален из базы")

    def check_balance(self, session):
        user = session.query(UserTable).filter(UserTable.id == self.user_id).first()
        return user.balance
    
