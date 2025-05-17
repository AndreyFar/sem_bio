import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.interpolate import CubicSpline
from components.diagnozy_skupiny import DG_SKUPINY, patri_do_skupiny  # Import DG_SKUPINY


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
    cols = st.columns(3)

    for i, mutacia in enumerate(['hfe_c187g_(h63d)', 'hfe_a193t_(s65c)', 'hfe_g845a_(c282y)']):
        if mutacia not in df.columns:
            st.error(f"Chyba: Stĺpec '{mutacia}' nenájdený v DataFrame.")
            continue

        with cols[i]:
            st.subheader(f"Mutácia: {mutacia}")
            genotyp_counts = df[mutacia].value_counts()
            fig_genotyp, ax_genotyp = plt.subplots()
            ax_genotyp.bar(genotyp_counts.index, genotyp_counts.values)
            ax_genotyp.set_xlabel("Genotyp")
            ax_genotyp.set_ylabel("Počet pacientov")
            st.pyplot(fig_genotyp)


def zobraz_vek_vs_genotyp(df):
    st.header("Vzťah medzi vekom pacienta a prítomnosťou konkrétneho genotypu")
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
                hist, bins = np.histogram(df_genotyp['vek'], bins=20)

                # Použijeme CubicSpline na interpoláciu
                cs = CubicSpline(bins[:-1], hist)
                vek_hladke = np.linspace(bins.min(), bins.max(), 200)
                ax_vek.plot(vek_hladke, cs(vek_hladke), label=genotyp)

            ax_vek.set_xlabel("Vek")
            ax_vek.set_ylabel("Počet pacientov")
            ax_vek.legend()
            st.pyplot(fig_vek)


def zobraz_pohlavie_vs_genotyp(df):
    st.header("Porovnanie distribúcie genotypov medzi mužmi a ženami")

    genotyp_order = ['heterozygot', 'mutant', 'normal']
    color_map = {
        'heterozygot': 'blue',
        'mutant': 'orange',
        'normal': 'green'
    }

    cols = st.columns(3)

    for i, mutacia in enumerate(['hfe_c187g_(h63d)', 'hfe_a193t_(s65c)', 'hfe_g845a_(c282y)']):
        if mutacia not in df.columns:
            st.error(f"Chyba: Stĺpec '{mutacia}' nenájdený v DataFrame.")
            continue
        with cols[i]:
            st.subheader(f"Mutácia: {mutacia}")
            pohlavie_genotyp = df.groupby(['pohlavie', mutacia]).size().unstack(fill_value=0)

            plot_columns = [col for col in genotyp_order if col in pohlavie_genotyp.columns]

            if not plot_columns:
                st.write("Pre túto mutáciu nie sú k dispozícii žiadne dáta o genotypoch na zobrazenie.")
                continue

            pohlavie_genotyp_ordered = pohlavie_genotyp[plot_columns]
            plot_colors = [color_map[col] for col in plot_columns if col in color_map]

            if len(plot_colors) != len(plot_columns):
                st.warning(
                    f"Niektorým genotypom v mutácii {mutacia} nebola priradená farba. Použijú sa predvolené farby.")
                current_plot_colors = None
            else:
                current_plot_colors = plot_colors

            fig_pohlavie, ax_pohlavie = plt.subplots()

            # Vykreslíme graf
            pohlavie_genotyp_ordered.plot(
                kind='bar',
                stacked=True,
                ax=ax_pohlavie,
                color=current_plot_colors
            )

            ax_pohlavie.set_ylabel("Počet pacientov")
            ax_pohlavie.set_xlabel("Pohlavie")
            ax_pohlavie.legend(title="Genotyp")

            # Odovzdáme Figure Streamlitu
            st.pyplot(fig_pohlavie)
            plt.close(fig_pohlavie)


def zobraz_diagnozy_vs_genotyp(df):
    st.header("Výskyt genotypov v rôznych diagnostických kategóriách")

    genotyp_order = ['heterozygot', 'mutant', 'normal']
    color_map = {
        'heterozygot': 'blue',
        'mutant': 'orange',
        'normal': 'green'
    }

    vybrana_skupina = st.selectbox("Vyber skupinu diagnóz", list(DG_SKUPINY.keys()))
    rozsah = DG_SKUPINY[vybrana_skupina]

    st.subheader(f"Analýza pre skupinu diagnóz: {vybrana_skupina}")
    cols = st.columns(3)

    for i, mutacia in enumerate(['hfe_c187g_(h63d)', 'hfe_a193t_(s65c)', 'hfe_g845a_(c282y)']):
        if mutacia not in df.columns:
            st.error(f"Chyba: Stĺpec '{mutacia}' nenájdený v DataFrame.")
            continue

        with cols[i]:
            st.subheader(f"Mutácia: {mutacia}")
            df_copy = df.copy()
            df_copy['ma_dg'] = df_copy['diagnoza_mkch-10'].apply(lambda kod: patri_do_skupiny(kod, rozsah))
            df_copy['ma_dg_label'] = df_copy['ma_dg'].apply(lambda x: 'Má' if x else 'Nemá')
            pecen_genotyp = df_copy.groupby(['ma_dg_label', mutacia]).size().unstack(fill_value=0)

            plot_columns = [col for col in genotyp_order if col in pecen_genotyp.columns]

            if not plot_columns:
                st.write(
                    "Pre túto mutáciu a diagnostickú skupinu nie sú k dispozícii žiadne dáta o genotypoch na zobrazenie.")
                continue

            pecen_genotyp_ordered = pecen_genotyp[plot_columns]
            plot_colors = [color_map[col] for col in plot_columns if col in color_map]

            if len(plot_colors) != len(plot_columns):
                st.warning(
                    f"Niektorým genotypom v mutácii {mutacia} (diagnózy) nebola priradená farba. Použijú sa predvolené farby.")
                current_plot_colors = None
            else:
                current_plot_colors = plot_colors

            fig_pecen, ax_pecen = plt.subplots()
            pecen_genotyp_ordered.plot(
                kind='bar',
                stacked=False,
                ax=ax_pecen,
                color=current_plot_colors
            )

            ax_pecen.set_ylabel("Počet pacientov")
            ax_pecen.set_xlabel(f"Má diagnózu z oblasti {vybrana_skupina}")
            ax_pecen.legend(title="Genotyp")
            st.pyplot(fig_pecen)
            plt.close(fig_pecen)
