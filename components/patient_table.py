import streamlit as st


def show_patient_table(df):
    st.subheader(f"Zobrazených pacientov: {len(df)}")
    if df.empty:
        st.warning("Žiadni pacienti nespĺňajú aktuálne filtre.")
    else:
        st.dataframe(df, use_container_width=True)


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
