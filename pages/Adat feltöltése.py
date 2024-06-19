import streamlit as st
import pandas as pd

# ---- CONFIG ----
st.set_page_config(page_title="Beolvaso", layout="wide")

# ---- CACHEING ---

if 'df_income' not in st.session_state:
    df_income = []
if 'df_expense' not in st.session_state:
    df_expense = []
if 'df_category' not in st.session_state:
    df_category = []

# ---- MAIN SITE ---

st.header('Adat feltöltés', divider='grey')

st.write('')

info1, info2 = st.columns((1,1), gap='large')

with info1:
    st.subheader('Feltöltési útmutató', divider='grey')
    st.write('1. A feltöltendő excel csak egy munkafüzeten tartalmazhat adatot')
    st.write('2. Az első sor az oszlopazonosító')
    st.write('3. Az adat beolvasás az A:1 cellával kezdődik, így az adatnak is ott kell kezdődnie')
    st.write('4. A feltöltött excel táblákban az első sorban található oszlop neveknek meg kell egyeznie a jobb ooldalt található lenyitható részeken található oszlopnevekkel. Amennyiben ez a feltétel nem teljesül a program nem képes feldolgozni az adatokat!')
    
with info2:
    st.subheader('Szükséges oszlopok', divider='grey')
    with st.expander('Bevételi adatok oszlopok'):
        st.write('Szükséges oszlopok: kelt, netto, cat_code')
        st.caption('kelt: A kiadás dátuma, ezen érték alapján történik az időbeki szűrés')
        st.caption('netto: Számla érték, számolandó, összehasonlítandó összeg')
        st.caption('cat_code: Kategória kód, ez alapján történik a csoportosítás')
        st.write('Opcionális oszlopok')
        st.caption('partner: Tartalmazza a partner nevét')
        st.caption('bizonylat_szam: A számlához tartozó bizonylatszám')
        st.caption('megjegyzes: Bármilyen, a kiadáshoz fűzütt megjegyzés')
        st.caption('main_cat: Egyéb kategorizálási lehetőség')
        st.caption('source: Költségi fizetési formája')
    with st.expander('Kiadási adatok oszlopok'):
        st.write('Szükséges oszlopok: kelt, netto, cat_code')
        st.caption('kelt: A kiadás dátuma, ezen érték alapján történik az időbeki szűrés')
        st.caption('netto: Számla érték, számolandó, összehasonlítandó összeg')
        st.caption('cat_code: Kategória kód, ez alapján történik a csoportosítás')
        st.write('Opcionális oszlopok')
        st.caption('partner: Tartalmazza a partner nevét')
        st.caption('bizonylat_szam: A számlához tartozó bizonylatszám')
        st.caption('megjegyzes: Bármilyen, a kiadáshoz fűzütt megjegyzés')
        st.caption('main_cat: Egyéb kategorizálási lehetőség')
        st.caption('source: Költségi fizetési formája')
    with st.expander('Kiadási kategóriák oszlopok'):
        st.write('Szükséges oszlopok: Kategória, Alkategória, Elem, cat_code')
        st.caption('Kategória: Elsődleges kategória')
        st.caption('Alkategória: Második szintű kategória bontás')
        st.caption('Elem: Konkrét kategória elem')
        st.caption('cat_code: Kategória kód, ez alapján történik a csoportosítás')
        st.write('Opcionális oszlopok')
        st.caption('Régi kód: Korábban használt kategória kódoláshoz tájékoztatás')
        st.caption('Leírás: Kategória leírása')

# --- INCOME DATA ---

st.write('')
st.subheader('Bevételi adatok', divider='grey')

inc1, inc2, inc3 = st.columns((2,3,3), gap='large')

with inc1:
    st.write('Bevételi adatok feltöltése')
    income_xlsx = st.file_uploader('',type=['xlsx'], key=1, label_visibility='collapsed')
    
    if income_xlsx != None:
        temp_df_income = pd.read_excel(income_xlsx)

        st.divider()
        
        if st.button('Bevételi adatok mentése', use_container_width=True):
            df_income = temp_df_income
            del temp_df_income
            st.session_state['df_income'] = df_income
            st.rerun()

with inc2:
    st.write('Előnézet')

    if income_xlsx != None:
        st.dataframe(temp_df_income, hide_index=True)
    

with inc3:
    st.write('Aktív kiadások adatbázis')
    if 'df_income' in st.session_state:
        df_income = st.session_state['df_income']
        st.dataframe(df_income, hide_index=True)

# --- EXPANSE DATA ---

st.write('')
st.subheader('Kiadási adatok', divider='grey')

exp1, exp2, exp3 = st.columns((2,3,3), gap='large')

with exp1:
    st.write('Kiadási adatok feltöltése')
    expense_xlsx = st.file_uploader('',type=['xlsx'], key=2, label_visibility='collapsed')
    
    if expense_xlsx != None:
        temp_df_expense = pd.read_excel(expense_xlsx)

        st.divider()
        
        if st.button('Kiadási adatok mentése', use_container_width=True):
            df_expense = temp_df_expense
            del temp_df_expense
            st.session_state['df_expense'] = df_expense
            st.rerun()

with exp2:
    st.write('Előnézet')

    if expense_xlsx != None:
        st.dataframe(temp_df_expense, hide_index=True)
    

with exp3:
    st.write('Aktív kiadások adatbázis')
    if 'df_expense' in st.session_state:
        df_expense = st.session_state['df_expense']
        st.dataframe(df_expense, hide_index=True)


# --- EXPANSE CATEGORY DATA ---

st.write('')
st.subheader('Kiadási kategóriák', divider='grey')

cat1, cat2, cat3 = st.columns((2,3,3), gap='large')

with cat1:
    st.write('Kiadási kategória adatok feltöltése')
    category_xlsx = st.file_uploader('',type=['xlsx'], key=3, label_visibility='collapsed')
    
    if category_xlsx != None:
        temp_df_category = pd.read_excel(category_xlsx)

        st.divider()
        
        if st.button('Kiadási kategória adatok mentése', use_container_width=True):
            df_category = temp_df_category
            del temp_df_category
            st.session_state['df_category'] = df_category
            st.rerun()

with cat2:
    st.write('Előnézet')

    if category_xlsx != None:
        st.dataframe(temp_df_category, hide_index=True)
    

with cat3:
    st.write('Aktív kiadások adatbázis')
    if 'df_category' in st.session_state:
        df_category = st.session_state['df_category']
        st.dataframe(df_category, hide_index=True)