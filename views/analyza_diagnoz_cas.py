import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from components.diagnozy_skupiny import DG_SKUPINY, patri_do_skupiny

# Pomocná funkcia na priradenie skupiny diagnózy z existujúceho kódu
def prirad_skupinu_diagnozy(kod_diagnozy, dg_skupiny_dict):
    if pd.isna(kod_diagnozy):
        return "Neznáma diagnóza"
    for skupina, (start_kod, end_kod) in dg_skupiny_dict.items():
        if patri_do_skupiny(str(kod_diagnozy), (start_kod, end_kod)):
            return skupina
    return "Iné (mimo definovaných skupín)"

def show(df_loaded):
    st.title("Analýza diagnóz MKCH-10 a ich vývoj v čase")

    if df_loaded.empty:
        st.warning("Neboli načítané žiadne dáta na analýzu.")
        return

    df = df_loaded.copy()

    # --- 1. Príprava dát pre časovú analýzu ---
    if 'validovany_vysledok' not in df.columns:
        st.error("Kritický stĺpec 'validovany_vysledok' chýba v dátach.")
        return
    
    df['validovany_vysledok'] = pd.to_datetime(df['validovany_vysledok'], errors='coerce')
    df.dropna(subset=['validovany_vysledok'], inplace=True)
    if df.empty:
        st.warning("Po odstránení záznamov bez platného dátumu výsledku nezostali žiadne dáta.")
        return
        
    df['rok_vysetrenia'] = df['validovany_vysledok'].dt.year
    df['rok_vysetrenia'] = df['rok_vysetrenia'].astype(int)

    if 'diagnoza_mkch-10' not in df.columns:
        st.error("Kritický stĺpec 'diagnoza_mkch-10' chýba v dátach.")
        return

    df['skupina_diagnozy'] = df['diagnoza_mkch-10'].apply(lambda x: prirad_skupinu_diagnozy(x, DG_SKUPINY))

    # --- Vývoj počtu diagnóz v čase podľa skupín (Tabuľka) ---
    st.header("Vývoj počtu diagnóz v čase podľa skupín")
    diag_over_time = df.groupby(['rok_vysetrenia', 'skupina_diagnozy']).size().reset_index(name='pocet')
    
    if not diag_over_time.empty:
        diag_over_time_pivot = diag_over_time.pivot(index='rok_vysetrenia', columns='skupina_diagnozy', values='pocet').fillna(0)
        
        st.subheader("Tabuľkový prehľad počtu diagnóz podľa skupín a rokov")
        st.dataframe(diag_over_time_pivot.style.format("{:.0f}"))

        # --- Grafický prehľad vývoja počtu diagnóz (s výberom) ---
        st.subheader("Grafický prehľad vývoja počtu diagnóz podľa skupín")
        
        available_groups_for_plot = diag_over_time_pivot.columns.tolist()
        
        # Predvolený výber - napr. prvých 5 skupín, ak ich je toľko, inak všetky dostupné.
        # Ak je dostupná len jedna, vyberieme ju. Ak žiadna, zoznam bude prázdny.
        if len(available_groups_for_plot) > 5:
            default_selected_groups = available_groups_for_plot[:5]
        elif len(available_groups_for_plot) > 0:
            default_selected_groups = available_groups_for_plot
        else:
            default_selected_groups = []

        selected_groups_for_plot_input = st.multiselect(
            "Vyberte skupiny diagnóz pre zobrazenie v grafe:",
            options=available_groups_for_plot,
            default=default_selected_groups,
            key="multiselect_diag_groups_plot" 
        )

        if selected_groups_for_plot_input:
            df_to_plot = diag_over_time_pivot[selected_groups_for_plot_input]
            # Odstrániť stĺpce, ktoré sú celé nulové, aby sa nekreslili prázdne čiary
            df_to_plot_non_zero = df_to_plot.loc[:, (df_to_plot != 0).any(axis=0)]

            if not df_to_plot_non_zero.empty and not df_to_plot_non_zero.columns.empty:
                fig1, ax1 = plt.subplots(figsize=(14, 7))
                
                num_lines = len(df_to_plot_non_zero.columns)
                plot_colors = []
                if num_lines > 0:
                    if num_lines <= 10:
                        # Použije prvých num_lines farieb z 'tab10'
                        plot_colors = plt.cm.get_cmap('tab10').colors[:num_lines]
                    elif num_lines <= 20:
                        # Použije prvých num_lines farieb z 'tab20'
                        plot_colors = plt.cm.get_cmap('tab20').colors[:num_lines]
                    else:
                        # Pre viac ako 20 farieb, použijeme 'gist_rainbow' alebo inú vhodnú mapu
                        # a rovnomerne z nej vyberieme farby
                        cmap_long = plt.cm.get_cmap('gist_rainbow', num_lines) 
                        plot_colors = [cmap_long(i) for i in range(num_lines)]
                
                for i, column in enumerate(df_to_plot_non_zero.columns):
                    ax1.plot(df_to_plot_non_zero.index, df_to_plot_non_zero[column], 
                             marker='o', linestyle='-', label=column, color=plot_colors[i])
                
                ax1.set_xlabel("Rok vyšetrenia")
                ax1.set_ylabel("Počet diagnóz")
                ax1.legend(title="Skupina diagnóz", bbox_to_anchor=(1.05, 1), loc='upper left')
                ax1.grid(True, linestyle='--', alpha=0.7)
                plt.xticks(rotation=45)
                # Nastavenie osi X pre lepšiu čitateľnosť rokov
                ax1.xaxis.set_major_locator(mticker.MaxNLocator(integer=True, prune='both', nbins='auto'))
                fig1.tight_layout() # Automatické prispôsobenie layoutu
                st.pyplot(fig1)
            else:
                st.info("Pre vybrané skupiny neboli nájdené žiadne nenulové dáta na zobrazenie v grafe, alebo všetky vybrané skupiny mali nulové počty.")
        elif available_groups_for_plot: # Ak sú skupiny dostupné, ale používateľ nič nevybral
             st.info("Vyberte aspoň jednu skupinu diagnóz pre zobrazenie grafu.")
        # else: (ak nie sú dostupné žiadne skupiny na výber, nič sa nezobrazí)

    else:
        st.info("Nie sú dostupné dáta pre agregovaný prehľad vývoja počtu diagnóz podľa skupín (ani pre tabuľku).")

    
