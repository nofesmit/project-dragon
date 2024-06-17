import streamlit as st
import pandas as pd

def app():
    st.title('Data Analysis')

    if st.session_state['dataframe'] is not None:
        df = st.session_state['dataframe']
        st.write("Basic Statistics")
        st.write(df.describe())
        # Add more analysis features as needed
    else:
        st.write("No data uploaded yet. Please upload data on the Data Uploader page.")