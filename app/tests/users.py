import os
import sys
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from services.users import User

from models.schemas import UserRegister

from database.database import get_db

from auth.jwt_handler import create_access_token


env_path = os.path.join(sys.path[0], ".env")
load_dotenv(env_path)

user_router = APIRouter(tags=["Users"])


@user_router.post("/signup")
async def registration(user_data: UserRegister, session=Depends(get_db)):
    user_exists = User().get_user_by_email(session, user_data.email)

    if user_exists:
        return "Пользователь с таким email существует"
    else:
        user = User(
            email=user_data.email,
            phone=user_data.phone,
            user_name=user_data.name,
            user_surname=user_data.surname,
            user_password=user_data.user_password,
        )
        user.user_add(session)
        return "Пользователь зарегистрирован"


@user_router.post("/signin")
async def autorization(user: OAuth2PasswordRequestForm = Depends(), session=Depends(get_db)):
    user = User(email=user.username, user_password=user.password)
    if user.autorization(session) == "Пользователь не найден":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )
    elif user.autorization(session) == "Пароль не подходит. Доступ запрещен":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пароль не подходит. Доступ запрещен.",
        )
    else:
        access_token = create_access_token(user.email)
        return {"access_token": access_token, "token_type": "Bearer"}


@user_router.get("/balance/{id}")
async def check_balance(id: int, session=Depends(get_db)):
    user = User(user_id=id)
    return {"Твой баланс": user.check_balance(session)}


@user_router.delete("/delete/{id}")
async def delete_user(id: int, session=Depends(get_db)):
    user = User(user_id=id)
    user.user_del(session)
    return "Пользователь удален"
