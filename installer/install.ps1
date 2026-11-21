# rdr2-modmenu installer — drops the exe + script hook into the RDR2 folder.
param(
    [string]$Rdr2Path = "C:\Program Files\Rockstar Games\Red Dead Redemption 2",
    [string]$BuildDir = "..\dist"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path "$Rdr2Path\RDR2.exe")) {
    throw "RDR2.exe not found under $Rdr2Path. Pass -Rdr2Path explicitly."
}

$exe = Join-Path $BuildDir "rdr2-modmenu.exe"
if (-not (Test-Path $exe)) { throw "Build first: python scripts\build_exe.py" }

Copy-Item $exe -Destination $Rdr2Path -Force
Copy-Item "..\src\rdr2_modmenu\script_hook\menu_hook.lua" -Destination "$Rdr2Path\scripts" -Force

Write-Host "Installed rdr2-modmenu to $Rdr2Path" -ForegroundColor Green
Write-Host "Launch RDR2, press F5 in-game to open the menu." -ForegroundColor Yellow