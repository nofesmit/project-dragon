import streamlit as st
import pandas as pd

# ---- CONFIG ----
st.set_page_config(page_title="Kiadások", layout="wide")

# --- PAGE ---

if 'df_expense' not in st.session_state:
    st.title('Az adatok vizsgálatához először töltsön fel vizsgálandó adatot.')
    st.write('Bevételek vizsgálatához a bevételi adatok feltöltése szükséges!')

df_expense = st.session_state['df_expense']

st.header('Kiadasok', divider='grey')
    