import streamlit as st
import requests
import pandas
import plotly.graph_objects as go

import sys
print(sys.executable)

st.set_page_config(layout="wide")
st.set_page_config(page_title="Welcome to AI Assistance.")
st.markdown("<h1 style='text-align: center;'><u>MSC Genie</u></h1>", unsafe_allow_html=True)

content_available=False
df:pandas.DataFrame = None
sql_query:str=None
fig = None

col1, col2 = st.columns(2)


sql_area, =st.columns([1])


def askQuestion(query:str):
    if query is not None and len(query.strip()) > 15 :
        global sql_query
        response = requests.get(f'http://localhost:8000/generate-sql?query={query}')
        response.raise_for_status()
        with sql_area:
            st.subheader("Generated Query")
            st.text_area("", response.json()['sql_query'], height=100)
        df=fetchResult(sql_query=response.json()['sql_query'])
        updateChart(df=df)

def fetchResult(sql_query:str):
    response = requests.get(f'http://localhost:8000/fetch-results?query={sql_query}')
    response.raise_for_status()
    data=response.json()
    df=pandas.read_json(data['data'])
    with col1:
        col1.subheader('Records:')
        col1.dataframe(df, height=500, use_container_width=True)
    return df

def updateChart(df):
    with col2:
        st.subheader("Chart")
        columns = df.columns.tolist()
        x_column = st.selectbox("Select the X-axis column", columns, index=0)
        
        # Allow multiple columns to be selected for the Y-axis
        y_columns = st.multiselect("Select the Y-axis columns", columns, default=[columns[1]])

        # Create a Plotly Figure object
        fig = go.Figure()

        # Add a Bar trace for each dynamically selected Y-axis column
        for y_column in y_columns:
            fig.add_trace(go.Bar(
                x=df[x_column],
                y=df[y_column],
                name=y_column
            ))

        # Update the layout with titles that reflect the selected columns
        fig.update_layout(
            title=f"Chart of {', '.join(y_columns)} by {x_column}",
            xaxis_title=x_column,
            yaxis_title="Value"
        )
        # Render the Plotly chart using st.plotly_chart
        col2.plotly_chart(fig, use_container_width=True)
        pass

col_input, col_button = st.columns([0.9, 0.1])
input_query: str=None
with col_input:
    input_query=st.text_input(label="Query",placeholder="MSC Genie at your Service! Ask your query.", label_visibility="hidden")
with col_button:
    st.button(label='Ask', type="primary",on_click=askQuestion(input_query))
