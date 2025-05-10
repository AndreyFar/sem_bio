import streamlit as st
from process.data_processing import load_data, normalize_data, clean_data
from views import domov, o_nas, kontakt, zoznam_pacientov, hwe_testy, prenasaci_predispozicia, diagnozy

st.set_page_config(page_title="HH Centrum", layout="wide")

# CSS úpravy
st.markdown(
    """
    <style>
        #MainMenu, footer {visibility: hidden;}
        .css-6qob1r.eczjsme10 {padding-top: 1rem;}
        .stRadio > div {gap: 0.5rem;}
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar nadpis
st.sidebar.markdown(
    """
    <div style='text-align: center; font-size: 24px; font-weight: bold; padding: 10px 0;'>
        HH Centrum
    </div>
    <hr style="margin-top: 0;">
    """,
    unsafe_allow_html=True
)

# Načítanie a spracovanie dát
df_raw = load_data("data/SSBU25_data.csv")
df_normalized = normalize_data(df_raw)
df_clean = clean_data(df_normalized, verbose=False)

# Navigácia
stranka = st.sidebar.radio(
    "Navigácia",
    ["Domov", "O nás", "Kontakt", "Zoznam pacientov", "HWE testy", "Prenášači a predispozícia", "Diagnózy"]
)

# Obsah podľa výberu
if stranka == "Domov":
    domov.show()

elif stranka == "O nás":
    o_nas.show()

elif stranka == "Kontakt":
    kontakt.show()

elif stranka == "Zoznam pacientov":
    zoznam_pacientov.show(df_clean)

elif stranka == "HWE testy":
    hwe_testy.show(df_clean)

elif stranka == "Prenášači a predispozícia":
    prenasaci_predispozicia.show(df_clean)

elif stranka == "Diagnózy":
    diagnozy.show(df_clean)
