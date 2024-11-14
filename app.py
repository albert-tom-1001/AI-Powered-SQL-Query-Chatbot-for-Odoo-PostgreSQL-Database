import vanna as vn
import streamlit as st
import pandas as pd
import psycopg2
from vanna.remote import VannaDefault

# Vanna AI 
vanna_api_key = st.secrets["vanna"]["api_key"]
vanna_model_name = 'chinook'
vn = VannaDefault(model=vanna_model_name, api_key=vanna_api_key)

st.title("Welcome to your :blue[SQL Chatbot]")

def conn_params():
    server_host = "182.66.248.250"
    server_port = "5432"
    database_name = "odoo17"
    DB_username = "odoo17"
    password = "KENf9wcR28fh2"
    return server_host, password, DB_username, database_name, server_port

# Initialize session states if they don't exist
if "query" not in st.session_state:
    st.session_state.query = ""
if "clear_query" not in st.session_state:
    st.session_state.clear_query = False

def query_database():
    if st.session_state.clear_query:
        # Clear query state and reset the flag
        st.session_state.query = ""
        st.session_state.clear_query = False
    
    # Input for user query
    query_input = st.text_input("What would you like to know from the database?", value=st.session_state.query, key="query")

    # Check if there's a query and execute only if it's provided
    if query_input:
        st.subheader(query_input)
        sql = vn.generate_sql(query_input)
        st.code(sql, language='sql')
        
        # Run the query and display the results
        df = vn.run_sql(sql)
        st.dataframe(df, use_container_width=True)
        
        # Generate and display a chart
        fig = vn.get_plotly_figure(plotly_code=vn.generate_plotly_code(question=query_input, sql=sql, df=df), df=df)
        st.plotly_chart(fig, use_container_width=True)

        # "Ask Again" button to clear the input
        if st.button("Ask Again"):
            st.session_state.clear_query = True  # Set flag to clear input on the next run

# Connect to PostgreSQL database and query
server_host, password, DB_username, database_name, server_port = conn_params()
vn.connect_to_postgres(host=server_host, dbname=database_name, password=password, user=DB_username, port=server_port)
query_database()
