import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Project Dragon')

if 'df' in st.session_state:
    df = st.session_state.df


st.dataframe(df)