import json
import os
from database import Database

def vycisti_cislo(hodnota, typ=float):
    """Převede text na číslo (float nebo int)."""
    if not hodnota:
        return 0.0 if typ == float else 0
    try:
        text = str(hodnota).replace(',', '.').strip()
        return typ(text)
    except ValueError:
        return 0.0 if typ == float else 0

def spust_migraci():
    json_soubor = "chov_data.json"
    if not os.path.exists(json_soubor):
        print(f"Soubor {json_soubor} nebyl nalezen.")
        return

    db = Database()
    with open(json_soubor, "r", encoding="utf-8") as f:
        stara_data = json.load(f)

    print(f"Zahajuji migraci {len(stara_data)} králíků...")

    for klic_tetovani, info in stara_data.items():
        usi = klic_tetovani.split('/')
        l_ucho = usi[0].strip() if len(usi) > 0 else ""
        p_ucho = usi[1].strip() if len(usi) > 1 else ""

        # Kompletní balík dat se všemi klíči, které database.py vyžaduje
        kralik_pro_sql = {
            "levo": l_ucho,
            "pravo": p_ucho,
            "jmeno": info.get("jmeno", ""), # Pokud v JSON není, dáme prázdné
            "pohlavi": info.get("pohlavi", ""),
            "plemeno": info.get("plemeno", ""),
            "barva": info.get("barva", ""),
            "datum_narozeni": info.get("narozeni", info.get("datum_vrhu", "")),
            "hmotnost": vycisti_cislo(info.get("hmotnost"), float),
            "chovatel": info.get("chovatel", ""),
            "adresa": info.get("adresa", ""),
            "naroz_ks": vycisti_cislo(info.get("naroz_ks"), int),
            "odchov_ks": vycisti_cislo(info.get("odchov_ks"), int),
            "registr_ks": vycisti_cislo(info.get("registr_ks"), int)
        }

        db.uloz_kralika(kralik_pro_sql)
        print(f"Králík {klic_tetovani} převeden.")

    print("\nMigrace hotova!")

if __name__ == "__main__":
    spust_migraci()