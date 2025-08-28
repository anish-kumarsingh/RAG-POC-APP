import streamlit as st
from db import local_db
from props import app_props
import app
from utility import app_constants
import os
from dotenv import load_dotenv

env_path = 'variables.env'

# Load the variables from the specified file
load_dotenv(dotenv_path=env_path)


app_properties = app_props.PropLoader('app.properties')

#Add your tocket in environment or here so it will be available to connect with Hugging face.
# os.environ.setdefault(app_properties.getProp(app_constants.HUGGINGFACE_TOEKN_KEY), app_properties.getProp(app_constants.HUGGINGFACE_TOEKN_KEY))
print(f"Hugging face value in env : {os.getenv("HF_TOKEN")}")
data_access=local_db.SqlDataPool(app_properties)
enable_tabs=False
enable_error=False
if "text_value" not in st.session_state:
    st.session_state.text_value = ""

if "error_text_value" not in st.session_state:
    st.session_state.error_text_value = ""
if enable_error:
    st.write(st.session_state.error_text_value)
tab1 = None
tab2 = None
if enable_tabs:
    tab1 , tab2 = st.tabs(["Data Frame", "Charts"])
    tab1.dataframe(None, height=250, use_container_width=True)
    tab1.bar_chart(None, height=250, use_container_width=True)
user_query=st.text_input(label="Assitant",placeholder="Ask me something.", value=st.session_state.text_value)
if st.button("Submit"):
    print(f"User input: {user_query}")
    st.session_state.text_value=""
    st.session_state.error_text_value=""
    enable_error=False
    sql_query = app.processAgentRequst(user_query)
    print(f"Returned query: {sql_query}")
    if sql_query is not None and sql_query.startswith("select"):
        dataFrame = data_access.executeQuery(sql_query)
        enable_tabs=True
        tab1.dataframe(dataFrame, height=250, use_container_width=True)
        tab1.bar_chart(dataFrame, height=250, use_container_width=True)
    else :
        st.session_state.error_text_value=sql_query
        enable_error=True
    # user_query=st.text_input(label="Assitant",placeholder="Ask me something.")



