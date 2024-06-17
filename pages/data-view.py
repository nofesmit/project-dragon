import streamlit as st

def app():
    st.title('Data Viewer')

    if st.session_state['dataframe'] is not None:
        st.write(st.session_state['dataframe'])
    else:
        st.write("No data uploaded yet. Please upload data on the Data Uploader page.")