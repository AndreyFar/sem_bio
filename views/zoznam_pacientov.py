import streamlit as st

from components.filters import filter_patients
from components.patient_table import show_patient_table


def show(df):
    st.title("Zoznam pacientov")

    # Výber filtrov
    df_filtered = filter_patients(df)

    # Zobrazenie tabuľky
    show_patient_table(df_filtered)
