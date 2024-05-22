from models.data import DataTable
import datetime


# класс для данных
class OperData:
    def __init__(self, data: str = "", user_id: int = 0) -> None:
        self.data = data
        self.user_id = user_id

    # метод для загрузки истории запросов пользователя
    def load_data(self, session, user_id):
        data = session.query(DataTable).filter(DataTable.user_id == user_id).all()
        if not data:
            return None

        return data

    # метод для удаления истории запросов пользователя
    def delete_data_history(self, session, user_id):
        data = session.query(DataTable).filter(DataTable.user_id == user_id).all()
        for obj in data:
            session.delete(obj)
        session.commit()

    # метод для преобразования данных из БД в словарь
    def transform_data(self, data):
        transform_data = {}
        for obj in data:
            transform_data[f"Данные ID{obj.id}"] = {}
            transform_data[f"Данные ID{obj.id}"]["Дата запроса"] = obj.request_date
            transform_data[f"Данные ID{obj.id}"]["Входящие данные"] = obj.input_data
            transform_data[f"Данные ID{obj.id}"]["Исходящие данные"] = obj.output_data
        return transform_data

    # метод для сохранения входящих данных
    def save_input_data(self, session):
        data_add = DataTable(
            user_id=self.user_id,
            request_date=datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S"),
            input_data=self.data,
            output_data=None,
        )
        session.add(data_add)
        session.commit()

    # метод для сохранения исходящих данных
    def save_output_data(self, session, output_data):
        data = (
            session.query(DataTable)
            .filter(
                DataTable.user_id == self.user_id, DataTable.input_data == self.data
            )
            .first()
        )
        data.output_data = output_data
        session.commit()

    def check_output(self, session):

        if self.load_output_data(session) == None:
            return "no prediction("
        else:
            return "have prediction!"

    def load_output_data(self, session):
        output_data = (
            session.query(DataTable.output_data)
            .filter(
                DataTable.user_id == self.user_id, DataTable.input_data == self.data
            )
            .first()
        )
        return output_data[0]
