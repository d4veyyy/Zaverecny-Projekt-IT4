Webová aplikace – Správa skladu

Popis projektu

Tato webová aplikace je určena pro správu skladových zásob a umožňuje správu produktů ve skladu, jako je přidávání nových položek, aktualizace stavu zásob, jejich mazání a sledování historie pohybů. Aplikace je postavena pomocí Django na backendu, který generuje HTML šablony pro frontend, což umožňuje plnou integraci serverové logiky s uživatelským rozhraním.

Funkcionalita:

 Přidávání, aktualizace a mazání produktů ve skladu.

 Zobrazení aktuálního stavu zásob.

 Možnost filtrování a vyhledávání produktů.
 
 Sledování historie skladových operací (příjem/výdej).
 
 Upozornění na nízké zásoby.
 
 Uživatelské rozhraní pro přihlášení a správu uživatelů.
 
 Použité technologie

Frontend:

HTML: Struktura webu.
CSS: Stylování uživatelského rozhraní.
JavaScript: Interaktivita stránek, dynamické funkce na straně klienta.

Backend:

Python: Hlavní jazyk backendu.
Django: Webový framework pro správu serverových operací, šablon a datové logiky.
SQLite (výchozí databáze Django): Používána pro ukládání dat skladových položek a uživatelských účtů.

Další technologie:
Django Templating Engine: Generování HTML šablon s dynamickými daty.
Bootstrap (nepovinně): Pro moderní responzivní design a lepší UX/UI.
Struktura projektu
plaintext

root
   ├── sklad               # Hlavní aplikace pro správu skladu                                                                                                                                                                   
  │   ├── templates       # HTML šablony
  │   │   └── sklad       # Šablony pro různé stránky (index, detail, formuláře, atd.)
  │   ├── static          # CSS, JavaScript a obrázky
  │   ├── views.py        # Logika pro jednotlivé stránky a operace
  │   ├── models.py       # Datové modely pro skladové položky
  │   ├── urls.py         # Definice URL tras
  │   └── forms.py        # Formuláře pro přidávání/úpravu produktů
   ├── db.sqlite3          # Databáze SQLite (pro skladová data)
  └── manage.py           # Hlavní soubor pro správu aplikace Django

Funkce
 
 Přidávání produktů: Administrátoři mohou přidávat nové produkty s detaily jako název, popis, cena a množství na skladě.
 Aktualizace a mazání: Možnost editovat informace o produktu nebo jej odstranit.
 Seznam produktů: Přehled všech dostupných produktů na skladě s možností filtrování a vyhledávání.
 Detail produktu: Zobrazení podrobností o konkrétní položce ve skladu.
 Sledování zásob: Automatická upozornění, pokud některé položky klesnou pod stanovený limit.
 Uživatelská autentizace: Přihlášení, registrace a správa uživatelských rolí (administrátor, skladník).
