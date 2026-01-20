import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
from docx import Document
from evidence import Registr
from kralik import Kralik

class Aplikace:
    def __init__(self, root):
        self.registr = Registr()
        self.root = root
        self.root.title("Registr chovu králíků")
        self.root.geometry("900x700")

        # --- HORNÍ PANEL (Hledání a přidávání) ---
        top_frame = tk.Frame(root, pady=10)
        top_frame.pack(fill="x", padx=10)

        tk.Button(top_frame, text="➕ Přidat nového králíka", command=self.novy_kralik_okno, bg="#4CAF50", fg="white").pack(side="left", padx=5)
        
        tk.Label(top_frame, text="🔍 Hledat:").pack(side="left", padx=(20, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.aktualizuj_tabulku(self.search_var.get()))
        tk.Entry(top_frame, textvariable=self.search_var, width=30).pack(side="left")

        # --- TABULKA ---
        self.tree = ttk.Treeview(root, columns=("id", "jmeno", "pohlavi", "plemeno"), show="headings")
        self.tree.heading("id", text="Tetování (L/P)")
        self.tree.heading("jmeno", text="Jméno")
        self.tree.heading("pohlavi", text="Pohlaví")
        self.tree.heading("plemeno", text="Plemeno")
        
        self.tree.column("id", width=120)
        self.tree.column("jmeno", width=150)
        self.tree.column("pohlavi", width=70)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Akce
        self.tree.bind("<Double-1>", self.otevri_detail)
        tk.Button(root, text="❌ Smazat vybraného", command=self.smazat_z_tabulky, bg="#f44336", fg="white").pack(pady=5)

        self.aktualizuj_tabulku()

    def aktualizuj_tabulku(self, filtr=""):
        for i in self.tree.get_children(): self.tree.delete(i)
        filtr = filtr.lower()
        for k in self.registr.seznam_kraliku.values():
            if not filtr or filtr in k.jmeno.lower() or filtr in k.id.lower():
                self.tree.insert("", "end", values=(k.id, k.jmeno, k.pohlavi, k.plemeno))

    def smazat_z_tabulky(self):
        vyber = self.tree.selection()
        if not vyber: return
        k_id = self.tree.item(vyber[0])['values'][0]
        if messagebox.askyesno("Smazat", f"Opravdu smazat králíka {k_id}?"):
            self.registr.smazat_kralika(k_id)
            self.aktualizuj_tabulku()

    def novy_kralik_okno(self):
        self.otevri_editor(None)

    def otevri_detail(self, event):
        vyber = self.tree.selection()
        if not vyber: return
        k_id = self.tree.item(vyber[0])['values'][0]
        kralik = self.registr.seznam_kraliku.get(k_id)
        self.otevri_editor(kralik)

    def otevri_editor(self, kralik):
        editor = tk.Toplevel(self.root)
        editor.title("Karta králíka")
        editor.geometry("650x750")

        notebook = ttk.Notebook(editor)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # --- ZÁLOŽKA 1: DATA ---
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="Základní údaje")

        fields = [
            ("Levé ucho (L. u.):", "levo"), ("Pravé ucho (P. u.):", "pravo"),
            ("Jméno:", "jmeno"), ("Pohlaví (1,0/0,1):", "pohlavi"),
            ("Plemeno:", "plemeno"), ("Barva:", "barva"),
            ("Datum vrhu:", "datum_vrhu"), ("Hmotnost (kg):", "hmotnost"),
            ("Ocenění (body):", "body"), ("Chovatel:", "chovatel"),
            ("Adresa chovatele:", "adresa"),
            ("Narozených (ks):", "naroz_ks"),
            ("Odchovaných (ks):", "odchov_ks"),
            ("Registrovaných (ks):", "registr_ks")
        ]
        
        entries = {}
        # Definujeme nápovědy pro jednotlivá pole
        napovedy = {
            "pohlavi": "1,0 = samec | 0,1 = samice",
            #"levo": "Organizace a měsíc (např. C 1-5)",
            #"pravo": "Rok a pořadové číslo (např. S-10)",
            "datum_vrhu": "Formát: 16. ledna 2026",
            "hmotnost": "Zadávejte v kg (např. 4.5)",
            "body": "Bodové hodnocení z výstavy",
            "otec_id": "Tetování otce ve formátu L/P",
            "matka_id": "Tetování matky ve formátu L/P"
        }

        for i, (label_text, attr) in enumerate(fields):
            # 1. Popisek (Label)
            tk.Label(tab1, text=label_text).grid(row=i, column=0, sticky="e", padx=5, pady=3)
            
            # 2. Vstupní pole (Entry)
            ent = tk.Entry(tab1, width=35)
            ent.grid(row=i, column=1, sticky="w", padx=5, pady=3)
            
            # Nastavení hodnoty, pokud upravujeme existujícího králíka
            if kralik: 
                ent.insert(0, getattr(kralik, attr))
            
            # 3. Nápověda (vedle políčka)
            text_napovedy = napovedy.get(attr, "")
            if text_napovedy:
                tk.Label(tab1, text=text_napovedy, font=("Arial", 8, "italic"), fg="#7f8c8d").grid(row=i, column=2, sticky="w", padx=10)

            # 4. Magická funkce ENTER (přeskok na další)
            # Pokud je to poslední pole, skočí na první tlačítko
            ent.bind("<Return>", lambda e: e.widget.tk_focusNext().focus())
            entries[attr] = ent

        # --- ZÁLOŽKA 2: RODOKMEN ---
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="Předci")
        
        tk.Label(tab2, text="ID Otce (L/P):").pack(pady=(20, 2))
        ent_otec = tk.Entry(tab2, width=30)
        ent_otec.pack()
        if kralik: ent_otec.insert(0, kralik.otec_id)

        tk.Label(tab2, text="ID Matky (L/P):").pack(pady=(10, 2))
        ent_matka = tk.Entry(tab2, width=30)
        ent_matka.pack()
        if kralik: ent_matka.insert(0, kralik.matka_id)

        # --- TLAČÍTKA EDITORU ---
        def ulozit():
            data = {attr: entries[attr].get() for _, attr in fields}
            data["otec_id"] = ent_otec.get()
            data["matka_id"] = ent_matka.get()
            
            novy = Kralik(**data)
            self.registr.uloz_kralika(novy)
            self.aktualizuj_tabulku()
            editor.destroy()
            messagebox.showinfo("Hotovo", "Králík byl uložen.")

        tk.Button(editor, text="💾 Uložit data", command=ulozit, bg="#4CAF50", fg="white", width=20, pady=10).pack(pady=5)
        
        if kralik:
            # Rámeček pro tisková tlačítka
            print_frame = tk.LabelFrame(editor, text="Tisk dokumentů", padx=10, pady=10)
            print_frame.pack(fill="x", padx=10, pady=10)

            tk.Button(print_frame, text="📜 Generovat jen RODOKMEN", 
                      command=lambda: self.generovat_jen_rodokmen(kralik), 
                      bg="#2196F3", fg="white", width=35).pack(pady=2)

            tk.Button(print_frame, text="📝 Generovat jen POTVRZENÍ", 
                      command=lambda: self.generovat_jen_potvrzeni(kralik), 
                      bg="#FF9800", fg="white", width=35).pack(pady=2)

            tk.Button(print_frame, text="🖨️ Generovat KOMPLETNÍ DOKUMENT", 
                      command=lambda: self.generovat_kompletni_dokument(kralik), 
                      bg="#4CAF50", fg="white", font=("Arial", 9, "bold"), width=35, pady=5).pack(pady=10)

    # --- OKNO PRO VÝBĚR PARTNERA ---
    def vyber_partnera(self, pohlavi_hledane):
        self.vybrany_partner = None
        
        okno_vyberu = tk.Toplevel(self.root)
        okno_vyberu.title(f"Vyberte {'Samce' if pohlavi_hledane == '1,0' else 'Samici'}")
        okno_vyberu.geometry("450x400")
        okno_vyberu.grab_set() # Zablokuje ostatní okna, dokud nevyberete

        tk.Label(okno_vyberu, text="Dvojklikem vyberte partnera ze seznamu:", font=("Arial", 10, "bold")).pack(pady=10)

        tree = ttk.Treeview(okno_vyberu, columns=("id", "jmeno"), show="headings")
        tree.heading("id", text="Tetování")
        tree.heading("jmeno", text="Jméno")
        tree.pack(fill="both", expand=True, padx=10, pady=5)

        # Naplníme jen králíky opačného pohlaví
        for k in self.registr.seznam_kraliku.values():
            if k.pohlavi == pohlavi_hledane:
                tree.insert("", "end", values=(k.id, k.jmeno))

        def potvrdit(event=None):
            vyber = tree.selection()
            if vyber:
                k_id = tree.item(vyber[0])['values'][0]
                self.vybrany_partner = self.registr.seznam_kraliku.get(str(k_id))
                okno_vyberu.destroy()

        tree.bind("<Double-1>", potvrdit)
        tk.Button(okno_vyberu, text="✅ Potvrdit výběr", command=potvrdit, bg="#4CAF50", fg="white", pady=5).pack(pady=10)
        
        self.root.wait_window(okno_vyberu)
        return self.vybrany_partner

    # --- UPRAVENÉ FUNKCE PRO TISK ---

    def generovat_jen_potvrzeni(self, kralik):
        # Místo dialogu otevřeme naše nové okno
        opacne_pohlavi = "0,1" if kralik.pohlavi == "1,0" else "1,0"
        partner = self.vyber_partnera(opacne_pohlavi)
        
        if not partner: return # Uživatel nic nevybral
        
        try:
            doc = Document(os.path.join(os.path.dirname(os.path.abspath(__file__)), "rodokmen.docx"))
            nahrady = self._priprav_data_potvrzeni(kralik, partner)
            self._proved_nahrazeni(doc, nahrady)
            nazev = f"Potvrzeni_{kralik.id.replace('/', '-')}.docx"
            doc.save(nazev)
            os.startfile(nazev)
        except Exception as e: messagebox.showerror("Chyba", str(e))

    def generovat_kompletni_dokument(self, kralik):
        # 1. Výběr partnera
        opacne_pohlavi = "0,1" if kralik.pohlavi == "1,0" else "1,0"
        partner = self.vyber_partnera(opacne_pohlavi)
        if not partner: return

        # 2. Dotaz na datum krytí
        datum_kryti = simpledialog.askstring("Datum krytí", "Zadejte datum krytí:", initialvalue="1. 1. 2026")
        
        # 3. Určení samce a samice pro potvrzení
        samec = kralik if kralik.pohlavi == "1,0" else partner
        samice = kralik if kralik.pohlavi == "0,1" else partner

        # 4. Kontrola počtu mláďat - pokud je v kartě 0, zeptáme se
        narozeno = samice.naroz_ks
        if str(narozeno) == "0":
            narozeno = simpledialog.askstring("Počet mláďat", "Kolik se narodilo mláďat?", initialvalue="0")
        
        odchovano = samice.odchov_ks
        if str(odchovano) == "0":
            odchovano = simpledialog.askstring("Počet mláďat", "Kolik se odchovalo mláďat?", initialvalue="0")

        try:
            doc = Document(os.path.join(os.path.dirname(__file__), "rodokmen.docx"))
            
            # Nahrady pro rodokmen
            nahrady = self._ziskej_nahrady_rodokmenu(kralik)
            
            # Nahrady pro připouštěcí potvrzení
            nahrady.update({
                "{{m_majitel}}": samec.chovatel,
                "{{m_adresa}}": samec.adresa,
                "{{s_majitel}}": samice.chovatel,
                "{{s_adresa}}": samice.adresa,
                "{{k_datum}}": datum_kryti if datum_kryti else "....................",
                "{{v_nar}}": str(narozeno),
                "{{v_odch}}": str(odchovano),
                "{{p_plemeno}}": samice.plemeno,
                "{{p_barva}}": samice.barva
            })

            self._proved_nahrazeni(doc, nahrady)
            nazev = f"Kompletni_{kralik.id.replace('/', '-')}.docx"
            doc.save(nazev)
            os.startfile(nazev)
        except Exception as e:
            messagebox.showerror("Chyba", str(e))

    def _priprav_data_potvrzeni(self, kralik, partner):
        # Rozlišíme kdo je kdo
        samec = kralik if kralik.pohlavi == "1,0" else partner
        samice = kralik if kralik.pohlavi == "0,1" else partner
        
        # Tady se plní ty údaje, co ti chyběly
        return {
            "{{m_majitel}}": samec.chovatel if samec else "",
            "{{m_adresa}}": samec.adresa if samec else "",
            "{{s_majitel}}": samice.chovatel if samice else "",
            "{{s_adresa}}": samice.adresa if samice else "",
            "{{p_plemeno}}": samice.plemeno if samice else "",
            "{{p_barva}}": samice.barva if samice else "",
            "{{v_nar}}": str(samice.naroz_ks) if samice else "0",
            "{{v_odch}}": str(samice.odchov_ks) if samice else "0",
            "{{v_reg}}": str(samice.registr_ks) if samice else "0"
        }


    def _ziskej_nahrady_rodokmenu(self, kralik):
        """Funkce, která připraví balík dat pro rodokmen."""
        def get_anc(k_id, prefix, level):
            def vycisti(t): return str(t).replace(" ", "").lower() if t else ""
            target = vycisti(k_id)
            k = None
            if target:
                for rk in self.registr.seznam_kraliku.values():
                    if vycisti(rk.id) == target:
                        k = rk
                        break
            data = {}
            if k:
                data[f"{{{{{prefix}_l}}}}"] = k.levo
                data[f"{{{{{prefix}_p}}}}"] = k.pravo
                data[f"{{{{{prefix}_ch}}}}"] = f"{k.chovatel}, {k.adresa}"
                if level == 1:
                    data[f"{{{{{prefix}_pl}}}}"] = k.plemeno
                    data[f"{{{{{prefix}_dv}}}}"] = k.datum_vrhu
                data["o"], data["m"] = k.otec_id, k.matka_id
            else:
                keys = ["l", "p", "ch"]
                if level == 1: keys += ["pl", "dv"]
                for key in keys: data[f"{{{{{prefix}_{key}}}}}"] = ""
                data["o"], data["m"] = None, None
            return data

        nahrady = {
            "{{jmeno}}": kralik.jmeno, "{{levo}}": kralik.levo, "{{pravo}}": kralik.pravo,
            "{{plemeno}}": kralik.plemeno, "{{datum_vrhu}}": kralik.datum_vrhu,
            "{{chovatel}}": kralik.chovatel, "{{adresa}}": kralik.adresa,
            "{{hmotnost}}": str(kralik.hmotnost), "{{body}}": str(kralik.body),
            "{{v_reg}}": str(kralik.registr_ks) if kralik.registr_ks else "0"
        }
        o = get_anc(kralik.otec_id, "otec", 1); m = get_anc(kralik.matka_id, "matka", 1)
        oo = get_anc(o["o"], "oo", 2); mo = get_anc(o["m"], "mo", 2)
        om = get_anc(m["o"], "om", 2); mm = get_anc(m["m"], "mm", 2)
        ooo = get_anc(oo["o"], "ooo", 3); moo = get_anc(oo["m"], "moo", 3)
        omo = get_anc(mo["o"], "omo", 3); mmo = get_anc(mo["m"], "mmo", 3)
        oom = get_anc(om["o"], "oom", 3); mom = get_anc(om["m"], "mom", 3)
        omm = get_anc(mm["o"], "omm", 3); mmm = get_anc(mm["m"], "mmm", 3)
        
        for d in [o, m, oo, mo, om, mm, ooo, moo, omo, mmo, oom, mom, omm, mmm]:
            nahrady.update({k: v for k, v in d.items() if str(k).startswith("{")})
        return nahrady

    # --- 1. TLAČÍTKO: JEN RODOKMEN ---
    def generovat_jen_rodokmen(self, kralik):
        try:
            doc = Document(os.path.join(os.path.dirname(__file__), "rodokmen.docx"))
            nahrady = self._ziskej_nahrady_rodokmenu(kralik)
            self._proved_nahrazeni(doc, nahrady)
            nazev = f"Rodokmen_{kralik.id.replace('/', '-')}.docx"
            doc.save(nazev)
            os.startfile(nazev)
        except Exception as e: messagebox.showerror("Chyba", str(e))

    # --- 2. TLAČÍTKO: JEN POTVRZENÍ ---
    def generovat_jen_potvrzeni(self, kralik):
        partner_id = simpledialog.askstring("Párování", "Zadejte tetování partnera:")
        if not partner_id: return
        try:
            doc = Document(os.path.join(os.path.dirname(__file__), "rodokmen.docx"))
            nahrady = self._priprav_data_potvrzeni(kralik, partner_id)
            self._proved_nahrazeni(doc, nahrady)
            nazev = f"Potvrzeni_{kralik.id.replace('/', '-')}.docx"
            doc.save(nazev)
            os.startfile(nazev)
        except Exception as e: messagebox.showerror("Chyba", str(e))

    # --- 3. TLAČÍTKO: KOMPLETNÍ DOKUMENT ---
    def generovat_kompletni_dokument(self, kralik):
        # 1. Výběr partnera
        opacne_pohlavi = "0,1" if kralik.pohlavi == "1,0" else "1,0"
        partner = self.vyber_partnera(opacne_pohlavi)
        
        if not partner:
            messagebox.showwarning("Pozor", "Pro kompletní dokument s potvrzením je nutné vybrat partnera.")
            return

        # 2. Dotaz na datum krytí (tohle v programu chybělo)
        datum_kryti = simpledialog.askstring("Datum krytí", "Zadejte datum krytí (např. 1. 5. 2025):")
        if not datum_kryti: datum_kryti = "...................."

        try:
            adresar_projektu = os.path.dirname(os.path.abspath(__file__))
            cesta_k_sablone = os.path.join(adresar_projektu, "rodokmen.docx")
            doc = Document(cesta_k_sablone)

            # Sběr dat pro rodokmen (předci)
            nahrady = self._ziskej_nahrady_rodokmenu(kralik)

            # Sběr dat pro připouštěcí potvrzení
            samec = kralik if kralik.pohlavi == "1,0" else partner
            samice = kralik if kralik.pohlavi == "0,1" else partner

            # Kontrola majitelů - pokud v kartě chybí, použijeme text z dialogu nebo prázdno
            m_jmeno = samec.chovatel if samec.chovatel else "Doplnit ručně"
            m_adr = samec.adresa if samec.adresa else ""
            s_jmeno = samice.chovatel if samice.chovatel else "Doplnit ručně"
            s_adr = samice.adresa if samice.adresa else ""

            nahrady.update({
                "{{m_majitel}}": m_jmeno,
                "{{m_adresa}}": m_adr,
                "{{s_majitel}}": s_jmeno,
                "{{s_adresa}}": s_adr,
                "{{p_plemeno}}": samice.plemeno,
                "{{p_barva}}": samice.barva,
                "{{k_datum}}": datum_kryti,
                "{{v_nar}}": str(samice.naroz_ks) if int(samice.naroz_ks) > 0 else "0",
                "{{v_odch}}": str(samice.odchov_ks) if int(samice.odchov_ks) > 0 else "0"
            })

            # Provedení nahrazení
            self._proved_nahrazeni(doc, nahrady)

            nazev = f"Kompletni_{kralik.id.replace('/', '-')}.docx"
            doc.save(nazev)
            os.startfile(nazev)
            
        except Exception as e:
            messagebox.showerror("Chyba", f"Generování selhalo: {e}")

    # --- POMOCNÉ METODY PRO VÝŠE UVEDENÉ FUNKCE ---
    def _priprav_data_potvrzeni(self, kralik, partner_id):
        p_id_cisty = partner_id.replace(" ", "").lower()
        partner = None
        for k in self.registr.seznam_kraliku.values():
            if k.id.replace(" ", "").lower() == p_id_cisty:
                partner = k
                break
        
        samec = kralik if kralik.pohlavi == "1,0" else partner
        samice = kralik if kralik.pohlavi == "0,1" else partner
        
        return {
            "{{m_majitel}}": samec.chovatel if samec else "---",
            "{{m_adresa}}": samec.adresa if samec else "---",
            "{{s_majitel}}": samice.chovatel if samice else "---",
            "{{s_adresa}}": samice.adresa if samice else "---",
            "{{p_plemeno}}": samice.plemeno if samice else "---",
            "{{p_barva}}": samice.barva if samice else "---",
            "{{v_nar}}": str(samice.naroz_ks) if samice else "0",
            "{{v_odch}}": str(samice.odchov_ks) if samice else "0"
        }

    def _proved_nahrazeni(self, doc, nahrady):
        for p in doc.paragraphs:
            for k, v in nahrady.items():
                if k in p.text: p.text = p.text.replace(k, str(v))
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for k, v in nahrady.items():
                        if k in cell.text: cell.text = cell.text.replace(k, str(v))

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplikace(root)
    root.mainloop()