import streamlit as st

from props import app_props
import app
from utility import app_constants
import os
from dotenv import load_dotenv

st.set_page_config(page_title="Welcome to AI Assistance.")

enable_error=False
if "text_value" not in st.session_state:
    st.session_state.text_value = ""

if "error_text_value" not in st.session_state:
    st.session_state.error_text_value = ""
if enable_error:
    st.write(st.session_state.error_text_value)

tab1 , tab2 = st.tabs(["Data Frame", "Charts"])
user_query=st.text_input(label="Assitant",placeholder="Ask me something.", value=st.session_state.text_value)
if st.button("Submit"):
    print(f"User input: {user_query}")
    st.session_state.text_value=""
    st.session_state.error_text_value=""
    enable_error=False
    sql_query:str = app.processAgentRequst(user_query)
    print(f"Returned query: {sql_query}")
    if sql_query is not None and sql_query.strip().lower().startswith("select"):
        dataFrame = data_access.executeQuery(sql_query)
        print(f"Got response from db:{dataFrame}")
        enable_tabs=True
        tab1.dataframe(dataFrame, height=250, use_container_width=True)
        tab1.bar_chart(dataFrame, y=['created_time'], x='due_date', height=250, use_container_width=True)
    else :
        st.session_state.error_text_value=sql_query
        enable_error=True




