<#
.SYNOPSIS
    Tool di Backup con Interfaccia Grafica per Windows
.AUTHOR
    Creato Da MattiYZ - COPYRIGHT 2026
#>

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Creazione della Finestra Principale
$form = New-Object System.Windows.Forms.Form
$form.Text = "Backup Tool - MattiYZ"
$form.Size = New-Object System.Drawing.Size(400, 370)
$form.StartPosition = "CenterScreen"
$form.FormBorderStyle = "FixedDialog"
$form.MaximizeBox = $false

# Etichetta di benvenuto
$label = New-Object System.Windows.Forms.Label
$label.Location = New-Object System.Drawing.Point(20, 20)
$label.Size = New-Object System.Drawing.Size(340, 20)
$label.Text = "Seleziona gli elementi da includere nel backup:"
$form.Controls.Add($label)

# Checkbox per Documenti
$chkDocs = New-Object System.Windows.Forms.CheckBox
$chkDocs.Location = New-Object System.Drawing.Point(30, 60)
$chkDocs.Size = New-Object System.Drawing.Size(300, 24)
$chkDocs.Text = "Documenti"
$form.Controls.Add($chkDocs)

# Checkbox per Desktop
$chkDesktop = New-Object System.Windows.Forms.CheckBox
$chkDesktop.Location = New-Object System.Drawing.Point(30, 90)
$chkDesktop.Size = New-Object System.Drawing.Size(300, 24)
$chkDesktop.Text = "Desktop"
$form.Controls.Add($chkDesktop)

# Checkbox per Download
$chkDownloads = New-Object System.Windows.Forms.CheckBox
$chkDownloads.Location = New-Object System.Drawing.Point(30, 120)
$chkDownloads.Size = New-Object System.Drawing.Size(300, 24)
$chkDownloads.Text = "Download"
$form.Controls.Add($chkDownloads)

# Pulsante di Avvio
$btnBackup = New-Object System.Windows.Forms.Button
$btnBackup.Location = New-Object System.Drawing.Point(130, 210)
$btnBackup.Size = New-Object System.Drawing.Size(120, 35)
$btnBackup.Text = "Avvia Backup"
$form.Controls.Add($btnBackup)

# Etichetta Copyright in basso
$lblCopyright = New-Object System.Windows.Forms.Label
$lblCopyright.Location = New-Object System.Drawing.Point(20, 280)
$lblCopyright.Size = New-Object System.Drawing.Size(340, 20)
$lblCopyright.Text = "Creato Da MattiYZ - COPYRIGHT 2026"
$lblCopyright.TextAlign = [System.Drawing.ContentAlignment]::MiddleCenter
$lblCopyright.Font = New-Object System.Drawing.Font("Microsoft Sans Serif", 8, [System.Drawing.FontStyle]::Italic)
$form.Controls.Add($lblCopyright)

# Azione al click del pulsante
$btnBackup.Add_Click({
    $fbd = New-Object System.Windows.Forms.FolderBrowserDialog
    $fbd.Description = "Seleziona la cartella di destinazione per il backup"
    
    if ($fbd.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
        $destRoot = $fbd.SelectedPath
        $timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
        $backupDir = Join-Path $destRoot "Backup_$timestamp"
        New-Item -ItemType Directory -Path $backupDir | Out-Null

        $userProfile = $env:USERPROFILE
        $count = 0

        if ($chkDocs.Checked) {
            $source = Join-Path $userProfile "Documents"
            if (Test-Path $source) {
                Copy-Item -Path $source -Destination $backupDir -Recurse -Force
                $count++
            }
        }

        if ($chkDesktop.Checked) {
            $source = Join-Path $userProfile "Desktop"
            if (Test-Path $source) {
                Copy-Item -Path $source -Destination $backupDir -Recurse -Force
                $count++
            }
        }

        if ($chkDownloads.Checked) {
            $source = Join-Path $userProfile "Downloads"
            if (Test-Path $source) {
                Copy-Item -Path $source -Destination $backupDir -Recurse -Force
                $count++
            }
        }

        if ($count -gt 0) {
            [System.Windows.Forms.MessageBox]::Show("Backup completato con successo!", "Completato", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Information)
        } else {
            [System.Windows.Forms.MessageBox]::Show("Nessun elemento selezionato.", "Attenzione", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Warning)
        }
    }
})

# Mostra la finestra
[void]$form.ShowDialog()
