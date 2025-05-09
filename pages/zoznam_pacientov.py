import streamlit as st
import pandas as pd

from process.data_processing import load_data, normalize_data, clean_data
from components.filters import filter_patients
from components.patient_table import show_patient_table

def show():
    st.title("Zoznam pacientov")

    # Načítanie a spracovanie dát
    df_raw = load_data("data/SSBU25_data.csv")
    df = clean_data(normalize_data(df_raw), False)

    # Výber filtrov
    df_filtered = filter_patients(df)

    # Zobrazenie tabuľky
    show_patient_table(df_filtered)
