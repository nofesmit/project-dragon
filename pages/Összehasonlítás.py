import streamlit as st
import pandas as pd



# --- PAGE ---

st.title('Összehasonlítás')
st.divider()

# --- SESSION VARIABLES ---

if 'df_income' and 'df_expense' not in st.session_state:
    st.subheader('Nincs feltöltve vizsgálandó adat.')
    st.write('')
    st.write('Az adatok feltöltéséhez kattintson az alábbi gonbra:')
    st.write('')
    st.page_link('pages/Adatfeltöltés.py', label=' Adatfeltöltés', icon='📝')
else:
    df_income = st.session_state['df_income']
    df_expense = st.session_state['df_expense']
    
# --- INTERSACTION ---
    
    df_date = set(df_expense['month_year'].unique().tolist()).intersection(df_income['month_year'].unique().tolist())
    df_date['year'] = df_date['month_year'].year
    df_date['month'] = df_date['month_year'].month
    
    st.dataframe(df_date)

# --- FILTER ---
    
    with st.expander('Keresés és szűrés'):
        st.markdown('**A szűrési feltételek kiválaszhatók a legürgülő listából, de a mezőbe kattintva be lehet írni a keresett elemet, majd arra rákattintva kiválasztani.**')
        yfcol1, yfcol2, yfcol3 = st.columns((1,1,1), gap='medium')
        cfcol1, cfcol2, cfcol3 = st.columns((1,1,1), gap='medium')
        cfcol4, cfcol5, cfcol6 = st.columns((3,1,1), gap='medium')
    
# --- TIME FILTERS ---

    quarter_mapping = {'Q1': 1, 'Q2': 2, 'Q3': 3, 'Q4': 4}
    months_in_quarter = {
        1: [1, 2, 3],
        2: [4, 5, 6],
        3: [7, 8, 9],
        4: [10, 11, 12]}
    month_names = { 1: 'Január', 2: 'Február', 3: 'Március', 4: 'Április', 5: 'Május', 6: 'Június', 7: 'Július', 8: 'Augusztus', 9: 'Szeptember', 10: 'Október', 11: 'November', 12: 'December'}
    year = sorted(df_date['year'].unique())
    years = yfcol1.multiselect('Tárgyév', options=year, placeholder='Válassz évet',)
    if len(years) == 0:
        years = sorted(df['year'].unique())

    quarters = yfcol2.multiselect('Negyedév', options=quarter_mapping, placeholder='Válassz negyedévet')
    selected_quarters = [quarter_mapping[q] for q in quarters]
    if len(selected_quarters) == 0:
        selected_quarters = sorted(df['quarter'].unique())
    
    available_months = set()
    for q in selected_quarters:
        available_months.update(months_in_quarter[q])
        
    available_month_names = [month_names[m] for m in available_months]
    
    months = yfcol3.multiselect('Hónap', options=available_month_names, placeholder='Válassz hónapot')
    selected_months = [k for k, v in month_names.items() if v in months]
    if len(selected_months) == 0:
        selected_months = sorted(df['month'].unique())
