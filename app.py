import streamlit as st
from process.data_processing import load_data, normalize_data, clean_data

# Načítanie a čistenie dát
df_raw = load_data("data/SSBU25_data.csv")
df_normalized = normalize_data(df_raw)
df_clean = clean_data(df_normalized, False)

# Nastavenie rozloženia stránky
st.set_page_config(page_title="HH Centrum", layout="wide")

# Sidebar menu
st.sidebar.title("Menu")
stranka = st.sidebar.radio("Navigácia", ["Domov", "O nás", "Kontakt", "Zoznam pacientov"])

# Obsah stránky podľa výberu
if stranka == "Domov":
    st.title("Vitaj na stránke!")
    st.write("Vyber si možnosť z menu naľavo.")
elif stranka == "O nás":
    st.title("O nás")
    st.write("Sme odborné centrum pre analýzu vzoriek.")
elif stranka == "Kontakt":
    st.title("Kontakt")
    st.write("Email: kontakt@hhcentrum.sk")
    st.write("el: +421 123 456 789")
elif stranka == "Zoznam pacientov":
    st.title("Zoznam pacientov")

    vek_filter = st.slider("Zobraziť pacientov nad vek", min_value=0, max_value=100, value=0)

    if "vek" in df_clean.columns:
        df_filtered = df_clean[df_clean["vek"] > vek_filter]
    else:
        st.write("Dataset neobsahuje stĺpec 'vek'. Skontroluj názvy stĺpcov.")

    st.dataframe(df_filtered, use_container_width=True)
