import streamlit as st
import pandas as pd
from components.diagnozy_skupiny import DG_SKUPINY, patri_do_skupiny


def filter_patients(df):
    df_filtered = df.copy()

    with st.expander("Filtrovať pacientov"):
        id_filter = st.text_input("Vyhľadať pacienta podľa ID (presný zápis)")

        # Ak je zadané ID, filtrujeme podľa neho a ostatné filtre vypneme
        if id_filter.strip():
            df_filtered = df_filtered[df_filtered["id"].astype(str) == id_filter.strip()]
            return df_filtered

        vek_range = st.slider("Rozsah veku pacienta", min_value=0, max_value=100, value=(0, 100))
        pohlavie_filter = st.multiselect("Pohlavie", options=["M", "F"], default=["M", "F"])
        diagnoza_filter = st.text_input("Diagnoza (MKCH-10)")

        dg_skupiny_filter = st.multiselect("Skupiny diagnóz", options=list(DG_SKUPINY.keys()))

        hfe_h63d = st.selectbox("Mutácia HFE_C187G (H63D)", ["Všetky", "normal", "heterozygot", "mutant"])
        hfe_s65c = st.selectbox("Mutácia HFE_A193T (S65C)", ["Všetky", "normal", "heterozygot", "mutant"])
        hfe_c282y = st.selectbox("Mutácia HFE_G845A (C282Y)", ["Všetky", "normal", "heterozygot", "mutant"])

        prijem_range = st.date_input(
            "Rozsah dátumu prijatia vzorky",
            value=(pd.to_datetime("2000-01-01").date(), pd.to_datetime("today").date())
        )
        vysledok_range = st.date_input(
            "Rozsah dátumu výsledku",
            value=(pd.to_datetime("2000-01-01").date(), pd.to_datetime("today").date())
        )

        status_options = df["geneticky_status"].dropna().unique().tolist()
        geneticky_status_filter = st.multiselect(
            "Genetický status",
            options=status_options,
            default=status_options
        )

        if st.button("Aplikovať filtre"):
            df_filtered = df_filtered[
                (df_filtered["vek"] >= vek_range[0]) & (df_filtered["vek"] <= vek_range[1])
                ]
            df_filtered = df_filtered[df_filtered["pohlavie"].isin(pohlavie_filter)]

            if diagnoza_filter:
                df_filtered = df_filtered[
                    df_filtered["diagnoza_mkch-10"].str.contains(diagnoza_filter, case=False, na=False)
                ]

            if dg_skupiny_filter:
                def patri_do_vybranych_skupin(kod):
                    return any(patri_do_skupiny(kod, DG_SKUPINY[skupina]) for skupina in dg_skupiny_filter)

                df_filtered = df_filtered[df_filtered["diagnoza_mkch-10"].apply(patri_do_vybranych_skupin)]

            if hfe_h63d != "Všetky":
                df_filtered = df_filtered[df_filtered["hfe_c187g_(h63d)"] == hfe_h63d]
            if hfe_s65c != "Všetky":
                df_filtered = df_filtered[df_filtered["hfe_a193t_(s65c)"] == hfe_s65c]
            if hfe_c282y != "Všetky":
                df_filtered = df_filtered[df_filtered["hfe_g845a_(c282y)"] == hfe_c282y]

            df_filtered = df_filtered[
                (df_filtered["prijem_vzorky"].dt.date >= prijem_range[0]) &
                (df_filtered["prijem_vzorky"].dt.date <= prijem_range[1])
                ]
            df_filtered = df_filtered[
                (df_filtered["validovany_vysledok"].dt.date >= vysledok_range[0]) &
                (df_filtered["validovany_vysledok"].dt.date <= vysledok_range[1])
                ]

            if geneticky_status_filter:
                df_filtered = df_filtered[df_filtered["geneticky_status"].isin(geneticky_status_filter)]

    return df_filtered
