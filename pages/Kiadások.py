import streamlit as st
import pandas as pd

# ---- CONFIG ----
st.set_page_config(page_title="Kiadások", layout="wide")

# ---- FUNCTIONS ----

def exp_clean(df_expense):
    df_expense = df_expense[['kelt','partner', 'bizonylat_szam', 'megjegyzes', 'netto', 'cat_code', 'main_cat', 'source']]
    df_expense['kelt'] = pd.to_datetime(df_expense['kelt'])
    return df_expense

def join(df_expense, df_category):
    df_exp_cat = pd.merge(df_expense,df_category,on='cat_code',how='left')
    df_exp_cat = df_exp_cat.rename(columns={'Kategória': 'category', 'Alkategória': 'subcategory', 'Elem': 'item'}).drop(columns=['Régi kód', 'Leírás'],axis=1)
    return df_exp_cat

if 'df_expense' not in st.session_state or 'df_category' not in st.session_state:
    st.title('Az adatok vizsgálatához először töltsön fel vizsgálandó adatot.')
    st.write('Kiadások vizsgálatához a kiadási adatok és a kiadási kategóriák feltöltése szükséges!')
else:
    df_expense = st.session_state['df_expense']
    df_category = st.session_state['df_category']

    df_expense = exp_clean(df_expense)
    df_exp_cat = join(df_expense, df_category)


    st.title('Kiadások')

    st.dataframe(df_exp_cat)
    st.write(df_exp_cat.dtypes)
    st.write(df_exp_cat['netto'].sum())