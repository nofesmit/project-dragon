import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Project Dragon')

import streamlit as st
import importlib
import sys
from pathlib import Path

# Ensure the 'pages' directory is in the sys.path
pages_dir = Path(__file__).parent / 'pages'
sys.path.append(str(pages_dir))

# Create a session state to store the dataframe
if 'dataframe' not in st.session_state:
    st.session_state['dataframe'] = None

st.title('Multi-Page Streamlit App')

PAGES = {
    "Data Uploader": "data_uploader",
    "Data Viewer": "data_viewer",
    "Data Filter": "data_filter",
    "Data Analysis": "data_analysis"
}

# Sidebar for navigation
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

# Import and run the selected page
page = importlib.import_module(PAGES[selection])
page.app()