import streamlit as st
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="Adatfeltöltés", layout="wide", page_icon='dragon')

hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

# --- SESSION VARIABLES ---

if 'df_inc_data' not in st.session_state:
    df_inc_data = pd.DataFrame
else:
    df_inc_data = st.session_state['df_inc_data']

if 'df_inc_cat' not in st.session_state:
    df_inc_cat = pd.DataFrame
else:
    df_inc_cat = st.session_state['df_inc_cat']

if 'df_income' not in st.session_state:
    df_income = pd.DataFrame
else:
    df_income = st.session_state['df_income']

if 'df_exp_data' not in st.session_state:
    df_exp_data = pd.DataFrame
else:
    df_exp_data = st.session_state['df_exp_data']

if 'df_exp_cat' not in st.session_state:
    df_exp_cat = pd.DataFrame
else:
    df_exp_cat = st.session_state['df_exp_cat']

if 'df_expense' not in st.session_state:
    df_expense = pd.DataFrame
else:
    df_expense = st.session_state['df_expense']

if 'df_employees' not in st.session_state:
    df_employees = pd.DataFrame
else:
    df_employees = st.session_state['df_employees']

# --- DATAFRAME CLEANING ---

def income_clean(df_inc_data, df_inc_cat):
    df_income = pd.merge(df_inc_data, df_inc_cat, on='kat_kod', how='left')
    df_income['year'] = pd.DatetimeIndex(df_income['datum']).year
    df_income['month'] = pd.DatetimeIndex(df_income['datum']).month
    df_income['quarter'] = pd.DatetimeIndex(df_income['datum']).quarter
    df_income['month_year'] = df_income['datum'].dt.to_period('m')
    
    df_income['kat_kod'] = df_income['kat_kod'].apply(lambda x: str(x) if pd.notnull(x) else None)
    df_income['kat_kod'] = df_income['kat_kod'].fillna('hiányos')
    df_income['kategoria'] = df_income['kategoria'].apply(lambda x: str(x) if pd.notnull(x) else None)
    df_income['kategoria'] = df_income['kategoria'].fillna('hiányos')
    df_income['alkategoria'] = df_income['alkategoria'].apply(lambda x: str(x) if pd.notnull(x) else None)
    df_income['alkategoria'] = df_income['alkategoria'].fillna('hiányos')
    df_income['elem'] = df_income['elem'].apply(lambda x: str(x) if pd.notnull(x) else None)
    df_income['elem'] = df_income['elem'].fillna('hiányos')
    
    df_income = df_income.rename(columns={'teljes_forintban': 'netto'})
    
    return df_income

def expense_clean(df_exp_data, df_exp_cat):
    df_expense = pd.merge(df_exp_data, df_exp_cat, on='kat_kod', how='left')
    df_expense['year'] = pd.DatetimeIndex(df_expense['datum']).year
    df_expense['month'] = pd.DatetimeIndex(df_expense['datum']).month
    df_expense['quarter'] = pd.DatetimeIndex(df_expense['datum']).quarter
    df_expense['month_year'] = df_expense['datum'].dt.to_period('m')
    
    df_expense['bizonylat_szam'] = df_expense['bizonylat_szam'].apply(lambda x: str(x) if pd.notnull(x) else None)
    df_expense['bizonylat_szam'] = df_expense['bizonylat_szam'].fillna('')
    df_expense['megjegyzes'] = df_expense['megjegyzes'].apply(lambda x: str(x) if pd.notnull(x) else None)
    df_expense['megjegyzes'] = df_expense['megjegyzes'].fillna('')
    
    df_expense['kat_kod'] = df_expense['kat_kod'].apply(lambda x: str(x) if pd.notnull(x) else None)
    df_expense['kat_kod'] = df_expense['kat_kod'].fillna('hiányos')
    df_expense['fo_kat'] = pd.to_numeric(df_expense['fo_kat'], errors='coerce').fillna(0).astype(int)
    df_expense['kategoria'] = df_expense['kategoria'].apply(lambda x: str(x) if pd.notnull(x) else None)
    df_expense['kategoria'] = df_expense['kategoria'].fillna('hiányos')
    df_expense['alkategoria'] = df_expense['alkategoria'].apply(lambda x: str(x) if pd.notnull(x) else None)
    df_expense['alkategoria'] = df_expense['alkategoria'].fillna('hiányos')
    df_expense['elem'] = df_expense['elem'].apply(lambda x: str(x) if pd.notnull(x) else None)
    df_expense['elem'] = df_expense['elem'].fillna('hiányos')
    return df_expense

# --- MAIN SITE ---

st.title('Adat feltöltés')

st.divider()

info1, info2 = st.columns((2,1), gap='large')

with info1:
    st.write('1. Ajálnott a minta dokumentum letöltése és annak módosított verziójának visszatöltése!')
    st.write('2. A vizsgálandó adathalmaz az első munkalapon legyen.')
    st.write('3. Az első sor az oszlopazonosító, szűrési és paraméterezési adatok.')
    st.write('4. Az adat beolvasás az A:1 cellával kezdődik, így az adatnak is ott kell kezdődnie')
    st.write('5. A feltöltött excel táblák az első sorának egyeznie kell a mintában található oszlop nevekkel!')
    st.write('6. A szükséges excel táblák feltöltése és összefűzése után használható az alkalmazás.')
    
with info2:
    #Income data
    inc_data_templ = 'templates/incomes_data_template.xlsx'
    with open(inc_data_templ, 'rb') as file:
        inc_data_templ_cont = file.read()   
    st.download_button(
        label="Bevételi adat minta letöltése",
        data=inc_data_templ_cont,
        file_name="bevetel_adat_minta.xlsx",
        mime='application/excel',
        use_container_width=True)
    
    #Income category
    inc_cat_templ = 'templates/incomes_category_template.xlsx'
    with open(inc_cat_templ, 'rb') as file:
        inc_cat_templ_cont = file.read()   
    st.download_button(
        label="Bevételi kategória minta letöltése",
        data=inc_cat_templ_cont,
        file_name="bevetel_kategoria_minta.xlsx",
        mime='application/excel',
        use_container_width=True)
    
    #Expense data
    exp_data_templ = 'templates/expenses_data_template.xlsx'
    with open(exp_data_templ, 'rb') as file:
        exp_data_templ_cont = file.read()   
    st.download_button(
        label="Kiadási adat minta letöltése",
        data=exp_data_templ_cont,
        file_name="kiadas_adat_minta.xlsx",
        mime='application/excel',
        use_container_width=True)
    
    #Expense category
    exp_cat_templ = 'templates/expenses_category_template.xlsx'
    with open(exp_cat_templ, 'rb') as file:
        exp_cat_templ_cont = file.read()   
    st.download_button(
        label="Kiadási kategória minta letöltése",
        data=exp_cat_templ_cont,
        file_name="kiadas_kategoria_minta.xlsx",
        mime='application/excel',
        use_container_width=True)
    
    #Employee data
    employee_templ = 'templates/employees_template.xlsx'
    with open(employee_templ, 'rb') as file:
        employee_templ_cont = file.read()   
    st.download_button(
        label="Létszám adat minta letöltése",
        data=employee_templ_cont,
        file_name="letszam_minta.xlsx",
        mime='application/excel',
        use_container_width=True)

# --- DATA CLEANING ---

st.write('')
st.subheader('Összefűzés', divider='grey')

dcl1, dcl2 = st.columns((1,1), gap='medium')

if df_income.empty:
    if df_inc_cat.empty or df_inc_data.empty:
        dcl1.warning('Bevételi adatok összefűzéséhez töltse fel a szükséges táblákat')
    else:
        if dcl1.button('Bevételi adatok összefűzése', use_container_width=True):
            st.session_state['df_income'] = income_clean(df_inc_data, df_inc_cat)
            st.rerun()
else:
    dcl1.success('Bevételi adatok előkészítve')
    
if df_expense.empty:
    if df_exp_cat.empty or df_exp_data.empty:
        dcl2.warning('Kiadási adatok összefűzéséhez töltse fel a szükséges táblákat')
    else:
        if dcl2.button('Kiadási adatok összefűzése', use_container_width=True):
            st.session_state['df_expense'] = expense_clean(df_exp_data, df_exp_cat)
            st.rerun()
else:
    dcl2.success('Kiadási adatok előkészítve')


# --- INCOME DATA ---

st.write('')
st.subheader('Bevételi adatok', divider='grey')
inc1, inc2 = st.columns((1,3), gap='medium')

if df_inc_data.empty:
    inc1.warning('Hiányzó bevételi adat')
else:
    inc1.success('Bevételi adat feltöltve')

if df_inc_cat.empty:
    inc1.warning('Hiányzó bevételi kategória')
else:
    inc1.success('Bevételi kategória feltöltve')

with inc2.expander('Bevételi adatok'):

    inc_data = st.file_uploader('inc_data',type=['xlsx'], key=1, label_visibility='collapsed')
    
    if inc_data != None:
        df_inc_data_columns = ['partner', 'datum', 'egyseg_ar', 'deviza', 'mennyiseg', 'teljes_ar', 'teljes_forintban', 'EUR_HUF', 'kat_kod']
        temp_df_inc_data = pd.read_excel(inc_data)
        if df_inc_data_columns == temp_df_inc_data.columns.to_list():
            if st.button('Bevételi adatok mentése', use_container_width=True):
                df_inc_data = temp_df_inc_data
                del temp_df_inc_data
                st.session_state['df_inc_data'] = df_inc_data
                st.rerun()
        else:
            st.error('Helytelen oszlopnevek!')
    if not df_inc_data.empty:
        st.subheader('Aktív bevételi adatok', divider='grey')
        st.dataframe(df_inc_data)

with inc2.expander('Bevételi kategóriák'):

    inc_cat = st.file_uploader('inc_cat',type=['xlsx'], key=2, label_visibility='collapsed')
    
    if inc_cat != None:
        df_inc_cat_columns = ['kategoria', 'alkategoria', 'elem', 'kat_kod']
        temp_df_inc_cat = pd.read_excel(inc_cat)
        if df_inc_cat_columns == temp_df_inc_cat.columns.to_list():
            if st.button('Bevételi kategóriák mentése', use_container_width=True):
                df_inc_cat = temp_df_inc_cat
                del temp_df_inc_cat
                st.session_state['df_inc_cat'] = df_inc_cat
                st.rerun()
        else:
            st.error('Helytelen oszlopnevek!')
    if not df_inc_cat.empty:
        st.subheader('Aktív bevételi kategóriák', divider='grey')
        st.dataframe(df_inc_cat)

# --- EXPANSE DATA ---

st.write('')
st.subheader('Kiadási adatok', divider='grey')
exp1, exp2 = st.columns((1,3), gap='medium')

if df_exp_data.empty:
    exp1.warning('Hiányzó kiadási adat')
else:
    exp1.success('Kiadási adat feltöltve')

if df_exp_cat.empty:
    exp1.warning('Hiányzó kiadási kategória')
else:
    exp1.success('Kiadási kategória feltöltve')

with exp2.expander('Kiadási adatok'):

    exp_data = st.file_uploader('exp_data',type=['xlsx'], key=3, label_visibility='collapsed')
    
    if exp_data != None:
        df_exp_data_columns = ['ID', 'partner', 'bizonylat_szam', 'megjegyzes', 'datum', 'netto', 'kat_kod', 'fo_kat', 'forras']
        temp_df_exp_data = pd.read_excel(exp_data)
        if df_exp_data_columns == temp_df_exp_data.columns.to_list():
            if st.button('Kiadási adatok mentése', use_container_width=True):
                df_exp_data = temp_df_exp_data
                df_exp_data['bizonylat_szam'] = df_exp_data['bizonylat_szam'].apply(lambda x: str(x) if pd.notnull(x) else None)
                df_exp_data['bizonylat_szam'] = df_exp_data['bizonylat_szam'].fillna('')
                df_exp_data['megjegyzes'] = df_exp_data['megjegyzes'].apply(lambda x: str(x) if pd.notnull(x) else None)
                df_exp_data['megjegyzes'] = df_exp_data['megjegyzes'].fillna('')
                df_exp_data['kat_kod'] = df_exp_data['kat_kod'].str.strip()
                del temp_df_exp_data
                st.session_state['df_exp_data'] = df_exp_data
                st.rerun()
        else:
            st.error('Helytelen oszlopnevek!')
    if not df_exp_data.empty:
        st.subheader('Aktív kiadási adatok', divider='grey')
        st.dataframe(df_exp_data)

with exp2.expander('Kiadási kategóriák'):

    exp_cat = st.file_uploader('exp_cat',type=['xlsx'], key=4, label_visibility='collapsed')
    
    if exp_cat != None:
        df_exp_cat_columns = ['kategoria', 'alkategoria', 'elem', 'kat_kod']
        temp_df_exp_cat = pd.read_excel(exp_cat)
        if df_exp_cat_columns == temp_df_exp_cat.columns.to_list():
            if st.button('Kiadási kategóriák mentése', use_container_width=True):
                df_exp_cat = temp_df_exp_cat
                df_exp_cat['kat_kod'] = df_exp_cat['kat_kod'].str.strip()
                del temp_df_exp_cat
                st.session_state['df_exp_cat'] = df_exp_cat
                st.rerun()
        else:
            st.error('Helytelen oszlopnevek!')
    if not df_exp_cat.empty:
        st.subheader('Aktív kiadási kategóriák', divider='grey')
        st.dataframe(df_exp_cat)
        
# --- EMPLOYEE ---

st.write('')
st.subheader('Létszám adatok', divider='grey')
emp1, emp2 = st.columns((1,3), gap='medium')

if df_employees.empty:
    emp1.warning('Hiányzó létszám adat')
else:
    emp1.success('Létszám adatok feltöltve')

with emp2.expander('Létszám adatok'):

    employees = st.file_uploader('employee',type=['xlsx'], key=5, label_visibility='collapsed')
    
    if employees != None:
        df_employees_columns = ['datum', 'vam', 'penzugy', 'egyeb', 'osszes']
        temp_df_employees = pd.read_excel(employees)
        if df_employees_columns == temp_df_employees.columns.to_list():
            if st.button('Létszám adatok mentése', use_container_width=True):
                df_employees = temp_df_employees
                del temp_df_employees
                df_employees['month_year'] = df_employees['datum'].dt.to_period('m')
                df_employees = df_employees.drop(['datum'], axis=1)
                st.session_state['df_employees'] = df_employees
                st.rerun()
        else:
            st.error('Helytelen oszlopnevek!')
    if not df_employees.empty:
        st.subheader('Aktív létszám adatok', divider='grey')
        st.dataframe(df_employees)