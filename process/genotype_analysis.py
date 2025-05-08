import pandas as pd


def genotype_distribution(df: pd.DataFrame):
    """
    Vypočíta percentuálne zastúpenie jednotlivých genotypov a počet prenášačov
    a pacientov s genetickou predispozíciou na hereditárnu hemochromatózu pre každú mutáciu.
    """
    genotypes = ['normal', 'heterozygot', 'mutant']
    mutations = ['hfe_c187g_(h63d)', 'hfe_a193t_(s65c)', 'hfe_g845a_(c282y)']

    for mutation in mutations:
        # Zistenie percentuálneho zastúpenia genotypov
        genotype_percentages = [f"{genotype}: {(df[mutation] == genotype).sum() / len(df) * 100:.2f}%" for genotype in genotypes]

        # Výpis do jedného riadku
        print(f"Mutácia({mutation}) -> Genotypy: {', '.join(genotype_percentages)}")
