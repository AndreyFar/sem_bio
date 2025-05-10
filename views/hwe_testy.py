import streamlit as st
from process.hwe_tests import test_hwe


def show(df):
    st.title("HWE Testy a rozdelenie genotypov")

    # Definované mutácie a genotypy
    mutations = ['hfe_c187g_(h63d)', 'hfe_a193t_(s65c)', 'hfe_g845a_(c282y)']
    genotypes = ['normal', 'heterozygot', 'mutant']

    # Zobrazenie výsledkov pre každú mutáciu
    for mutation in mutations:
        st.subheader(f"Mutácia: `{mutation.upper()}`")

        # Percentuálne zastúpenie genotypov
        counts = df[mutation].value_counts()
        total = counts.sum()
        percentages = {g: (counts.get(g, 0) / total * 100) for g in genotypes}

        cols = st.columns(len(genotypes))
        for i, g in enumerate(genotypes):
            cols[i].metric(g.capitalize(), f"{counts.get(g, 0)} ({percentages[g]:.2f}%)")

        # Výsledok HWE testu
        p_value = test_hwe(df[mutation], verbose=False)
        if p_value is not None:
            st.markdown(f"**p-hodnota HWE testu:** `{p_value:.4f}`")
            if p_value < 0.05:
                st.error("❌ Odmietame H₀: Dáta nie sú v Hardy-Weinbergovej rovnováhe.")
            else:
                st.success("✅ Neodmietame H₀: Dáta sú v Hardy-Weinbergovej rovnováhe.")
        else:
            st.warning("Nebolo možné vypočítať HWE test – žiadne alebo neúplné dáta.")

        st.divider()
