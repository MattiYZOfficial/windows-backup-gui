#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nome script: install_basicapp.py
Creato Da: MattiYZ
Copyright © 2026 MattiYZ. Tutti i diritti riservati.
Descrizione: Tool grafico per l'installazione automatica di applicazioni per ufficio e produttività tramite Chocolatey.
"""

import os
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk

# Lista delle app pensate per l'ufficio e la produttività (senza gaming)
APPLICAZIONI = [
    ("Google Chrome", "googlechrome"),
    ("Mozilla Firefox", "firefox"),
    ("LibreOffice", "libreoffice-fresh"),
    ("Adobe Acrobat Reader", "adobereader"),
    ("Microsoft PowerToys", "powertoys"),
    ("7-Zip", "7zip"),
    ("Thunderbird (Email)", "thunderbird"),
    ("Zoom", "zoom"),
    ("Microsoft Teams", "microsoft-teams"),
    ("Notepad++", "notepadplusplus"),
    ("Git", "git"),
    ("Visual Studio Code", "vscode")
]

def verifica_e_installa_choco():
    chk = subprocess.run("choco --version", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if chk.returncode != 0:
        messagebox.showinfo("Chocolatey", "Chocolatey non trovato. Verrà installato automaticamente (richiede permessi di Amministratore).")
        cmd_choco = "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
        res = subprocess.run(f'powershell -Command "Start-Process powershell -ArgumentList \'-NoProfile -ExecutionPolicy Bypass -Command \\"{cmd_choco}\\"\' -Verb RunAs"', shell=True)
        return res.returncode == 0
    return True

def avvia_installazione():
    selezionate = [pkg for (nome, pkg), var in zip(APPLICAZIONI, checkboxes_vars) if var.get()]
    
    if not selezionate:
        messagebox.showwarning("Attenzione", "Seleziona almeno un'applicazione da installare.")
        return

    if not verifica_e_installa_choco():
        messagebox.showerror("Errore", "Impossibile configurare Chocolatey. L'installazione è stata annullata.")
        return

    progress['maximum'] = len(selezionate)
    progress['value'] = 0
    root.update_idletasks()

    completate = 0
    for i, pkg in enumerate(selezionate):
        cmd = f'powershell -Command "Start-Process powershell -ArgumentList \'-NoProfile -Command choco install {pkg} -y\' -Verb RunAs -Wait"'
        res = subprocess.run(cmd, shell=True)
        
        completate += 1
        progress['value'] = completate
        root.update_idletasks()

    messagebox.showinfo("Completato", "Installazione delle applicazioni da ufficio completata!")
    progress['value'] = 0

# Finestra Principale
root = tk.Tk()
root.title("Office & Productivity Installer - MattiYZ")
root.geometry("420x550")
root.resizable(False, False)

# Titolo
lbl_title = tk.Label(root, text="Seleziona i programmi per ufficio e produttività:", font=("Arial", 10, "bold"))
lbl_title.pack(anchor="w", padx=30, pady=(20, 10))

# Generazione dinamica delle checkbox
checkboxes_vars = []
for nome, pkg in APPLICAZIONI:
    var = tk.BooleanVar(value=False)
    chk = tk.Checkbutton(root, text=nome, variable=var, font=("Arial", 10))
    chk.pack(anchor="w", padx=35, pady=2)
    checkboxes_vars.append(var)

# Barra di caricamento
progress = ttk.Progressbar(root, orient="horizontal", length=350, mode="determinate")
progress.pack(pady=15)

# Pulsante di avvio
btn_install = tk.Button(root, text="Avvia Installazione", command=avvia_installazione, width=18, height=2, bg="#e0e0e0")
btn_install.pack(pady=5)

# Copyright in basso
lbl_copy = tk.Label(root, text="Creato Da MattiYZ - COPYRIGHT 2026", font=("Arial", 8, "italic"), fg="gray")
lbl_copy.pack(side="bottom", pady=10)

root.mainloop()
