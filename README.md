# Registr chovu králíků

Profesionální desktopová aplikace pro evidenci králíků, správu rodokmenů a automatické generování chovatelských dokumentů s využitím SQL databáze a AI technologií.

---

## Hlavní funkce

### 1. Profesionální SQL evidence
* **Robustní úložiště:** Přechod na SQLite databázi zajišťuje integritu dat a bleskové vyhledávání i při velkém množství záznamů.
* **Karta králíka:** Detailní správa údajů (tetování L/P, jméno, pohlaví, plemeno, barva, hmotnost, chovatel a adresa).
* **Uživatelský komfort:** Rychlé vyplňování políček pomocí klávesy **Enter** a automatické skenování údajů z fotek.
* **Správa vrhů:** Evidence počtu narozených, odchovaných a registrovaných mláďat.

### 2. AI Most & OCR Motor
* **AI Most:** Možnost importovat kompletní rodokmen (všech 14 předků) jedním kliknutím pomocí JSON kódu z AI chatbota.
* **Lokální OCR:** Integrované skenování tištěných tabulek na zadní straně rodokmenů pro automatické rozpoznání tetování předků.
* **Integrovaný Prompt:** Aplikace obsahuje nápovědu s připraveným příkazem pro AI, který stačí zkopírovat.

### 3. Inteligentní rodokmeny
* **Vizuální výběr:** Výběr rodičů probíhá interaktivně ze seznamu králíků v databázi (namísto ručního vypisování ID), s automatickým filtrem podle pohlaví.
* **Automatické generace:** Program automaticky dohledává plemena, data vrhu a chovatele všech předků až do **3. generace** (14 předků).
* **Vazby:** Každý králík v databázi je pevně propojen se svými předky pomocí SQL relací.

### 4. Tisk a export (MS Word)
Aplikace využívá chytrou šablonu `rodokmen.docx` pro generování:
**Rodokmen:** Kompletně vyplněná tabulka se 14 předky a údaji o zvířeti.
**Připouštěcí potvrzení:** Zadní strana dokumentu s automatickým určením majitele samce/samice, datem krytí a statistikami vrhu.
* **Kompletní dokument:** Spojení obou funkcí do jednoho dokumentu na jedno kliknutí.

---

## Technické informace

### Požadavky
* **Python 3.11+**
* Knihovny: `python-docx` (Word), `pytesseract` (OCR), `opencv-python` (zpracování obrazu), `sqlite3` (databáze).

### Struktura souborů
* `main.py`: Hlavní okno aplikace a logika uživatelského rozhraní.
* `database.py`: SQL motor aplikace, správa tabulek a hierarchických vazeb.
* `ocr_processor.py`: Logika pro rozpoznávání textu a tetování z fotografií.
* `chov_kraliku.db`: Hlavní SQL databázový soubor se všemi uloženými záznamy.
* `rodokmen.docx`: Šablona pro generování výstupů se značkami (např. `{{levo}}`, `{{otec_pl}}`, `{{v_nar}}` atd.).

---

## Nápověda pro zápis
* **Pohlaví:** Používáme formát `1,0` pro samce a `0,1` pro samici.
* **Tetování:** Levé ucho (L. u.) značí organizaci a měsíc, pravé ucho (P. u.) značí rok a pořadové číslo.
* **AI Import:** Pro bezchybný přenos dat používejte vestavěný **Super-Prompt** dostupný pod ikonou v aplikaci.

---

## Zálohování
Všechna data jsou uložena v databázovém souboru `chov_kraliku.db`. Pro maximální bezpečnost doporučujeme tento soubor pravidelně zálohovat na externí disk nebo cloudové úložiště.
