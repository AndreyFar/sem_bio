import streamlit as st

from components.patient_table import styluj_geneticky_status
from components.urci_riziko import urci_riziko


def show(df):
    st.title("Prenášači a predispozície")

    df = df.copy()
    df["geneticky_status"] = df.apply(urci_riziko, axis=1)

    st.info("Zobrazený je zoznam pacientov s pridaným atribútom `geneticky_status`, ktorý identifikuje riziko ochorenia HH na základe mutácií.")

    df = df[["id", "vek", "pohlavie", "diagnoza_mkch-10",
             "hfe_c187g_(h63d)", "hfe_a193t_(s65c)", "hfe_g845a_(c282y)", "geneticky_status"]]
    st.dataframe(styluj_geneticky_status(df), use_container_width=True)

    prenasaci = (df["geneticky_status"] == "prenášač").sum()
    predisponovani = (df["geneticky_status"] == "predispozícia").sum()

    st.metric("Počet prenášačov", prenasaci)
    st.metric("Počet pacientov s genetickou predispozíciou", predisponovani)
