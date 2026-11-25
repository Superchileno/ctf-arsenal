# Importa writeups locales al repositorio CTF, en modo "solo conocimiento".
#
# Copia documentacion y scripts (nunca artefactos pesados) desde una carpeta de
# retos ya resuelta hacia CTF\<evento>\<reto>\, conservando la estructura.
#
# Uso:
#   .\import_local.ps1 -Source "C:\ruta\ctf" -Event "trama-2026"
#   .\import_local.ps1 -Source "C:\ruta\ANCI" -Event "anci-2026" -DryRun
#
# Despues de importar, sanear antes de publicar:
#   python arsenal\sanitize.py --path CTF\<evento> --check

param(
    [Parameter(Mandatory=$true)][string]$Source,
    [Parameter(Mandatory=$true)][string]$Event,
    [string]$Destino = "",
    [int]$MaxKB = 256,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
if (-not $Destino) { $Destino = Join-Path $root "CTF\$Event" }

if (-not (Test-Path $Source)) { throw "No existe el origen: $Source" }

# Carpetas que nunca se copian (artefactos intermedios, evidencia, backups)
$excluirDirs = @("work", "evidence", "flags", "backups", "node_modules", "__pycache__", ".git")

# Extensiones que sí son conocimiento reutilizable
$extensiones = @(".md", ".py", ".sh", ".ps1", ".txt", ".csv", ".json", ".yml", ".yaml")

$copiados = 0
$omitidos = 0
$bytes = 0

Get-ChildItem -Path $Source -Recurse -File | ForEach-Object {
    $rel = $_.FullName.Substring($Source.Length).TrimStart('\')
    $partes = $rel -split '\\'

    if ($partes | Where-Object { $excluirDirs -contains $_ }) { $omitidos++; return }
    if ($extensiones -notcontains $_.Extension.ToLower()) { $omitidos++; return }
    if ($_.Length -gt ($MaxKB * 1024)) { $omitidos++; return }

    $destinoArchivo = Join-Path $Destino $rel
    if ($DryRun) {
        Write-Output "  [dry] $rel"
    } else {
        $dir = Split-Path -Parent $destinoArchivo
        if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
        Copy-Item $_.FullName $destinoArchivo -Force
    }
    $copiados++
    $bytes += $_.Length
}

Write-Output ""
Write-Output "Origen : $Source"
Write-Output "Destino: $Destino"
Write-Output ("Copiados: {0} archivos ({1:N2} MB) | omitidos: {2}" -f $copiados, ($bytes/1MB), $omitidos)
if ($DryRun) { Write-Output "Modo simulación: no se escribió nada." }
