import streamlit as st

def show_patient_table(df):
    st.subheader(f"Zobrazených pacientov: {len(df)}")
    if df.empty:
        st.warning("Žiadni pacienti nespĺňajú aktuálne filtre.")
    else:
        st.dataframe(df, use_container_width=True)
