import streamlit as st
import pandas as pd

# ---- CONFIG ----
st.set_page_config(page_title="Bevételek", layout="wide")

# ---- FUNCTIONS ----

def inc_clean(df_income):
    df_income = df_income.replace('_x000D_', '', regex=True)
    df_income = df_income.replace('\n', '', regex=True)
    df_income = df_income[['Kiállítás','partner','Bizonylat II.','Megjegyzés','Szállítási mód','Cikk','ar','penznem', 'mennyiseg','teljes_ar','HUF_ar','EUR_HUF']]
    df_income['Kiállítás'] = pd.to_datetime(df_income['Kiállítás'])
    return df_income

if 'df_income' not in st.session_state:
    st.title('Az adatok vizsgálatához először töltsön fel vizsgálandó adatot.')
    st.write('Bevételek vizsgálatához a bevételi adatok feltöltése szükséges!')
else:
    df_income = st.session_state['df_income']
    
    df_income = inc_clean(df_income)

    st.title('Bevételek')
    
    st.dataframe(df_income)
    st.write(df_income.dtypes)
    st.write(df_income['HUF_ar'].sum())