from process.data_processing import load_data, normalize_data, clean_data

# Načítanie a čistenie dát
df_raw = load_data("data/SSBU25_data.csv")
df_normalized = normalize_data(df_raw)
df_clean = clean_data(df_normalized, False)
