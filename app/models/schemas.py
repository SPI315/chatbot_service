from pydantic import BaseModel


class UserRegister(BaseModel):
    email: str
    phone: str
    name: str
    surname: str
    user_password: str
    balance: int
    tg_id: str
