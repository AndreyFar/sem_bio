DG_SKUPINY = {
    "Infekcie (kap. I)": ("A00", "B99"),
    "Nádory (kap. II)": ("C00", "D48"),
    "Krvné choroby a imunitné poruchy (kap. III)": ("D50", "D89"),
    "Metabolizmus, žľazy (kap. IV)": ("E00", "E90"),
    "Psychické poruchy (kap. V)": ("F00", "F99"),
    "Nervový systém (kap. VI)": ("G00", "G99"),
    "Oči (kap. VII)": ("H00", "H59"),
    "Uši (kap. VIII)": ("H60", "H95"),
    "Srdce a obehová sústava (kap. IX)": ("I00", "I99"),
    "Dýchacia sústava (kap. X)": ("J00", "J99"),
    "Tráviaca sústava (kap. XI)": ("K00", "K93"),
    "Koža a podkožie (kap. XII)": ("L00", "L99"),
    "Svaly, kĺby, spojivové tkanivo (kap. XIII)": ("M00", "M99"),
    "Močová a pohlavná sústava (kap. XIV)": ("N00", "N99"),
    "Tehotenstvo, pôrod (kap. XV)": ("O00", "O99"),
    "Perinatálne stavy (kap. XVI)": ("P00", "P96"),
    "Vrodené chyby (kap. XVII)": ("Q00", "Q99"),
    "Príznaky a nálezy (kap. XVIII)": ("R00", "R99"),
    "Úrazy, otravy (kap. XIX)": ("S00", "T98"),
    "Vonkajšie príčiny (kap. XX)": ("V01", "Y98"),
    "Sociálne faktory (kap. XXI)": ("Z00", "Z99")
}


def kod_prefix(kod):
    if not isinstance(kod, str) or len(kod) < 3:
        return None
    return kod[:3]


def patri_do_skupiny(kod, rozsah):
    prefix = kod_prefix(kod)
    if not prefix:
        return False
    od, do = rozsah
    return od <= prefix <= do
