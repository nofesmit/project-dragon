import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Project Dragon')

import streamlit as st
import os
import importlib

# Create a session state to store the dataframe
if 'dataframe' not in st.session_state:
    st.session_state['dataframe'] = None

st.title('Multi-Page Streamlit App')

PAGES = {
    "Data Uploader": "pages.data_uploader",
    "Data Viewer": "pages.data_viewer",
    "Data Filter": "pages.data_filter",
    "Data Analysis": "pages.data_analysis"
}

# Sidebar for navigation
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

# Import and run the selected page
page = importlib.import_module(PAGES[selection])
page.app()