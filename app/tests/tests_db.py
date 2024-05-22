from services.users import User
from conftest import Session


from services.users import User
from services.transaction import Transaction

test_transaction = Transaction()
test_user = User(
    email="test_2@mail.ru",
    phone="+7777777777",
    user_name="test_2",
    user_surname="test_2",
    user_password="123",
    balance=0,
    tg_id="-",
)


def test_create_user(session: Session):
    try:
        test_user.user_add(session)
        assert True
    except Exception as e:
        assert False, e


def test_create_transaction(session: Session):
    try:
        test_transaction.replanishment(session, user_id=test_user.user_id, value=100)
        assert True
    except Exception as e:
        assert False, e


def test_delete_history(session: Session):
    try:
        test_transaction.del_history(session, user_id=test_user.user_id)
        assert True
    except Exception as e:
        assert False, e


def test_delete_user(session: Session):
    try:
        test_user.user_del(session)
        assert True
    except Exception as e:
        assert False, e
