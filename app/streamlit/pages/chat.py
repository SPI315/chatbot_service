import streamlit as st
from menu import menu_with_redirect
import requests
from params import FASTAPI_URL

menu_with_redirect()

st.title("Здесь надо что-то написать :arrow_heading_down:")

prompt = st.chat_input(placeholder="Напиши что нибудь, а я продолжу!", max_chars=50)
if prompt:
    st.markdown(f"Ты написал: {prompt}")
    with st.spinner("Подожди, подожди..."):
        response = requests.get(
            f"{FASTAPI_URL}/model/pred/{st.session_state.user_id}",
            headers={"Authorization": f"Bearer {st.session_state.user_token}"},
            params={"data": prompt},
            timeout=600,
        )

        new_response = response.text

        if response.status_code == 200:
            st.markdown(f"А я говорю:{new_response}", unsafe_allow_html=True)
            check_balance = requests.get(
                f"{FASTAPI_URL}/user/balance/{st.session_state.user_id}",
                headers={"Authorization": f"Bearer {st.session_state.user_token}"},
                timeout=600,
            )
            balance = check_balance.text
            sidebar = st.sidebar.markdown(
                f"""
                        # У тебя осталось:
                        # :red[{balance} :money_with_wings:]"""
            )

        else:
            st.markdown("Извини, не могу говорить. Все, пока!")
