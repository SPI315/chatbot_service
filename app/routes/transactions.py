from fastapi import APIRouter, HTTPException, status, Depends

from services.transaction import Transaction
from database.database import get_db

transactions_router = APIRouter(tags=["Transactions"])


@transactions_router.post("/replanishment/{id}")
async def replanishment(id: int, summ: int, session=Depends(get_db)):
    try:
        transaction = Transaction()
        transaction.replanishment(session, user_id=id, value=summ)
        return "Баланс пополнен"
    except Exception as exc:
        return f"В настоящий момент пополнение не доступно: {exc}"


@transactions_router.get("/history/{id}")
async def load_history(id: int, session=Depends(get_db)):
    transaction = Transaction()
    hist = transaction.load_history(session, id)
    if hist:
        return hist
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Нет истории - нет проблем."
        )


@transactions_router.delete("/del_hist/{id}")
async def del_history(id: int, session=Depends(get_db)):
    transaction = Transaction()
    try:
        transaction.del_history(session, user_id=id)
        return "История транзакций очищена"
    except Exception as exc:
        return f"История транзакций не очищена по причине: {exc}"
