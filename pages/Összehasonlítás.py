import streamlit as st
import pandas as pd



if 'df_expense' not in st.session_state or 'df_category' not in st.session_state or 'df_income' not in st.session_state:
    st.title('Az adatok vizsgálatához először töltsön fel vizsgálandó adatot.')
    st.write('Kiadások vizsgálatához a kiadási adatok és a kiadási kategóriák feltöltése szükséges!')
else:
    df_expense = st.session_state['df_expense']
    df_category = st.session_state['df_category']
    df_income = st.session_state['df_income']
    
if 'df_income' not in st.session_state:
    st.title('Az adatok vizsgálatához először töltsön fel vizsgálandó adatot.')
    st.write('Bevételek vizsgálatához a bevételi adatok feltöltése szükséges!')
else:
    


    st.title('Összehasonlítás')