import streamlit as st
from pages import domov, o_nas, kontakt, zoznam_pacientov

st.set_page_config(page_title="HH Centrum", layout="wide")

st.sidebar.title("Menu")
stranka = st.sidebar.radio("Navigácia", ["Domov", "O nás", "Kontakt", "Zoznam pacientov"])

if stranka == "Domov":
    domov.show()

elif stranka == "O nás":
    o_nas.show()

elif stranka == "Kontakt":
    kontakt.show()

elif stranka == "Zoznam pacientov":
    zoznam_pacientov.show()
