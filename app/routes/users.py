import os
import sys
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from services.users import User

from models.schemas import UserRegister

from database.database import get_db

from auth.jwt_handler import create_access_token
from auth.hash_password import HashPassword
from auth.authenticate import authenticate

env_path = os.path.join(sys.path[0], ".env")
load_dotenv(env_path)

user_router = APIRouter(tags=["Users"])


@user_router.post("/signup")
async def registration(user_data: UserRegister, session=Depends(get_db)):
    user_exists = User().get_user_by_email(session, user_data.email)

    hashed_password = HashPassword().create_hash(user_data.user_password)
    
    if user_exists:
        return "Пользователь с таким email существует"
    else:
        user = User(
            email=user_data.email,
            phone=user_data.phone,
            user_name=user_data.name,
            user_surname=user_data.surname,
            user_password=hashed_password,
        )
        user.user_add(session)
        return "Пользователь зарегистрирован"


@user_router.post("/signin")
async def autorization(
    user: OAuth2PasswordRequestForm = Depends(), session=Depends(get_db)
):
    
    user_exists = User().get_user_by_email(session, user.username)
    if user_exists is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )
    elif HashPassword().verify_hash(user.password, user_exists.user_password):
        access_token = create_access_token(user.username)
        return {"access_token": access_token, "token_type": "Bearer"}
        
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пароль не подходит. Доступ запрещен.",
        )


@user_router.get("/balance/{id}")
async def check_balance(id: int, session=Depends(get_db), user:str=Depends(authenticate)):
    user = User(user_id=id)
    return user.check_balance(session)


@user_router.delete("/delete/{id}")
async def delete_user(id: int, session=Depends(get_db)):
    user = User(user_id=id)
    user.user_del(session)
    return "Пользователь удален"


@user_router.get("/get_by_email")
async def get_by_email(email: str, session=Depends(get_db), user:str=Depends(authenticate)):
    user_exists = User().get_user_by_email(session=session, email=email)
    if user_exists is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь с таким email не не зарегистрирован",
        )
    return user_exists
