from shiny import App, ui, render
import pandas as pd
from process.data_processing import load_data, normalize_data, clean_data
from process.hwe_tests import test_hwe

# Načítanie a čistenie dát
df_raw = load_data("data/SSBU25_data.csv")
df_normalized = normalize_data(df_raw)
df_clean = clean_data(df_normalized, False)

# Načítanie genotypových stĺpcov pre test Hardy-Weinbergovej rovnováhy
genes = ['hfe_c187g_(h63d)', 'hfe_a193t_(s65c)', 'hfe_g845a_(c282y)']

# Výsledky testu HWE pre každý genotyp
hwe_results = {}
for gene in genes:
    p_value = test_hwe(df_clean[gene], verbose=False)
    hwe_results[gene] = p_value

# Definícia používateľského rozhrania s pridaným externým CSS
app_ui = ui.page_fluid(
    ui.tags.link(rel="stylesheet", href="static/styles.css"),
    ui.h2("Prehľad pacientov a výsledky Hardy-Weinbergovej rovnováhy"),
    ui.output_table("tabulka_pacientov"),
    ui.h3("Výsledky HWE testov:"),
    ui.output_table("hwe_results_table")
)

# Serverová logika
def server(input, output, session):
    @output
    @render.table
    def tabulka_pacientov():
        return df_clean

    @output
    @render.table
    def hwe_results_table():
        # Príprava dát na zobrazenie v tabuľke
        hwe_df = pd.DataFrame(list(hwe_results.items()), columns=["Genotyp", "p-hodnota"])
        return hwe_df


# Spustenie aplikácie
app = App(app_ui, server)
