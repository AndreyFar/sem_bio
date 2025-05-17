from scipy.stats import chisquare


def test_hwe(genotype_series, verbose=True):
    """
    Testuje Hardy-Weinbergovu rovnováhu pre daný genotypový stĺpec.
    """
    # Spočítanie počtu každého genotypu
    counts = genotype_series.value_counts()
    n_normal = counts.get("normal", 0)
    n_hetero = counts.get("heterozygot", 0)
    n_mutant = counts.get("mutant", 0)

    total = n_normal + n_hetero + n_mutant
    if total == 0:
        if verbose:
            print("Žiadne dostupné genotypy.")
        return None

    # Výpočet frekvencií alel
    p = (2 * n_normal + n_hetero) / (2 * total)
    q = 1 - p

    # Očakávané počty genotypov podľa HWE
    expected_normal = p ** 2 * total
    expected_hetero = 2 * p * q * total
    expected_mutant = q ** 2 * total

    expected = [expected_normal, expected_hetero, expected_mutant]
    observed = [n_normal, n_hetero, n_mutant]

    # Chi-square test
    chi2_stat, p_value = chisquare(f_obs=observed, f_exp=expected)

    if verbose:
        print(f"HWE test pre genotypy:")
        print(f" - Pozorované: {observed}")
        print(f" - Očakávané:  {[round(e, 2) for e in expected]}")
        print(f" - χ² = {round(chi2_stat, 3)}, p-hodnota = {round(p_value, 4)}")
        if p_value < 0.05:
            print("Odmietame H0: NIE je v HWE.")
        else:
            print("Neodmietame H0: Dáta sú v HWE.")

    return p_value
