from fastapi.testclient import TestClient
from services.users import User
from tests.conftest import Session

from fastapi.security import OAuth2PasswordRequestForm

user_for_tests = {
    "email": "test_3@mail.ru",
    "phone": "+7777777",
    "name": "test_3",
    "surname": "test_3",
    "user_password": "123",
    "balance": 0,
    "tg_id": "-",
}


def test_signup(client: TestClient):
    response = client.post("/user/signup", json=user_for_tests)
    assert response.status_code == 200
    assert response.json() == "Пользователь зарегистрирован"


def test_signup_same_email(client: TestClient):
    response = client.post("/user/signup", json=user_for_tests)
    assert response.status_code == 200
    assert response.json() == "Пользователь с таким email существует"


def test_signin(client: TestClient):
    response = client.post("/user/signin")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_empty_transaction_history(client: TestClient, session: Session):
    test_user = User().get_user_by_email(session, user_for_tests["email"])
    response = client.get(f"/transaction/history/{test_user.id}")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Нет истории - нет проблем.'}

def test_empty_data_history(client: TestClient, session: Session):
    test_user = User().get_user_by_email(session, user_for_tests["email"])
    response = client.get(f"/data/load_data_hist/{test_user.id}")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Нет истории - нет проблем.'}

def test_check_balance(client: TestClient, session: Session):
    test_user = User().get_user_by_email(session, user_for_tests["email"])
    response = client.get(f"/user/balance/{test_user.id}")
    assert response.status_code == 200
    assert response.json() == {"Твой баланс": 0}


def test_pred_without_cred(client: TestClient, session: Session):
    test_user = User().get_user_by_email(session, user_for_tests["email"])
    response = client.get(f"/model/pred/{test_user.id}?data=Это тестовый вопрос")
    assert response.status_code == 200
    assert response.json() == "Кинь сотку на баланс."


def test_replanishment(client: TestClient, session: Session):
    test_user = User().get_user_by_email(session, user_for_tests["email"])
    response = client.post(f"/transaction/replanishment/{test_user.id}?summ=500")
    assert response.status_code == 200
    assert response.json() == "Баланс пополнен"


def test_pred(client: TestClient, session: Session):
    test_user = User().get_user_by_email(session, user_for_tests["email"])
    response = client.get(f"/model/pred/{test_user.id}?data=Это тестовый вопрос")
    assert response.status_code == 200
    assert isinstance(response.json(), str)


def test_load_transaction_history(client: TestClient, session: Session):
    test_user = User().get_user_by_email(session, user_for_tests["email"])
    response = client.get(f"/transaction/history/{test_user.id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_delete_transaction_history(client: TestClient, session: Session):
    test_user = User().get_user_by_email(session, user_for_tests["email"])
    response = client.delete(f"/transaction/del_hist/{test_user.id}")
    assert response.status_code == 200
    assert response.json() == "История транзакций очищена"


def test_load_data_history(client: TestClient, session: Session):
    test_user = User().get_user_by_email(session, user_for_tests["email"])
    response = client.get(f"/data/load_data_hist/{test_user.id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_delete_data_history(client: TestClient, session: Session):
    test_user = User().get_user_by_email(session, user_for_tests["email"])
    response = client.delete(f"/data/del_data_hist/{test_user.id}")
    assert response.status_code == 200
    assert response.json() == f"История запросов пользователя ID{test_user.id} очищена"


def test_delete_user(client: TestClient, session: Session):
    test_user = User().get_user_by_email(session, user_for_tests["email"])
    response = client.delete(f"/user/delete/{test_user.id}")
    assert response.status_code == 200
    assert response.json() == "Пользователь удален"
