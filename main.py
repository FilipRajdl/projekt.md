import tkinter as tk
from tkinter import messagebox
from evidence import Registr
from kralik import Kralik

class Aplikace:
    def __init__(self, root):
        self.registr = Registr()
        self.root = root
        self.root.title("Registr chovu králíků")
        self.root.geometry("400x300")
        
        tk.Label(root, text="Levé ucho (např. C 5-4):", font=("Arial", 10, "bold")).pack(pady=5)
        self.entry_levo = tk.Entry(root)
        self.entry_levo.pack()

        tk.Label(root, text="Pravé ucho (např. S-123):", font=("Arial", 10, "bold")).pack(pady=5)
        self.entry_pravo = tk.Entry(root)
        self.entry_pravo.pack()

        tk.Label(root, text="Jméno králíka:").pack()
        self.entry_jmeno = tk.Entry(root)
        self.entry_jmeno.pack()

        tk.Label(root, text="Pohlaví (S/Samice):").pack(pady=5)
        self.entry_pohlavi = tk.Entry(root)
        self.entry_pohlavi.pack()

# --- Tlačítka ---
        self.btn_ulozit = tk.Button(root, text="Uložit do registru", command=self.ulozit, bg="#4CAF50", fg="white")
        self.btn_ulozit.pack(pady=20)

        self.btn_vypis = tk.Button(root, text="Zobrazit seznam", command=self.vypis)
        self.btn_vypis.pack()

    def ulozit(self):
        levo = self.entry_levo.get()
        pravo = self.entry_pravo.get()
        jmeno = self.entry_jmeno.get()
        pohlavi = self.entry_pohlavi.get()

        if levo and pravo and jmeno:
            novy = Kralik(levo, pravo, jmeno, pohlavi)
            if self.registr.pridat_kralika(novy):
                messagebox.showinfo("Hotovo", f"Králík {levo, pravo} byl uložen do souboru.")
                self.smaz_pole()
            else:
                messagebox.showerror("Chyba", "Tento králík (kombinace uší) již v registru je.")
        else:
            messagebox.showwarning("Pozor", "Vyplňte prosím levé ucho, pravé ucho i jméno.")
        
    def smaz_pole(self):
        self.entry_levo.delete(0, tk.END)
        self.entry_pravo.delete(0, tk.END)
        self.entry_jmeno.delete(0, tk.END)
        self.entry_pohlavi.delete(0, tk.END)

    def vypis(self):
        print("\n--- AKTUÁLNÍ SEZNAM KRÁLÍKŮ V REGISTRU ---")
        for k in self.registr.seznam_kraliku.values():
            print(f"ID: {k.id} | Jméno: {k.jmeno} | Pohlaví: {k.pohlavi}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplikace(root)
    root.mainloop()