import os
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, filedialog

def avvia_backup():
    # Prende la cartella scelta dall'utente
    dest_root = filedialog.askdirectory(title="Seleziona la cartella di destinazione per il backup")
    
    if not dest_root:
        return  # L'utente ha annullato

    # Crea una cartella con timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_dir = os.path.join(dest_root, f"Backup_{timestamp}")
    
    try:
        os.makedirs(backup_dir, exist_ok=True)
    except Exception as e:
        messagebox.showerror("Errore", f"Impossibile creare la cartella di backup:\n{e}")
        return

    user_profile = os.path.expanduser("~")
    count = 0

    # Controllo Documenti
    if var_docs.get():
        src = os.path.join(user_profile, "Documents")
        if os.path.exists(src):
            shutil.copytree(src, os.path.join(backup_dir, "Documents"), dirs_exist_ok=True)
            count += 1

    # Controllo Desktop
    if var_desktop.get():
        src = os.path.join(user_profile, "Desktop")
        if os.path.exists(src):
            shutil.copytree(src, os.path.join(backup_dir, "Desktop"), dirs_exist_ok=True)
            count += 1

    # Controllo Download
    if var_downloads.get():
        src = os.path.join(user_profile, "Downloads")
        if os.path.exists(src):
            shutil.copytree(src, os.path.join(backup_dir, "Downloads"), dirs_exist_ok=True)
            count += 1

    if count > 0:
        messagebox.showinfo("Completato", "Backup completato con successo!")
    else:
        messagebox.showwarning("Attenzione", "Nessun elemento selezionato.")

# Finestra Principale
root = tk.Tk()
root.title("Backup Tool - MattiYZ")
root.geometry("400x320")
root.resizable(False, False)

# Etichetta iniziale
lbl_title = tk.Label(root, text="Seleziona gli elementi da includere nel backup:", font=("Arial", 10))
lbl_title.pack(anchor="w", padx=30, pady=(25, 10))

# Variabili e Checkbox
var_docs = tk.BooleanVar()
chk_docs = tk.Checkbutton(root, text="Documenti", variable=var_docs, font=("Arial", 10))
chk_docs.pack(anchor="w", padx=35, pady=5)

var_desktop = tk.BooleanVar()
chk_desktop = tk.Checkbutton(root, text="Desktop", variable=var_desktop, font=("Arial", 10))
chk_desktop.pack(anchor="w", padx=35, pady=5)

var_downloads = tk.BooleanVar()
chk_downloads = tk.Checkbutton(root, text="Download", variable=var_downloads, font=("Arial", 10))
chk_downloads.pack(anchor="w", padx=35, pady=5)

# Pulsante di avvio
btn_backup = tk.Button(root, text="Avvia Backup", command=avvia_backup, width=15, height=2, bg="#e0e0e0")
btn_backup.pack(pady=20)

# Copyright in basso
lbl_copy = tk.Label(root, text="Creato Da MattiYZ - COPYRIGHT 2026", font=("Arial", 8, "italic"), fg="gray")
lbl_copy.pack(side="bottom", pady=10)

root.mainloop()
