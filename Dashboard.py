import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import toml

if 'df' not in st.session_state:
    st.write('First save a dataframe')

if 'df' in st.session_state:
    df = st.session_state.df
    
    st.write(df)

st.file_uploader('', key=1)
st.file_uploader('', key=2)