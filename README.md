# sem_bio
Semestrálna práca predmetu Softvérové spracovanie biomedicínskych údajov

# Prototyp interaktívnej analýzy genetických a klinických údajov pre hereditárnu hemochromatózu (HH)

Tento prototyp je webová aplikácia vytvorená pomocou knižnice **Streamlit**, ktorá umožňuje intuitívnu analýzu genetických a klinických údajov pacientov so zameraním na **hereditárnu hemochromatózu (HH)**. Cieľom aplikácie je podporiť lekárov a výskumníkov pri identifikácii geneticky rizikových pacientov a porozumení vzťahov medzi mutáciami a diagnózami.

Aplikácia umožňuje:

- Spracovanie dát vrátane čistenia, validácie a typovania stĺpcov.
- Filtrovanie pacientov podľa genetických mutácií (H63D, S65C, C282Y) a klinických diagnóz (MKCH-10).
- Vizualizáciu podielu genetického rizika v rôznych skupinách diagnóz.
- Štatistickú analýzu genotypov (Hardy-Weinbergov test rovnováhy).
- Vytváranie prehľadných grafov a interaktívnych tabuliek.

---

## Spustenie aplikácie

1. V termináli zadajte nasledujúci príkaz pre spustenie aplikácie:

```bash
streamlit run app.py --server.port 8502
