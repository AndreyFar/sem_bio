import streamlit as st
import matplotlib.pyplot as plt
from components.urci_riziko import urci_riziko

DG_SKUPINY = {
    "Pečeň": [
        "K70.1", "K70.3", "K70.9", "K71.0", "K71.2", "K71.9", "K72.0", "K73.0", "K73.1",
        "K73.2", "K73.9", "K74", "K74.0", "K74.1", "K74.2", "K74.3", "K74.4", "K74.5",
        "K74.6", "K75.0", "K75.2", "K75.8", "K75.9", "K76.0", "K76.1", "K76.3", "K76.7",
        "K76.8", "K76.9", "K77.0", "K77.8"
    ],
    "Cukrovka": [
        "E10.1", "E10.8", "E10.9", "E11.8", "E11.9", "E11.91", "E53.9", "E72.1", "E78.9",
        "E80.1", "E83.0", "E83.1", "E83.8", "E83.9", "E87.8"
    ],
    "Srdce": [
        "I50.0", "I50.00", "I50.9", "I25.8", "I25.9", "I26.9", "I48.9", "I49.9", "I20.9",
        "I21.0", "I21.4", "I10", "I10.00", "I10.01"
    ],
    "Pankreas": [
        "K86.1", "K86.9", "K87.1", "K90.0", "K92.0", "K92.1", "K92.2", "K92.8", "K92.9"
    ],
    "Pľúca": [
        "J18.9", "J63.4"
    ],
    "Kĺby": [
        "M54.13"
    ],
    "Poruchy lipidového metabolizmu": [
        "E78.9"
    ],
    "Infekcie": [
        "A08.4", "A09", "A09.9", "A41.8", "A69.2", "B15.9", "B16.9", "B17.9", "B18.1",
        "B18.2", "B18.9", "B19.9", "B27.8", "B97.8", "B99"
    ],
    "Onkologické ochorenia": [
        "C02.1", "C22.0", "C22.9", "C80.9"
    ],
    "Benígne nádory": [
        "D06", "D33.0", "D37.6", "D46.0", "D46.7", "D50.0", "D50.8", "D50.9", "D51.8",
        "D52.9", "D53.1", "D59.1", "D63.8", "D64.8", "D64.9", "D68.30", "D68.6", "D68.8",
        "D68.9", "D69.0", "D69.3", "D69.5", "D69.59", "D75.0", "D75.1", "D75.2", "D75.8",
        "D75.9"
    ],
    "Poruchy krvného systému": [
        "D75.0", "D75.1", "D75.2", "D75.8", "D75.9"
    ],
    "Nezaradené": [
        "G00.9", "G40.9", "G92", "G95.1", "H18.2", "I05.9", "I10", "I10.00", "I10.01",
        "I20.9", "I21.0", "I21.4", "I25.8", "I25.9", "I26.9", "I48.9", "I49.9", "I50.0",
        "I50.00", "I50.9", "I80.2", "I80.3", "I81", "I82.8", "I85.9", "I87.00", "I88.8",
        "J18.9", "J63.4", "K10.2", "K21.0", "K29.1", "K29.6", "K29.7", "K30", "K30.",
        "K31.9", "K50.9", "K51.9", "K52.9", "K59.9", "K63.0", "K63.9", "K70.1", "K70.3",
        "K70.9", "K71.0", "K71.2", "K71.9", "K72.0", "K73.0", "K73.1", "K73.2", "K73.9",
        "K74", "K74.0", "K74.1", "K74.2", "K74.3", "K74.4", "K74.5", "K74.6", "K75.0",
        "K75.2", "K75.8", "K75.9", "K76.0", "K76.1", "K76.3", "K76.7", "K76.8", "K76.9",
        "K77.0", "K77.8", "K80.5", "K82.9", "K83.1", "K83.8", "K83.9", "K85", "K86.1",
        "K86.9", "K87.1", "K90.0", "K92.0", "K92.1", "K92.2", "K92.8", "K92.9", "L95.8",
        "M54.13", "N11.0", "N11.8", "N17.9", "N18.0", "N18.8", "N30.8", "Q44.7", "R04.9",
        "R06.0", "R07.4", "R10.4", "R16.2", "R18", "R50.0", "R50.8", "R50.9", "R55", "R59.9",
        "R60.1", "R63.0", "R72.8", "R74.0", "R74.8", "R74.9", "R79.0", "X31.4", "Z30.4",
        "Z76.8"
    ]
}


def show(df):
    st.title("Vzťah medzi genetickým rizikom a diagnózami")

    vyber = st.selectbox("Vyber oblasť diagnóz", list(DG_SKUPINY.keys()))
    dg_kody = DG_SKUPINY[vyber]

    st.markdown(f"Analyzujeme diagnózy pre oblasť **{vyber}** (kódy: {', '.join(dg_kody)}).")
    df['riziko'] = df.apply(urci_riziko, axis=1)
    df['ma_dg'] = df['diagnoza_mkch-10'].isin(dg_kody)

    grouped = df.groupby('riziko')['ma_dg'].agg(['sum', 'count'])
    grouped['podiel'] = grouped['sum'] / grouped['count'] * 100

    st.dataframe(grouped.rename(columns={
        'sum': 'Počet s diagnózou',
        'count': 'Počet v skupine',
        'podiel': 'Podiel [%]'
    }))

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.bar(grouped.index, grouped['podiel'], color=['green', 'orange', 'red'])
        ax.set_ylabel("Podiel [%]", fontsize=10)
        ax.set_xlabel("Genetické riziko", fontsize=10)
        ax.set_ylim(0, 100)
        ax.tick_params(axis='both', labelsize=8)
        ax.set_title("", fontsize=12)
        plt.tight_layout()
        st.pyplot(fig)
