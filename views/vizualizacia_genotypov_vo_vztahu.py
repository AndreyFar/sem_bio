import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 
from scipy.interpolate import CubicSpline 
from views.diagnozy import DG_SKUPINY  # Import DG_SKUPINY


def show(df):
    st.title("Vizuálna analýza rozdelenia genotypov")

    # Zoznam dostupných grafov
    grafy = {
        "Rozdelenie genotypov": "genotypy",
        "Vek vs. genotyp": "vek",
        "Pohlavie vs. genotyp": "pohlavie",
        "Diagnózy vs. genotyp": "diagnozy"
    }

    # Výber grafu
    vybrany_graf = st.selectbox("Vyber graf, ktorý chceš zobraziť:", list(grafy.keys()))

    if vybrany_graf == "Rozdelenie genotypov":
        zobraz_rozdelenie_genotypov(df)
    elif vybrany_graf == "Vek vs. genotyp":
        zobraz_vek_vs_genotyp(df)
    elif vybrany_graf == "Pohlavie vs. genotyp":
        zobraz_pohlavie_vs_genotyp(df)
    elif vybrany_graf == "Diagnózy vs. genotyp":
        zobraz_diagnozy_vs_genotyp(df)


def zobraz_rozdelenie_genotypov(df):
    st.header("Rozdelenie genotypov")
    cols = st.columns(3)  # Vytvoríme 3 stĺpce

    for i, mutacia in enumerate(['hfe_c187g_(h63d)', 'hfe_a193t_(s65c)', 'hfe_g845a_(c282y)']):
        if mutacia not in df.columns:
            st.error(f"Chyba: Stĺpec '{mutacia}' nenájdený v DataFrame.")
            continue

        with cols[i]:  # Používame stĺpec pre danú mutáciu
            st.subheader(f"Mutácia: {mutacia}")
            genotyp_counts = df[mutacia].value_counts()
            fig_genotyp, ax_genotyp = plt.subplots()
            ax_genotyp.bar(genotyp_counts.index, genotyp_counts.values)
            ax_genotyp.set_xlabel("Genotyp")
            ax_genotyp.set_ylabel("Počet pacientov")
            st.pyplot(fig_genotyp)


def zobraz_vek_vs_genotyp(df):
    st.header("Vek vs. počet pacientov (plynulé čiary)")
    cols = st.columns(3)

    for i, mutacia in enumerate(['hfe_c187g_(h63d)', 'hfe_a193t_(s65c)', 'hfe_g845a_(c282y)']):
        if mutacia not in df.columns:
            st.error(f"Chyba: Stĺpec '{mutacia}' nenájdený v DataFrame.")
            continue

        with cols[i]:
            st.subheader(f"Mutácia: {mutacia}")
            fig_vek, ax_vek = plt.subplots()
            for genotyp in df[mutacia].unique():
                df_genotyp = df[df[mutacia] == genotyp]
                hist, bins = np.histogram(df_genotyp['vek'], bins=20)  # Vypočítame histogram

                # Použijeme CubicSpline na interpoláciu
                cs = CubicSpline(bins[:-1], hist)
                vek_hladke = np.linspace(bins.min(), bins.max(), 200)  # Viac bodov pre plynulú čiaru
                ax_vek.plot(vek_hladke, cs(vek_hladke), label=genotyp)

            ax_vek.set_xlabel("Vek")
            ax_vek.set_ylabel("Počet pacientov")
            ax_vek.legend()
            st.pyplot(fig_vek)

def zobraz_pohlavie_vs_genotyp(df):
    st.header("Pohlavie vs. genotyp")
    cols = st.columns(3)

    for i, mutacia in enumerate(['hfe_c187g_(h63d)', 'hfe_a193t_(s65c)', 'hfe_g845a_(c282y)']):
        if mutacia not in df.columns:
            st.error(f"Chyba: Stĺpec '{mutacia}' nenájdený v DataFrame.")
            continue
        with cols[i]:
            st.subheader(f"Mutácia: {mutacia}")
            pohlavie_genotyp = df.groupby(['pohlavie', mutacia]).size().unstack(fill_value=0)

            # Vytvoríme Figure a Axes
            fig_pohlavie, ax_pohlavie = plt.subplots()

            # Vykreslíme graf na Axes
            pohlavie_genotyp.plot(kind='bar', stacked=True, ax=ax_pohlavie)

            ax_pohlavie.set_ylabel("Počet pacientov")
            ax_pohlavie.set_xlabel("Pohlavie")
            ax_pohlavie.legend(title="Genotyp")

            # Odovzdáme Figure Streamlitu
            st.pyplot(fig_pohlavie)


def zobraz_diagnozy_vs_genotyp(df):
    st.header("Diagnózy vs. genotyp")

    # Používame DG_SKUPINY na výber diagnóz
    vybrana_skupina = st.selectbox("Vyber skupinu diagnóz", list(DG_SKUPINY.keys()))
    pecen_diagnozy = DG_SKUPINY[vybrana_skupina]

    st.subheader(f"Analýza pre skupinu diagnóz: {vybrana_skupina}")
    cols = st.columns(3)

    for i, mutacia in enumerate(['hfe_c187g_(h63d)', 'hfe_a193t_(s65c)', 'hfe_g845a_(c282y)']):
        if mutacia not in df.columns:
            st.error(f"Chyba: Stĺpec '{mutacia}' nenájdený v DataFrame.")
            continue

        with cols[i]:
            st.subheader(f"Mutácia: {mutacia}")
            df['ma_dg'] = df['diagnoza_mkch-10'].isin(pecen_diagnozy)
            # Nahradíme True/False za "Má"/"Nemá"
            df['ma_dg_label'] = df['ma_dg'].apply(lambda x: 'Má' if x else 'Nemá')
            pecen_genotyp = df.groupby(['ma_dg_label', mutacia]).size().unstack(fill_value=0)

            # Vytvoríme Figure a Axes
            fig_pecen, ax_pecen = plt.subplots()

            # Vykreslíme graf na Axes
            pecen_genotyp.plot(kind='bar', stacked=False, ax=ax_pecen)

            ax_pecen.set_ylabel("Počet pacientov")
            ax_pecen.set_xlabel(f"Má diagnózu z oblasti {vybrana_skupina}")
            ax_pecen.legend(title="Genotyp")

            # Odovzdáme Figure Streamlitu
            st.pyplot(fig_pecen)