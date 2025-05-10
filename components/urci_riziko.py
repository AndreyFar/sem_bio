def urci_riziko(row):
    genotypy = [
        row["hfe_c187g_(h63d)"],
        row["hfe_a193t_(s65c)"],
        row["hfe_g845a_(c282y)"]
    ]
    pocet_hetero = genotypy.count("heterozygot")
    pocet_mutant = genotypy.count("mutant")

    if pocet_mutant >= 1 or pocet_hetero >= 2:
        return "predispozícia"
    elif pocet_hetero == 1:
        return "prenášač"
    else:
        return "bez rizika"
