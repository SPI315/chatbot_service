from fastapi import APIRouter, Depends, HTTPException, status

from services.data import OperData
from services.ml import OperModel
from services.transaction import Transaction
from services.users import User
from database.database import get_db

data_router = APIRouter(tags=["Data"])


@data_router.get("/load_data_hist/{id}")
async def load_data_hist(id: int, session = Depends(get_db)):
    data_hist = OperData().load_data(session=session, user_id=id)
    if data_hist:
        return data_hist
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Нет истории - нет проблем."
        )


@data_router.delete("/del_data_hist/{id}")
async def del_data_hist(id: int, session = Depends(get_db)):
    data = OperData()
    try:
        data.delete_data_history(session=session, user_id=id)
        return f"История запросов пользователя ID{id} очищена"
    except Exception as exc:
        return f"История запросов не очищена по причине: {exc}"