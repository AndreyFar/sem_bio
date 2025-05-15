import streamlit as st
import matplotlib.pyplot as plt
from components.urci_riziko import urci_riziko
from components.diagnozy_skupiny import DG_SKUPINY, patri_do_skupiny


def show(df):
    st.title("Vzťah medzi genetickým rizikom a diagnózami")

    vyber = st.selectbox("Vyber oblasť diagnóz", list(DG_SKUPINY.keys()))
    rozsah = DG_SKUPINY[vyber]

    st.markdown(f"Analýza diagnóz pre oblasť **{vyber}** (interval: {rozsah[0]}–{rozsah[1]}).")
    df['riziko'] = df.apply(urci_riziko, axis=1)
    df['ma_dg'] = df['diagnoza_mkch-10'].apply(lambda kod: patri_do_skupiny(kod, rozsah))

    grouped = df.groupby('riziko')['ma_dg'].agg(['sum', 'count'])
    grouped['podiel'] = grouped['sum'] / grouped['count'] * 100

    # tabulka
    st.dataframe(grouped.rename(columns={
        'sum': 'Počet s diagnózou',
        'count': 'Počet v skupine',
        'podiel': 'Podiel [%]'
    }))

    # graf
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.bar(grouped.index, grouped['podiel'], color=['green', 'orange', 'red'])
        ax.set_ylabel("Podiel [%]", fontsize=10)
        ax.set_xlabel("Genetické riziko", fontsize=10)
        ax.set_ylim(0, 100)
        ax.tick_params(axis='both', labelsize=8)
        ax.set_title("", fontsize=12)
        plt.tight_layout()
        st.pyplot(fig)
