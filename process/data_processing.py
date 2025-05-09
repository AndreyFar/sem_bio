import pandas as pd


def load_data(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path, delimiter=';')
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    return df


def normalize_data(df: pd.DataFrame) -> pd.DataFrame:
    # Spracovanie dátumov
    df['validovany_vysledok'] = pd.to_datetime(df['validovany_vysledok'], format='%d.%m.%Y', errors='coerce')
    df['prijem_vzorky'] = pd.to_datetime(df['prijem_vzorky'], format='%d.%m.%Y', errors='coerce')

    # Spracovanie časov
    df['vysledok_cas'] = pd.to_datetime(df['vysledok_cas'], format='%H:%M', errors='coerce').dt.time
    df['prijem_cas'] = pd.to_datetime(df['prijem_cas'], format='%H:%M', errors='coerce').dt.time

    # Prevod veku
    df['vek'] = df['vek'].astype(str).str.replace(',', '.').astype(float)

    # Normalizácia pohlavia
    df['pohlavie'] = df['pohlavie'].str.strip().str.upper().replace({
        'M': 'M', 'MUŽ': 'M', 'MALE': 'M',
        'F': 'F', 'Ž': 'F', 'FEMALE': 'F'
    })

    # Normalizácia genotypov
    genotype_cols = [
        'hfe_c187g_(h63d)',
        'hfe_a193t_(s65c)',
        'hfe_g845a_(c282y)'
    ]
    genotype_mapping = {
        'normal': 'normal',
        'heterozygot': 'heterozygot',
        'mutant': 'mutant',
        'heterozygote': 'heterozygot',
        'homozygote': 'mutant',
        'wt': 'normal',
        '': pd.NA,
        '-': pd.NA,
        'nan': pd.NA
    }
    for col in genotype_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.lower().replace(genotype_mapping)

    return df


def clean_data(df: pd.DataFrame, verbose: bool = True) -> pd.DataFrame:
    """
    Odstráni všetky riadky, ktoré obsahujú aspoň jednu chýbajúcu hodnotu.
    Voliteľne zobrazí počet odstránených riadkov a detailne uvedie, ktoré stĺpce chýbali.
    """

    missing_rows = df[df.isnull().any(axis=1)]
    removed_count = len(missing_rows)
    cleaned_df = df.dropna()

    if verbose:
        print(f"Počet riadkov v datasete: {len(df)}")
        print(f"Odstránených riadkov s chýbajúcimi hodnotami: {removed_count}")
        print(f"Počet riadkov po čistení: {len(cleaned_df)}")

        if removed_count > 0:
            print("\nDetail chýbajúcich údajov v odstránených riadkoch:")
            for idx, row in missing_rows.iterrows():
                missing_cols = row[row.isnull()].index.tolist()
                print(f" - Riadok index {idx} (id={row.get('id', 'neznáme')}): chýba v {missing_cols}")

    return cleaned_df
