import sqlite3

class Database:
    def __init__(self, db_name="chov_kraliku.db"):
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.vytvor_tabulky()

    def vytvor_tabulky(self):
        # Přidali jsme všechny chybějící sloupce (jmeno, adresa, počty mláďat)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS kralici (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                levo TEXT,
                pravo TEXT,
                jmeno TEXT,
                pohlavi TEXT,
                plemeno TEXT,
                barva TEXT,
                datum_narozeni TEXT,
                hmotnost REAL,
                chovatel TEXT,
                adresa TEXT,
                naroz_ks INTEGER,
                odchov_ks INTEGER,
                registr_ks INTEGER,
                otec_id INTEGER,
                matka_id INTEGER,
                UNIQUE(levo, pravo)
            )
        ''')
        self.conn.commit()

    def uloz_kralika(self, data):
        """Uloží králíka a automaticky zpracuje i jeho rodiče (pokud v datech jsou)."""
        if not data: return None

        # Sladění názvů polí z JSONu s názvy v SQL tabulce
        sql_data = {
            "levo": data.get("levo", ""),
            "pravo": data.get("pravo", ""),
            "jmeno": data.get("jmeno", ""),
            "pohlavi": data.get("pohlavi", ""),
            "plemeno": data.get("plemeno", ""),
            "barva": data.get("barva", ""),
            "datum_narozeni": data.get("datum_narozeni", data.get("narozeni", "")),
            "chovatel": data.get("chovatel", ""),
            "adresa": data.get("adresa", ""),
            "hmotnost": data.get("hmotnost", 0),
            "naroz_ks": data.get("naroz_ks", 0),
            "odchov_ks": data.get("odchov_ks", 0),
            "registr_ks": data.get("registr_ks", 0)
        }

        sql = '''INSERT INTO kralici 
                 (levo, pravo, jmeno, pohlavi, plemeno, barva, datum_narozeni, hmotnost, chovatel, adresa, naroz_ks, odchov_ks, registr_ks)
                 VALUES 
                 (:levo, :pravo, :jmeno, :pohlavi, :plemeno, :barva, :datum_narozeni, :hmotnost, :chovatel, :adresa, :naroz_ks, :odchov_ks, :registr_ks)
                 ON CONFLICT(levo, pravo) DO UPDATE SET
                 jmeno=excluded.jmeno, pohlavi=excluded.pohlavi, plemeno=excluded.plemeno, 
                 barva=excluded.barva, datum_narozeni=excluded.datum_narozeni, hmotnost=excluded.hmotnost,
                 chovatel=excluded.chovatel, adresa=excluded.adresa, naroz_ks=excluded.naroz_ks, 
                 odchov_ks=excluded.odchov_ks, registr_ks=excluded.registr_ks
                 RETURNING id'''
        
        try:
            self.cursor.execute(sql, sql_data)
            k_id = self.cursor.fetchone()[0]
            self.conn.commit()

            # Zpracování rodičů (REKURZE)
            if 'otec' in data:
                oid = self.uloz_kralika(data['otec'])
                self.cursor.execute("UPDATE kralici SET otec_id=? WHERE id=?", (oid, k_id))
            
            if 'matka' in data:
                mid = self.uloz_kralika(data['matka'])
                self.cursor.execute("UPDATE kralici SET matka_id=? WHERE id=?", (mid, k_id))
            
            self.conn.commit()
            return k_id
        except Exception as e:
            print(f"Chyba uložení: {e}")
            return None

    def ziskej_vsechny_kraliky(self):
        self.cursor.execute("SELECT * FROM kralici ORDER BY id DESC")
        return [dict(row) for row in self.cursor.fetchall()]

    def ziskej_kralika_podle_id(self, id):
        self.cursor.execute("SELECT * FROM kralici WHERE id=?", (id,))
        res = self.cursor.fetchone()
        return dict(res) if res else None

    def najdi_podle_tetovani(self, text):
        if "/" in text:
            l, p = text.split('/')
            self.cursor.execute("SELECT * FROM kralici WHERE levo=? AND pravo=?", (l.strip(), p.strip()))
        else:
            self.cursor.execute("SELECT * FROM kralici WHERE levo=? OR pravo=?", (text.strip(), text.strip()))
        res = self.cursor.fetchone()
        return dict(res) if res else None

    def nastav_rodice(self, kid, oid, mid):
        self.cursor.execute("UPDATE kralici SET otec_id=?, matka_id=? WHERE id=?", (oid, mid, kid))
        self.conn.commit()

    def importuj_kompletni_rodokmen(self, data):
        """Zpracuje JSON s hlavním králíkem a jeho předky až do 'pravěku'."""
        
        def zpracuj_individualu(info):
            """Pomocná funkce: uloží králíka a vrátí jeho SQL ID."""
            if not info: return None
            # Uložíme základní data
            k_id = self.uloz_kralika(info)
            
            # Pokud má tento králík v JSONu své vlastní rodiče, jdeme hlouběji
            otec_id = None
            matka_id = None
            
            if 'predci' in info:
                otec_id = zpracuj_individualu(info['predci'].get('otec'))
                matka_id = zpracuj_individualu(info['predci'].get('matka'))
            elif 'otec' in info or 'matka' in info: # Jiný formát zápisu
                otec_id = zpracuj_individualu(info.get('otec'))
                matka_id = zpracuj_individualu(info.get('matka'))
                
            # Propojíme králíka s jeho rodiči
            if otec_id or matka_id:
                self.nastav_rodice(k_id, otec_id, matka_id)
            
            return k_id

        # Spustíme proces od hlavního králíka
        hlavni_data = data.get('hlavni_kralik', data)
        if 'predci' in data:
            hlavni_data['predci'] = data['predci']
            
        return zpracuj_individualu(hlavni_data)
    
    def importuj_kompletni_rodokmen(self, data):
        """Zpracuje hierarchická data a propojí 14 předků v SQL."""
        def zpracuj_kralika(info):
            if not info or not info.get('levo'): return None
            
            # 1. Uložíme/Aktualizujeme králíka a získáme jeho ID
            k_id = self.uloz_kralika(info)
            
            # 2. Pokud má v datech své rodiče, uložíme je také (rekurze)
            otec_id = None
            matka_id = None
            
            if 'otec' in info:
                otec_id = zpracuj_kralika(info['otec'])
            if 'matka' in info:
                matka_id = zpracuj_kralika(info['matka'])
                
            # 3. Propojíme králíka s jeho rodiči
            if otec_id or matka_id:
                self.nastav_rodice(k_id, otec_id, matka_id)
            
            return k_id

        return zpracuj_kralika(data)
    
    def uloz_14_predku(self, hlavni_k_id, seznam_tetovani):
        """
        Vezme seznam tetování a postupně je propojí jako předky.
        Předpokládá pořadí: 0:Otec_L, 1:Otec_P, 2:Matka_L, 3:Matka_P...
        """
        if len(seznam_tetovani) >= 4:
            # Otec 
            o_id = self.uloz_kralika({'levo': seznam_tetovani[0], 'pravo': seznam_tetovani[1]})
            # Matka 
            m_id = self.uloz_kralika({'levo': seznam_tetovani[2], 'pravo': seznam_tetovani[3]})
            
            # Propojíme s hlavním králíkem
            self.nastav_rodice(hlavni_k_id, o_id, m_id)
            return True
        return False

    def smaz_kralika(self, id):
        self.cursor.execute("DELETE FROM kralici WHERE id=?", (id,))
        self.conn.commit()