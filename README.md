# Registr chovu králíků


Profesionální desktopová aplikace pro evidenci králíků, správu rodokmenů a automatické generování chovatelských dokumentů ve formátu MS Word.

---

## Hlavní funkce

### 1. Komplexní evidence
* **Karta králíka:** Detailní správa údajů (tetování L/P, plemeno, barva, hmotnost, ocenění).
* **Uživatelský komfort:** Rychlé vyplňování políček pomocí klávesy **Enter** a inteligentní nápovědy přímo v editoru.
* **Správa vrhů:** Evidence počtu narozených, odchovaných a registrovaných mláďat.

### 2. Inteligentní rodokmeny
* **Automatické generace:** Program automaticky dohledává předky až do **3. generace**.
* **Vyhledávání:** Vyhledávání předků v databázi ignoruje mezery a rozdíly v malých/velkých písmenech v tetování.
* **Vazby:** Každý králík v databázi může figurovat jako potomek i jako předek jiného králíka.

### 3. Tisk a export (MS Word)
Aplikace využívá šablonu `rodokmen.docx` pro generování tří typů dokumentů:
* **Rodokmen:** Kompletně vyplněná přední strana s údaji o zvířeti a jeho předcích.
* **Připouštěcí potvrzení:** Zadní strana dokumentu s automatickým určením majitele samce/samice a datem krytí.
* **Kompletní dokument:** Spojení obou funkcí do jednoho souboru na jedno kliknutí.

### 4. Inteligentní párování
* Při generování potvrzení aplikace nabízí **automatický výběr partnera** opačného pohlaví ze seznamu, čímž eliminuje potřebu ručního vypisování tetování.

---

## Technické informace

### Požadavky
* **Python 3.11+**
* Knihovny: `python-docx` (pro práci s MS Word)

### Struktura souborů
* `main.py`: Hlavní okno aplikace a logika uživatelského rozhraní.
* `evidence.py`: Správa databáze a ukládání do JSON.
* `kralik.py`: Definice datové třídy králíka.
* `chov_data.json`: Databázový soubor se všemi uloženými záznamy.
* `rodokmen.docx`: Šablona pro generování výstupů (musí obsahovat značky jako `{{jmeno}}`, `{{otec_l}}` atd.).

---

## Nápověda pro zápis
* **Pohlaví:** Používáme formát `1,0` pro samce a `0,1` pro samici.
* **Tetování:** Levé ucho (L. u.) značí organizaci a měsíc, pravé ucho (P. u.) značí rok a pořadové číslo zvířete.
* **Datum:** Doporučený formát pro tisk je textový (např. *16. ledna 2026*).

---

## Zálohování
Všechna data jsou uložena lokálně v souboru `chov_data.json`. Pro bezpečnost se tento soubor může pravidelně zálohovat na externí disk nebo cloudové úložiště.



