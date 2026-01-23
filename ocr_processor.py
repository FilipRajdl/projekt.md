import pytesseract
import cv2
import re
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\rajdl\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

class OcrProcessor:
    def nacti_data_z_obrazku(self, cesta):
        if not os.path.exists(cesta): return {}

        img = cv2.imread(cesta)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Standardní vyčištění bez zvětšování (aby tam nebylo tolik šumu)
        processed = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        
        text = pytesseract.image_to_string(processed, lang='ces', config='--psm 3')
        
        # Výpis pro tvou kontrolu v terminálu
        print("\n" + "="*40)
        print("CO PROGRAM SKUTEČNĚ VIDÍ:")
        print(text)
        print("="*40 + "\n")
        
        vysledky = {}

        # 1. PLEMENO (Burgundský)
        if "rgund" in text.lower() or "burgu" in text.lower():
            vysledky['plemeno'] = "Burgundský"

        # 2. LEVÉ UCHO (Hledáme za 'levé ucho')
        # Zkusíme najít text, který následuje po 'levé ucho'
        lu_match = re.search(r'levé ucho[:.\s]*([A-Z0-9\-\s]+)', text, re.I)
        if lu_match:
            raw_lu = lu_match.group(1).strip()
            # Vezmeme jen první kousek (před případným dalším textem)
            clean_lu = re.search(r'([A-Z0-9]+[-\s]*[A-Z0-9]+)', raw_lu)
            if clean_lu:
                vysledky['levo'] = "C " + clean_lu.group(1).replace(" ", "")

        # 3. PRAVÉ UCHO
        pu_match = re.search(r'pravé ucho[:.\s]*([0-9\-\s]+)', text, re.I)
        if pu_match:
            vysledky['pravo'] = pu_match.group(1).strip().split()[0].replace(" ", "")

        # 4. DATUM VRHU
        dat_match = re.search(r'(\d{1,2}\s+[a-zěščřžýáíé]+\s+\d{4})', text, re.I)
        if dat_match:
            vysledky['datum_vrhu'] = dat_match.group(1).strip()

        # 5. POČTY MLÁĎAT 
        # Hledáme číslo hned za slovem
        narozeni = re.search(r'narozených\s+(\d+)', text, re.I)
        if narozeni: vysledky['naroz_ks'] = narozeni.group(1)

        odchovani = re.search(r'odchovaných\s+(\d+)', text, re.I)
        if odchovani: vysledky['odchov_ks'] = odchovani.group(1)

        registrovani = re.search(r'registrovaných\s+(\d+)', text, re.I)
        if registrovani: vysledky['registr_ks'] = registrovani.group(1)

        return vysledky


    def nacti_zadni_stranu(self, cesta):
        # Načtení a vylepšení kontrastu pro lepší čtení tabulek
        img = cv2.imread(cesta)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        processed = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        
        text = pytesseract.image_to_string(processed, lang='ces', config='--psm 3')
        
        # Hledáme vzory tetování: C 1-2, S-123, 6-1 atd.
        # Regex hledá písmeno (volitelně), mezeru a čísla s pomlčkou
        vzor = r'([A-Z]*\s*\d+[\s.-]+\d+)'
        nalezy = re.findall(vzor, text)
        
        # Vyčištění nálezů (odstranění mezer navíc)
        cista_tetovani = []
        for n in nalezy:
            clean = n.strip().replace(" ", "")
            if len(clean) > 2:
                # Pokusíme se vrátit formát s mezerou za písmenem pro čitelnost
                if clean[0].isalpha():
                    clean = f"{clean[0]} {clean[1:]}"
                cista_tetovani.append(clean)
        
        return cista_tetovani

    # pytesseract.pytesseract.tesseract_cmd = r'C:\Users\rajdl\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'