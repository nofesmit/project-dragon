import streamlit as st
import pandas as pd

def app():
    st.title('Data Uploader')

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.session_state['dataframe'] = df
        st.write("Data uploaded successfully!")

    if st.session_state['dataframe'] is not None:
        st.write("Current DataFrame:")
        st.write(st.session_state['dataframe'])