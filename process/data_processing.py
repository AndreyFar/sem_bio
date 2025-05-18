import pandas as pd
import re


def load_data(file_path: str) -> pd.DataFrame:
    """
    Načítanie údajov z CSV súboru
    """
    df = pd.read_csv(file_path, delimiter=';', dtype={'id': str})
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    return df


def clean_data(df: pd.DataFrame, verbose=False) -> pd.DataFrame:
    """
    Odstráni všetky riadky, ktoré obsahujú aspoň jednu chýbajúcu hodnotu.
    Voliteľne zobrazí počet odstránených riadkov a detailne uvedie, ktoré stĺpce chýbali.
    """
    missing_rows = df[df.isnull().any(axis=1)]
    removed_count = len(missing_rows)
    cleaned_df = df.dropna()

    if verbose:
        if removed_count > 0:
            print("\nDetail chýbajúcich údajov v odstránených riadkoch:")
            for idx, row in missing_rows.iterrows():
                missing_cols = row[row.isnull()].index.tolist()
                print(f" - Riadok index {idx} (id={row.get('id', 'neznáme')}): nan v {missing_cols}")

    return cleaned_df


def normalize_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transformácia údajov do jednotného formátu
    """
    df = df.copy()
    # ID na int
    df['id'] = df['id'].astype(str)

    # Spracovanie dátumov
    df['validovany_vysledok'] = pd.to_datetime(df['validovany_vysledok'], format='%d.%m.%Y', errors='coerce')
    df['prijem_vzorky'] = pd.to_datetime(df['prijem_vzorky'], format='%d.%m.%Y', errors='coerce')

    # Spracovanie časov
    df['vysledok_cas'] = pd.to_datetime(df['vysledok_cas'], format='%H:%M', errors='coerce').dt.time
    df['prijem_cas'] = pd.to_datetime(df['prijem_cas'], format='%H:%M', errors='coerce').dt.time

    # Vek na float s dvomi desatinnými miestami
    df['vek'] = df['vek'].astype(str).str.replace(',', '.').astype(float).round(2)

    # Pohlavie na veľké písmená, odstránenie medzier
    df['pohlavie'] = df['pohlavie'].astype(str).str.strip().str.upper()

    # Mutácie na malé písmená, odstránenie medzier
    for col in ['hfe_c187g_(h63d)', 'hfe_a193t_(s65c)', 'hfe_g845a_(c282y)']:
        df[col] = df[col].astype(str).str.strip().str.lower()

    # Diagnóza ako reťazec
    df['diagnoza_mkch-10'] = df['diagnoza_mkch-10'].astype(str).str.strip()

    return df


def check_diagnose_code(df: pd.DataFrame, verbose=False) -> pd.DataFrame:
    """
    Odstráni riadky s nevalidným kódom diagnózy podľa formátu MKCH-10:
    - veľké písmeno
    - 2 číslice
    - voliteľná desatinná časť: bodka + max 2 číslice
    """

    def je_validny_kod(kod: str) -> bool:
        if not isinstance(kod, str):
            return False
        return bool(re.fullmatch(r"[A-Z][0-9]{2}(\.[0-9]{1,2})?", kod))

    maska = df["diagnoza_mkch-10"].apply(je_validny_kod)

    if verbose:
        nevalidne = df[~maska]
        for idx, row in nevalidne.iterrows():
            print(f"Nevalidný kód na indexe {idx} – id: {row['id']}, kód: {row['diagnoza_mkch-10']}")

    return df[maska].reset_index(drop=True)
