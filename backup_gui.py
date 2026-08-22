import os
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, filedialog, ttk

def avvia_backup():
    dest_root = filedialog.askdirectory(title="Seleziona la cartella di destinazione per il backup")
    if not dest_root:
        return

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_dir = os.path.join(dest_root, f"Backup_{timestamp}")
    
    try:
        os.makedirs(backup_dir, exist_ok=True)
    except Exception as e:
        messagebox.showerror("Errore", f"Impossibile creare la cartella di backup:\n{e}")
        return

    user_profile = os.path.expanduser("~")
    
    # Lista delle cartelle da controllare e copiare
    elementi = [
        ("Documents", var_docs.get()),
        ("Desktop", var_desktop.get()),
        ("Downloads", var_downloads.get()),
        ("Music", var_music.get()),
        ("Pictures", var_pictures.get()),
        ("Videos", var_videos.get())
    ]
    
    # Filtriamo solo quelle selezionate che esistono davvero sul pc
    da_copiare = [nome for nome, selezionato in elementi if selezionato]
    
    if not da_copiare:
        messagebox.showwarning("Attenzione", "Seleziona almeno un elemento da salvare.")
        return

    # Configuriamo la barra di progresso
    progress['maximum'] = len(da_copiare)
    progress['value'] = 0
    root.update_idletasks()

    copionati = 0
    for nome in da_copiare:
        src = os.path.join(user_profile, nome)
        if os.path.exists(src):
            try:
                shutil.copytree(src, os.path.join(backup_dir, nome), dirs_exist_ok=True)
                copionati += 1
            except Exception as ex:
                print(f"Errore con {nome}: {ex}")
        
        progress['value'] = copionati
        root.update_idletasks()

    if copionati > 0:
        messagebox.showinfo("Completato", f"Backup completato con successo!\nSalvato in: {backup_dir}")
    else:
        messagebox.showwarning("Attenzione", "Nessuna cartella trovata sul sistema.")

    progress['value'] = 0

# Finestra Principale
root = tk.Tk()
root.title("Backup Tool - MattiYZ")
root.geometry("420x440")
root.resizable(False, False)

# Titolo
lbl_title = tk.Label(root, text="Seleziona gli elementi da includere nel backup:", font=("Arial", 10, "bold"))
lbl_title.pack(anchor="w", padx=30, pady=(20, 10))

# Variabili e Checkbox
var_docs = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Documenti", variable=var_docs, font=("Arial", 10)).pack(anchor="w", padx=35, pady=3)

var_desktop = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Desktop", variable=var_desktop, font=("Arial", 10)).pack(anchor="w", padx=35, pady=3)

var_downloads = tk.BooleanVar()
tk.Checkbutton(root, text="Download", variable=var_downloads, font=("Arial", 10)).pack(anchor="w", padx=35, pady=3)

var_music = tk.BooleanVar()
tk.Checkbutton(root, text="Musica", variable=var_music, font=("Arial", 10)).pack(anchor="w", padx=35, pady=3)

var_pictures = tk.BooleanVar()
tk.Checkbutton(root, text="Immagini", variable=var_pictures, font=("Arial", 10)).pack(anchor="w", padx=35, pady=3)

var_videos = tk.BooleanVar()
tk.Checkbutton(root, text="Video", variable=var_videos, font=("Arial", 10)).pack(anchor="w", padx=35, pady=3)

# Barra di caricamento
progress = ttk.Progressbar(root, orient="horizontal", length=350, mode="determinate")
progress.pack(pady=15)

# Pulsante di avvio
btn_backup = tk.Button(root, text="Avvia Backup", command=avvia_backup, width=18, height=2, bg="#e0e0e0")
btn_backup.pack(pady=5)

# Copyright in basso
lbl_copy = tk.Label(root, text="Creato Da MattiYZ - COPYRIGHT 2026", font=("Arial", 8, "italic"), fg="gray")
lbl_copy.pack(side="bottom", pady=10)

root.mainloop()
