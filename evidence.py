import os
import json
from kralik import Kralik


class Registr:
    def __init__(self, soubor="chov_data.json"):
        self.soubor = soubor
        self.seznam_kraliku = {}
        self.nacti_data()

    def pridat_kralika(self, kralik):
        if kralik.id not in self.seznam_kraliku:
            self.seznam_kraliku[kralik.id] = kralik
            self.uloz_data()
            return True
        return False
    """
    def najdi_podle_tetovani(self, tetovani):
        return self.seznam_kraliku.get(tetovani)
    """
        
    def uloz_data(self):
        data_k_ulozeni = {k_id: k.to_dict() for k_id, k in self.seznam_kraliku.items()}
        with open(self.soubor, "w", encoding="utf-8") as f:
            json.dump(data_k_ulozeni, f, ensure_ascii=False, indent=4)

    def nacti_data(self):
        if not os.path.exists(self.soubor):
            return
        try:
            with open(self.soubor, "r", encoding="utf-8") as f:
                data = json.load(f)
                for k_id, d in data.items():
                    novy = Kralik(d['levo'], d['pravo'], d['jmeno'], d['pohlavi'], d['otec_id'], d['matka_id'])
                    self.seznam_kraliku[k_id] = novy
        except Exception as e:
            print(f"Chyba při načítání dat: {e}")