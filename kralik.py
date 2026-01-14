class Kralik:
    def __init__(self, levo, pravo, jmeno, pohlavi, otec_id=None, matka_id=None):
        self.levo = levo # Tetovací číslo na levém uchu
        self.pravo = pravo # Tetovací číslo na pravém uchu
        self.jmeno = jmeno
        self.pohlavi = pohlavi
        self.otec_id = otec_id
        self.matka_id = matka_id
        self.vaha_historie = [] #Datum a vaha
        self.vystavy = []   #Bodove hondnoceni z vystav
        self.id = f"{levo}/{pravo}" # Unikatni identifikator kralika

    def to_dict(self):
        return {
            "levo": self.levo,
            "pravo": self.pravo,
            "jmeno": self.jmeno,
            "pohlavi": self.pohlavi,
            "otec_id": self.otec_id,
            "matka_id": self.matka_id,
            "vaha_historie": self.vaha_historie,
            "vystavy": self.vystavy,
        }