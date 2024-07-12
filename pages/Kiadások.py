import streamlit as st
import pandas as pd

# ---- CONFIG ----
st.set_page_config(page_title="Kiadások", layout="wide")

# ---- FUNCTIONS ----

def exp_clean(df_expense):
    try:
        # Ensure the DataFrame contains the required columns
        required_columns = ['kelt', 'partner', 'bizonylat_szam', 'megjegyzes', 'netto', 'cat_code', 'main_cat', 'source']
        missing_columns = [col for col in required_columns if col not in df_expense.columns]
        if missing_columns:
            raise ValueError(f"The DataFrame is missing the following columns: {missing_columns}")
        
        df_expense = df_expense[required_columns]
        df_expense['kelt'] = pd.to_datetime(df_expense['kelt'])
        df_expense['year'] = pd.DatetimeIndex(df_expense['kelt']).year
        
        return df_expense
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

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

# ---- PAGE ----

    st.dataframe(df_exp_cat)
    st.write(df_exp_cat.dtypes)

# ---- FILTERING -----
    all_value = 'Mind'

    st.sidebar.header('Évek', divider='grey')

    year = sorted(df_exp_cat['year'].unique())
    year.append(all_value)
    years = st.sidebar.multiselect('Válassz évet:', options=year, default='Mind')
    if "All" in years or len(years) == 0:
        years = sorted(df_exp_cat['year'].unique())

    st.sidebar.write("")
    st.sidebar.write("")

    st.sidebar.header('Kategória', divider='grey')

    cat_code = sorted(df_exp_cat['cat_code'].unique())
    cat_code.append(all_value)
    cat_codes = st.sidebar.multiselect('Válassz kategóriát:', options=cat_code, default='Mind')
    if "All" in cat_codes or len(cat_codes) == 0:
        regions = sorted(df_exp_cat['cat_code'].unique())
        


    selected_df = df_exp_cat[
        (df_exp_cat['year'].isin(years)) &
        (df_exp_cat['cat_code'].isin(cat_codes))]



    st.title('Kiadások')

    st.dataframe(selected_df)
