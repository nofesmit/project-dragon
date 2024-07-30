import streamlit as st

# --- CONFIG ---

st.set_page_config(page_title="ProjectDragon", layout="wide", page_icon='dragon')

hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

# --- PAGE ---


st.title('Project Dragon')

st.divider()

col1, col2 = st.columns((2,1))

with col2:
    st.image('images/project_dragon_logo.png')

with col1:
    st.write('A Project Dragon bevételi és kiadási adatok elemzéséhez jött létre.')
    st.write('')
    st.write('''A Multilog cégcsoport számára kialakított program alapját excel táblákból nyert adatok adják. 
            A minta excel táblák az "Adatfeltöltés" menüpont alatt letölthetők. 
            Az adattal feltöltött táblák visszatöltését követően az adatok elemzése és vizualizálása a "Bevételek", "Kiadások" és "Összehasonlítások" menüpont alatt elérhető''')
    st.write('')
    st.write('''Az alkalmazásban való navigáláshoz a bal oldali, összecsukható sáv használandó. 
            A program ideiglenes változókkal működik, semmilyen adat nem kerül mentésre! 
            Az oldal frissítése után az ideiglenes változók elvesznek!''')
    st.write('')
    st.caption('A programot Simon Kristóf készítette.')