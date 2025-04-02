Identifikácia definícií v textoch
Aplikácia na identifikáciu definícií v slovenských textoch pomocou dvoch rôznych metód: regulárnych výrazov (RegEx) a part-of-speech tagging (POST). Tento projekt umožňuje nájsť a extrahovať definície z manuálne vložených viet v textovom poli, ako aj porovnať efektivitu oboch metód na databáze 2000 zmiešaných textov a 500 medicínskych textov.

Funkcionalita
Aplikácia ponúka grafické rozhranie s nasledujúcimi možnosťami:

1. RegEx identifikácia - Hľadanie definícií pomocou regulárnych výrazov
2. POST identifikácia - Hľadanie definícií pomocou part-of-speech tagging
3. Porovnanie metód - Analýza účinnosti oboch metód na medicínskych a zmiešaných textoch

Podporované vzory definícií
Aplikácia dokáže rozpoznať nasledujúce typy definičných fráz v slovenskom jazyku:
RegEx vzory:
Priama definícia: "X je Y"
Definičná konštrukcia: "Definícia X je Y"
Definovanie: "X je definovaný ako Y"
Reflexívna konštrukcia: "X sa definuje ako Y"
Porozumenie definície: "Definovaním X rozumieme Y"
Slovesná konštrukcia: "X znamená Y"
Výrazová konštrukcia: "Výraz X znamená Y"

POST vzory:
Priama definícia: "X je Y"
Definičná konštrukcia: "Definícia X je Y"
Definovanie: "X je definovaný ako Y"
Reflexívna konštrukcia: "X sa definuje ako Y"
Porozumenie definície: "Definovaním X rozumieme Y"
Slovesná konštrukcia: "X znamená Y"
Výrazová konštrukcia: "Výraz X znamená Y"

Inštalácia
Požiadavky:
-Python 3.6 alebo novší
-pip

Postup inštalácie:

1. Naklonujte repozitár
   git clone https://github.com/jozefbobot/uni-bachelor-thesis-identification-of-definitions.git
   cd uni-bachelor-thesis-identification-of-definitions
2. Spustite inštalačný skript
   python src/setup.py
3. Po úspešnej inštalácii je potrebné aktivovať virtuálne prostredie
   Windows: venv\Scripts\activate
   Linux/macOS: source venv/bin/activate

Použitie
Po aktivácii virtuálneho prostredia spustite aplikáciu príkazom:
python main.py
