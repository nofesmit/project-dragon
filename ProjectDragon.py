import streamlit as st
import toml

# ----- CONFIG -----

st.set_page_config(page_title="ProjectDragon", layout="wide")

# ----- PAGE -----

st.title('Project Dragon')
st.divider()

st.write('Az alábbi mini program adatok elemzésére és vizualizálására használható. A Multilog cégcsoport számára kialakított rendszer alapját előre előkészített excel táblák adják. Ezekenek a tábláknak az előkészítése és megfelelő formában történő feltöltése elengedhetetlen a program megfelelő máködéséhez')

st.write('Az oldalak között a bal oldalon található menüpontokra kattintva lehet navigálni.')
st.write('Az adatok elemzéséhez először fel kell tölteni minden szükséges fájlt. Ezen fájlok listáját az adott oldalon lehet ellenőrizni. A funkciók nem jelennek meg, ameddig nincs minden szükséges adat feltöltve a rendszerbe.')
st.write('A program ideiglenes változókkal működik, semmilyen adat nem kerül mentésre!')
st.write('Az oldal frissítése után az ideiglenes változók elvesznek!')

st.caption('A programot Simon Kristóf készítette, kérdéssel és megláttással őt kell keresni.')