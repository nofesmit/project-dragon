import streamlit as st
import pandas as pd

# ---- CONFIG ----
st.set_page_config(page_title="Beolvaso", layout="wide")

st.title('Excel beolvasó')

col1, col2 = st.columns((1,1),gap='large')

with col1:
    st.subheader('Feltöltési útmutató')
    st.write('1. A feltöltendő excel csak egy munkafüzeten tartalmazhat adatot')
    st.write('2. Az első sor az oszlopazonosító')
    st.write('3. Az adat beolvasás az A:1 cellával kezdődik, így az adatnak is ott kell kezdődnie')
    st.write('')
    data_xlsx = st.file_uploader('',type=['xlsx'])
    st.divider()
    
    if data_xlsx != None:
        data = pd.read_excel(data_xlsx)
        col_name = data.columns.to_list()
        container = st.container()
        select_all = st.checkbox("Összes kijelölése", default=True)
        
        if select_all:
            selected_col = container.multiselect('Kiválasztott oszlopok', col_name, default=col_name)
        else:
            selected_col = container.multiselect('Kiválasztott oszlopok', col_name)


with col2:
    st.subheader('Excel előlnézet')
    if data_xlsx != None:
        filtered_data = data.loc[:,selected_col]
        st.dataframe(filtered_data, hide_index=True)
    else:
        st.write('')
        st.write('A fájl feltöltését követően látható az előnézet!')