import pandas as pd
import streamlit as st


def show_patient_table(df, styled=False):
    st.subheader(f"Zobrazených pacientov: {len(df)}")
    df = df.head(150).copy()

    if 'vek' in df.columns:
        df['vek'] = df['vek'].round(2)

    for col in ['validovany_vysledok', 'prijem_vzorky']:
        if col in df.columns:
            df[col] = df[col].dt.strftime('%d.%m.%Y')

    for col in ['vysledok_cas', 'prijem_cas']:
        if col in df.columns and df[col].dtype == 'object':
            df[col] = df[col].apply(lambda x: x.strftime('%H:%M') if pd.notnull(x) else "")

    if df.empty:
        st.warning("Žiadni pacienti nespĺňajú aktuálne filtre.")
    else:
        if styled and "geneticky_status" in df.columns:
            styled_df = styluj_geneticky_status(df)
            styled_df = styled_df.format({'vek': '{:.2f}'})
            st.write(styled_df)
        else:
            st.dataframe(df.style.format({'vek': '{:.2f}'}), use_container_width=True)


def styluj_geneticky_status(df):
    def farba_status(val):
        if val == "bez rizika":
            color = "green"
        elif val == "prenášač":
            color = "orange"
        elif val == "predispozícia":
            color = "red"
        else:
            color = "black"
        return f"color: {color}; font-weight: bold"

    return df.style.applymap(farba_status, subset=["geneticky_status"])
