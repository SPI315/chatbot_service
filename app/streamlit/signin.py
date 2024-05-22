import streamlit as st
from menu import menu, set_role
import requests
from loguru import logger
from params import FASTAPI_URL

menu()

if "role" not in st.session_state:
    st.session_state.role = False

st.session_state._role = st.session_state.role

if st.session_state.role == False:
    with st.form("signin", border=False):
        st.title("Привет! Добро пожаловать!")
        st.title("Здесь ты можешь пообщаться с мощнейшим искусственным интеллектом за деньги")
        st.title("Авторизуйся, чтобы продолжить:")

        email = st.text_input("Почта")
        password = st.text_input("Пароль", type="password")

        if st.form_submit_button("Отправить"):
            data = {"username": email, "password": password}
            response = requests.post(f"{FASTAPI_URL}/user/signin/", data=data)
            if response.status_code == 200:
                st.session_state._role = True
                st.session_state.user_token = response.json()["access_token"]
                set_role()
                

                user = requests.get(
                    f"{FASTAPI_URL}/user/get_by_email",
                    headers={"Authorization": f"Bearer {st.session_state.user_token}"},
                    params={"email": email},
                    timeout=600,
                )
                
                logger.info(user)
                logger.info(response)

                st.session_state.user_id = user.json()["id"]
                st.session_state.user_name = user.json()["name"]
                st.write(response.json())
                st.rerun()

            elif response.status_code in [401, 404]:
                st.write(response.json())
            else:
                st.error("some error")


elif st.session_state.role == True:
    st.title("Авторизовано!")
    st.title(f"Добро пожаловать, {st.session_state.user_name}!")

else:
    st.title("Сервис недоступен")
