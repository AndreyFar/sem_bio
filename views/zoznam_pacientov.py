import streamlit as st

from components.filters import filter_patients
from components.patient_table import show_patient_table


def show(df):
    st.title("Zoznam pacientov")
    df = df.copy()

    df_filtered = filter_patients(df)
    show_patient_table(df_filtered, styled=True)

    prenasaci = (df_filtered["geneticky_status"] == "prenášač").sum()
    predisponovani = (df_filtered["geneticky_status"] == "predispozícia").sum()

    st.metric("Počet prenášačov", prenasaci)
    st.metric("Počet pacientov s genetickou predispozíciou", predisponovani)
