# sem_bio
semestralna praca predmetu Softverove spracovanie biomedicinskych udajov

**8.5.**
- uprava datasetu v exceli
- vymazanie prazdnych stlpcov
- zmena nazvov atributov - namiesto medzery '_'
- prekonvertovanie na .csv format kvoli nacitaniu v python
- vytvorenie git repozitaru

- (ULOHA 1) - nacitanie, spracovanie datasetu a odstranenie neuplnych riadkov
- (ULOHA 2) - vykonanie hwe testov pre kazdu mutaciu - vysledna p-hodnota (pri poslednej mutacii C282Y nie su genotypy v rovnovahe)
- (ULOHA 3) - percentualne zastupenie genotypov pre kazdu mutaciu

**9.5.**
- priprava GUI pre efektivne zobrazenie informacii z datasetu
- kniznica streamlit


- podstranka - **zoznam pacientov**
- -> zobrazenie udajov o pacientoch a filter

**10.5.**
- podstranka - **hwe testy**
- -> percentulane rozdelenie genotypov
- -> vyhodnotenie ci su genotypy v Hardy-Weinbergovej rovnováhe


- podstranka - **prenasaci a predispozicia**
- -> zoznam pacientov s pridanym atributom 'geneticky_status' (bez_rizika, prenasac, predispouicia)
- -> pocet prenasacov a pocet s genetickou predispoziciou


- podstranka - **diagnozy**
- -> skumanie suvislosti medzi genetickym rizikom a diagnozami pacientov (Cukrovka, Benigne nadory, Poruchy krvneho systemu)
- -> vypocet podielu
- -> vykreslenie grafu
