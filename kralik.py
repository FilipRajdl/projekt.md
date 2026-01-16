class Kralik:
    def __init__(self, levo, pravo, jmeno, pohlavi="1,0", plemeno="", barva="",
                datum_vrhu="", naroz_ks=0, odchov_ks=0, registr_ks=0,
                hmotnost=0.0, body=0.0, chovatel="", adresa="",
                otec_id="", matka_id=""):
        
        self.levo = levo
        self.pravo = pravo
        self.id = f"{levo}/{pravo}"
        self.jmeno = jmeno
        self.pohlavi = pohlavi  # 1,0 nebo 0,1
        self.plemeno = plemeno
        self.barva = barva
        self.datum_vrhu = datum_vrhu
        self.naroz_ks = naroz_ks
        self.odchov_ks = odchov_ks
        self.registr_ks = registr_ks
        self.hmotnost = hmotnost
        self.body = body
        self.chovatel = chovatel
        self.adresa = adresa
        self.otec_id = otec_id
        self.matka_id = matka_id

    def to_dict(self):
        return self.__dict__
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)
            