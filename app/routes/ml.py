from fastapi import APIRouter, Depends

from services.data import OperData
from services.transaction import Transaction
from services.users import User
from database.database import get_db
import json
from rmworker.send_message import RpcClient
from auth.authenticate import authenticate

ml_router = APIRouter(tags=["ML"])


@ml_router.get("/pred/{id}")
async def pred(id: int, data: str, session=Depends(get_db), user:str=Depends(authenticate)):
    oper_data = OperData(data=data, user_id=id)
    user = User(id)
    transaction = Transaction()

    if user.check_balance(session) < 100:
        return "Кинь сотку на баланс."

    oper_data.save_input_data(session)

    to_send = json.dumps({id: data})

    response = RpcClient().send_message(message=to_send)
    result = json.loads(response)
    oper_data.save_output_data(session, result)
    transaction.write_off(session, user_id=id, value=100)

    return result
