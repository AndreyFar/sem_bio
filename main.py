from process.data_processing import load_data, normalize_data, clean_data, check_diagnose_code

# Načítanie a čistenie dát
df_raw = load_data("data/SSBU25_data.csv")
print(f"Počet riadkov v surovom datasete: {len(df_raw)}")

df_clean = clean_data(df_raw, True)
df_normalized = normalize_data(df_clean)

df_valid = check_diagnose_code(df_normalized, True)
print(f"Počet riadkov v spracovanom datasete: {len(df_valid)}")
