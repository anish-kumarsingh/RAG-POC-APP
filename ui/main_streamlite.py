import streamlit as st
import os
import requests
import pandas
import plotly.express as px


st.set_page_config(page_title="Welcome to AI Assistance.")
st.title('MSC Genie')
content_available=False
df:pandas.DataFrame = None
sql_query:str=None
fig = None

def askQuestion(query:str):
    global sql_query
    sql_query = requests.get(f'http://localhost:8000/generate-sql?query={query}')
    fetchResult(sql_query=sql_query)

def fetchResult(sql_query:str):
    data = requests.get(f'http://localhost:8000/fetch-results?query={sql_query}')
    df=pandas.read_json(data['data'])
    global fig
    fig = px.bar(
        df,
        x=data['chart-configs']['layout']['xaxis']['title'],
        y=data['chart-configs']['layout']['yaxis']['title'],
        title=data['chart-configs']['layout']['title']
    )
    global content_available
    content_available = True

with st.container:
    if content_available : 
        st.text_area("SQL", sql_query, height=150)
        st.dataframe(df)
        st.plotly_chart(fig)
        st.text_input(placeholder="MSC Genie at your Service! Ask your query.")
    st.button('Ask',on_click=askQuestion())


