import json
import os
from kralik import Kralik

class Registr:
    def __init__(self, soubor="chov_data.json"):
        self.soubor = soubor
        self.seznam_kraliku = {}
        self.nacti_data()

    def uloz_kralika(self, kralik):
        self.seznam_kraliku[kralik.id] = kralik
        self.uloz_na_disk()

    def smazat_kralika(self, kralik_id):
        if kralik_id in self.seznam_kraliku:
            del self.seznam_kraliku[kralik_id]
            self.uloz_na_disk()
            return True
        return False

    def uloz_na_disk(self):
        """Uloží aktuální stav databáze do JSON souboru."""
        data = {k_id: k.to_dict() for k_id, k in self.seznam_kraliku.items()}
        try:
            with open(self.soubor, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Chyba při ukládání: {e}")

    def nacti_data(self):
        """Načte data z JSON souboru při startu programu."""
        if os.path.exists(self.soubor):
            try:
                with open(self.soubor, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for k_id, d in data.items():
                        self.seznam_kraliku[k_id] = Kralik.from_dict(d)
            except Exception as e:
                print(f"Chyba při načítání: {e}")