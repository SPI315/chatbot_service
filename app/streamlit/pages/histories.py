import streamlit as st
import pandas as pd
from menu import menu_with_redirect
import requests
from params import FASTAPI_URL

menu_with_redirect()

st.title(
    f"Посмотри, что мы на тебя собрали, {st.session_state.user_name} :sleuth_or_spy:"
)

if st.button("Посмотреть историю транзакций"):
    response = requests.get(
        f"{FASTAPI_URL}/transaction/history/{st.session_state.user_id}",
        timeout=600,
    )
    if response.status_code == 200 or response.status_code == 404:
        history = pd.DataFrame(response.json())
        history = history.reindex(
            columns=["id", "user_id", "date", "replenishment", "write_off"]
        )
        history = history.rename(
            columns={
                "id": "ID транзакции",
                "user_id": "ID пользователя",
                "date": "Дата",
                "replenishment": "Пополнение",
                "write_off": "Списание",
            }
        )
        st.table(history)
    else:
        st.markdown("Извини, не могу говорить. Все, пока!")

if st.button("Посмотреть историю запросов"):
    response = requests.get(
        f"{FASTAPI_URL}/data/load_data_hist/{st.session_state.user_id}",
        timeout=600,
    )
    if response.status_code == 200 or response.status_code == 404:
        history = pd.DataFrame(response.json())
        history = history.reindex(
            columns=["id", "user_id", "request_date", "input_data", "output_data"]
        )
        history = history.rename(
            columns={
                "id": "ID запроса",
                "user_id": "ID пользователя",
                "request_date": "Дата",
                "input_data": "Исходные данные",
                "output_data": "Ответ сервиса",
            }
        )
        st.table(history)
    else:
        st.markdown("Извини, не могу говорить. Все, пока!")
