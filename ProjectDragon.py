import streamlit as st
import toml

# ----- CONFIG -----

st.set_page_config(page_title="ProjectDragon", layout="wide")

def update_theme_toml(theme_colors):
    config_path = ".streamlit/config.toml"

    with open(config_path, "r") as file:
        config = toml.load(file)
    
    config['theme']['primaryColor'] = theme_colors['primaryColor']
    config['theme']['backgroundColor'] = theme_colors['backgroundColor']
    config['theme']['secondaryBackgroundColor'] = theme_colors['secondaryBackgroundColor']
    config['theme']['textColor'] = theme_colors['textColor']
    
    with open(config_path, "w") as file:
        toml.dump(config, file)

# ----- PAGE -----

st.title('Project Dragon')
st.divider()

st.write('Az alábbi mini program adatok elemzésére és vizualizálására használható. A Multilog cégcsoport számára kialakított rendszer alapját előre előkészített excel táblák adják. Ezekenek a tábláknak az előkészítése és megfelelő formában történő feltöltése elengedhetetlen a program megfelelő máködéséhez')

st.write('Az oldalak között a bal oldalon található menüpontokra kattintva lehet navigálni.')
st.write('Az adatok elemzéséhez először fel kell tölteni minden szükséges fájlt. Ezen fájlok listáját az adott oldalon lehet ellenőrizni. A funkciók nem jelennek meg, ameddig nincs minden szükséges adat feltöltve a rendszerbe.')
st.write('A program ideiglenes változókkal működik, semmilyen adat nem kerül mentésre!')
st.write('Az oldal frissítése után az ideiglenes változók elvesznek!')

st.caption('A programot Simon Kristóf készítette, kérdéssel és megláttással őt kell keresni.')

st.header('Theme', divider='grey')

tcol1, tcol2 = st.columns((1,1))

if tcol1.button("Light", use_container_width=True, type='primary'):
    theme_colors = {
        'primaryColor': '#6D87BD',
        'backgroundColor': "#D1D1D1",
        'secondaryBackgroundColor': "#C1C1C1",
        'textColor': '#292929',
    }
    update_theme_toml(theme_colors)

if tcol2.button("Dark", use_container_width=True, type='primary'):
    theme_colors = {
        'primaryColor': '#6D87BD',
        'backgroundColor': '#4A4A4A',
        'secondaryBackgroundColor': '#232323',
        'textColor': "#F4F4F4",
    }
    update_theme_toml(theme_colors)
