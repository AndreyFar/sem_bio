import streamlit as st


def show():
    st.title("Vitaj v HH Centre")

    st.write("""
    **Sme centrum, ktoré sa zameriava na genetické testovanie hereditárnej hemochromatózy (HH).**
    
    Toto ochorenie spôsobuje, že telo vstrebáva príliš veľa železa – ako keby si mal silný magnet na železo v bruchu!
    
    Časom sa nadbytočné železo môže ukladať v orgánoch (napr. v pečeni či srdci) a spôsobiť vážne zdravotné problémy. Našťastie, ak o tom vieš včas, dá sa s tým veľa spraviť!
    """)

    st.markdown("---")

    st.subheader("O čo nám ide?")
    st.write("""
    Pomocou genetických testov zisťujeme, či máš v DNA „malé zmeny“ (mutácie), ktoré môžu súvisieť s týmto ochorením.
    Sledujeme najmä tri mutácie v géne **HFE**:
    
    - 🧬 **H63D**
    - 🧬 **S65C**
    - 🧬 **C282Y**

    Všetky tieto „kódy“ môžu niečo naznačiť o tvojej výbave na vstrebávanie železa.
    """)

    st.subheader("A čo sa z toho dozvieš?")
    st.write("""
    Podľa výsledkov testov ti vieme povedať, či si:
    
    - 🟢 **Bez rizika** – všetko vyzerá normálne.
    - 🟠 **Prenášač** – máš jednu z mutácií, ale ešte to nemusí nič znamenať.
    - 🔴 **S predispozíciou** – tvoje gény naznačujú vyššie riziko, že sa HH môže rozvinúť.

    """)

    st.markdown("---")
    st.info("Klikni na niektorú možnosť v menu vľavo a preskúmaj, čo všetko o HH vieme z tvojich genetických údajov.")
