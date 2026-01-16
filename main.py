import tkinter as tk
from tkinter import ttk, messagebox
from evidence import Registr
from kralik import Kralik

class Aplikace:
    def __init__(self, root):
        self.registr = Registr()
        self.root = root
        self.root.title("Registr králíků")
        self.root.geometry("800x600")

        # --- HLAVNÍ MENU A TABULKA ---
        top_frame = tk.Frame(root)
        top_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Button(top_frame, text="+ Přidat nového králíka", command=self.novy_kralik_okno).pack(side="left")
        
        # Tabulka
        self.tree = ttk.Treeview(root, columns=("id", "jmeno", "pohlavi", "plemeno"), show="headings")
        self.tree.heading("id", text="Tetování"); self.tree.heading("jmeno", text="Jméno")
        self.tree.heading("pohlavi", text="Pohlaví"); self.tree.heading("plemeno", text="Plemeno")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Dvojklik pro detail
        self.tree.bind("<Double-1>", self.otevri_detail)
        
        self.aktualizuj_tabulku()

    def aktualizuj_tabulku(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for k in self.registr.seznam_kraliku.values():
            self.tree.insert("", "end", values=(k.id, k.jmeno, k.pohlavi, k.plemeno))

    def novy_kralik_okno(self):
        # Otevře okno pro zadání základních dat
        self.otevri_editor(None)

    def otevri_detail(self, event):
        vyber = self.tree.selection()
        if not vyber: return
        k_id = self.tree.item(vyber[0])['values'][0]
        kralik = self.registr.seznam_kraliku.get(k_id)
        self.otevri_editor(kralik)

    def otevri_editor(self, kralik):
        editor = tk.Toplevel(self.root)
        editor.title("Karta králíka / Editor")
        editor.geometry("600x700")

        notebook = ttk.Notebook(editor)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # --- ZÁLOŽKA 1: ZÁKLADNÍ ÚDAJE ---
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="Základní údaje")

        # Dynamické vytvoření políček na základě tvého Wordu
        fields = [
            ("Levé ucho:", "levo"), ("Pravé ucho:", "pravo"),
            ("Jméno:", "jmeno"), ("Pohlaví (1,0/0,1):", "pohlavi"),
            ("Plemeno:", "plemeno"), ("Barva:", "barva"),
            ("Datum vrhu:", "datum_vrhu"), ("Hmotnost (kg):", "hmotnost"),
            ("Ocenění (b):", "body"), ("Chovatel:", "chovatel"),
            ("Adresa chovatele:", "adresa")
        ]
        
        self.entries = {}
        for i, (label, attr) in enumerate(fields):
            tk.Label(tab1, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=2)
            ent = tk.Entry(tab1)
            ent.grid(row=i, column=1, sticky="w", padx=5, pady=2)
            if kralik: ent.insert(0, getattr(kralik, attr))
            self.entries[attr] = ent

        # --- ZÁLOŽKA 2: RODOKMEN ---
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="Rodokmen")
        
        
        tk.Label(tab2, text="Zde bude vizuální strom předků", font=("Arial", 12, "italic")).pack(pady=20)
        
        # Pole pro ID rodičů
        tk.Label(tab2, text="ID Otce (L/P):").pack()
        self.ent_otec = tk.Entry(tab2)
        self.ent_otec.pack()
        if kralik: self.ent_otec.insert(0, kralik.otec_id)

        tk.Label(tab2, text="ID Matky (L/P):").pack()
        self.ent_matka = tk.Entry(tab2)
        self.ent_matka.pack()
        if kralik: self.ent_matka.insert(0, kralik.matka_id)

        # --- TLAČÍTKA ---
        def ulozit():
            try:
                data = {attr: self.entries[attr].get() for _, attr in fields}
                data["otec_id"] = self.ent_otec.get()
                data["matka_id"] = self.ent_matka.get()
                novy = Kralik(**data)
                self.registr.uloz_kralika(novy)
                self.aktualizuj_tabulku()
                editor.destroy()
                messagebox.showinfo("Uloženo", "Data byla úspěšně uložena do databáze.")
            except Exception as e:
                    messagebox.showerror("Chyba při ukládání", f"Nepodařilo se uložit: {e}")

        tk.Button(editor, text="💾 Uložit králíka", command=ulozit, bg="#4CAF50", fg="white").pack(pady=10)
        
        if kralik:
            tk.Button(editor, text="🖨️ Vyplnit Word Rodokmen", command=lambda: messagebox.showinfo("Tisk", "Generuji Rodokmen...")).pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplikace(root)
    root.mainloop()
