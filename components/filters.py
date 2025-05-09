import streamlit as st
import pandas as pd

def filter_patients(df):
    df_filtered = df.copy()

    with st.expander("Filtrovať pacientov"):
        vek_filter = st.slider("Zobraziť pacientov nad vek", min_value=0, max_value=100, value=0)
        pohlavie_filter = st.multiselect("Pohlavie", options=["M", "F"], default=["M", "F"])
        diagnoza_filter = st.text_input("Diagnoza (MKCH-10)")

        hfe_h63d = st.selectbox("Mutácia HFE_C187G (H63D)", ["Všetky", "normal", "heterozygot", "mutant"])
        hfe_s65c = st.selectbox("Mutácia HFE_A193T (S65C)", ["Všetky", "normal", "heterozygot", "mutant"])
        hfe_c282y = st.selectbox("Mutácia HFE_G845A (C282Y)", ["Všetky", "normal", "heterozygot", "mutant"])

        prijem_start = st.date_input("Začiatok dátumu prijatia vzorky", pd.to_datetime("2000-01-01").date())
        prijem_end = st.date_input("Koniec dátumu prijatia vzorky", pd.to_datetime("today").date())

        vysledok_start = st.date_input("Začiatok dátumu výsledku", pd.to_datetime("2000-01-01").date())
        vysledok_end = st.date_input("Koniec dátumu výsledku", pd.to_datetime("today").date())

        if st.button("Aplikovať filtre"):
            df_filtered = df_filtered[df_filtered["vek"] > vek_filter]
            df_filtered = df_filtered[df_filtered["pohlavie"].isin(pohlavie_filter)]
            if diagnoza_filter:
                df_filtered = df_filtered[df_filtered["diagnoza_mkch-10"].str.contains(diagnoza_filter, case=False, na=False)]
            if hfe_h63d != "Všetky":
                df_filtered = df_filtered[df_filtered["hfe_c187g_(h63d)"] == hfe_h63d]
            if hfe_s65c != "Všetky":
                df_filtered = df_filtered[df_filtered["hfe_a193t_(s65c)"] == hfe_s65c]
            if hfe_c282y != "Všetky":
                df_filtered = df_filtered[df_filtered["hfe_g845a_(c282y)"] == hfe_c282y]
            df_filtered = df_filtered[
                (df_filtered["prijem_vzorky"].dt.date >= prijem_start) &
                (df_filtered["prijem_vzorky"].dt.date <= prijem_end)
                ]
            df_filtered = df_filtered[
                (df_filtered["validovany_vysledok"].dt.date >= vysledok_start) &
                (df_filtered["validovany_vysledok"].dt.date <= vysledok_end)
                ]

    return df_filtered
