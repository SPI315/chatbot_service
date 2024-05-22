from models.users import UserTable
from models.transactions import TransactionsTable
from database.database import SessionLocal
import datetime
from loguru import logger


# класс для работы с транзакциями
class Transaction:
    def __init__(self) -> None:
        pass

    # метод для сохранения транзакций
    def save_transaction(self, session, user_id, replenishment=0, write_off=0):
        transaction = TransactionsTable(
            user_id=user_id,
            date=datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S"),
            replenishment=replenishment,
            write_off=write_off,
        )
        session.add(transaction)
        session.commit()

    # метод для вывода истории транзакций пользователя
    def load_history(self, session, user_id):
        result = (
            session.query(TransactionsTable)
            .filter(TransactionsTable.user_id == user_id)
            .all()
        )
        if not result:
            return None

        return result

    def transform_history(self, history):
        transform_history = {}
        for obj in history:
            transform_history[f"Транзакция ID{obj.id}"] = {}
            transform_history[f"Транзакция ID{obj.id}"]["Дата"] = obj.date
            if obj.replenishment == 0:
                transform_history[f"Транзакция ID{obj.id}"]["Списание"] = obj.write_off
            else:
                transform_history[f"Транзакция ID{obj.id}"][
                    "Пополнение"
                ] = obj.replenishment

        return transform_history

    # метод для удаления истории транзакций пользователя
    def del_history(self, session, user_id):
        result = (
            session.query(TransactionsTable)
            .filter(TransactionsTable.user_id == user_id)
            .all()
        )
        for obj in result:
            session.delete(obj)
        session.commit()
        logger.info(f"История транзакций пользователя с id{user_id} удалена из базы")

    # метод для пополнения баланса
    def replanishment(self, session, user_id, value):
        user_data = session.get(UserTable, user_id)
        logger.info(f"Текущий баланс: {user_data.balance}")

        user_data.balance = user_data.balance + value
        logger.info(
            f"Поподнение баланса на {value}. Текущий баланс: {user_data.balance}"
        )

        session.commit()
        self.save_transaction(session, user_id=user_id, replenishment=value)

    # метод для списания с баланса
    def write_off(self, session, user_id, value):
        user_data = session.get(UserTable, user_id)
        logger.info(f"Текущий баланс: {user_data.balance}")

        user_data.balance = user_data.balance - value
        logger.info(
            f"Списание с баланса на {value}. Текущий баланс: {user_data.balance}"
        )

        session.commit()
        self.save_transaction(session, user_id=user_id, write_off=value)
