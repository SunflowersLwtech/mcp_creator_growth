# MCP Creator Growth - Windows Update Script
# Usage: .\scripts\update.ps1

param(
    [string]$InstallPath = $PSScriptRoot.Replace("\scripts", ""),
    [switch]$Force
)

$ErrorActionPreference = "Stop"

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  MCP Creator Growth - Update Script" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

Push-Location $InstallPath

# Function to check if exe is locked
function Test-FileLocked {
    param([string]$Path)
    if (-not (Test-Path $Path)) { return $false }
    try {
        $file = [System.IO.File]::Open($Path, 'Open', 'Write')
        $file.Close()
        return $false
    } catch {
        return $true
    }
}

# Function to find and display processes using the exe
function Get-LockingProcesses {
    param([string]$ExePath)
    $processes = @()
    try {
        $handle = Get-Process | Where-Object {
            $_.Path -eq $ExePath -or $_.MainModule.FileName -eq $ExePath
        } -ErrorAction SilentlyContinue
        if ($handle) { $processes += $handle }
    } catch {}
    return $processes
}

# Read environment manager from saved file
if (Test-Path ".env_manager") {
    $EnvManager = Get-Content ".env_manager" -Raw
    $EnvManager = $EnvManager.Trim()
} else {
    # Fallback: detect from existing environment
    if (Test-Path ".venv") {
        $EnvManager = "uv"
    } elseif ((conda env list 2>$null | Select-String "mcp-creator-growth")) {
        $EnvManager = "conda"
    } elseif (Test-Path "venv") {
        $EnvManager = "venv"
    } else {
        Write-Host "Error: Cannot detect environment manager." -ForegroundColor Red
        Write-Host "Please run install.ps1 again." -ForegroundColor Yellow
        Pop-Location
        exit 1
    }
}

Write-Host "Environment: $EnvManager" -ForegroundColor Cyan

# Get current version
$currentVersion = "unknown"
try {
    $initFile = Get-Content "src\mcp_creator_growth\__init__.py" -Raw
    if ($initFile -match '__version__\s*=\s*"([^"]+)"') {
        $currentVersion = $Matches[1]
    }
} catch {}

Write-Host "Current version: $currentVersion" -ForegroundColor Gray
Write-Host ""

# Pull latest changes
Write-Host "[1/3] Pulling latest changes..." -ForegroundColor Yellow
git fetch origin main
$localCommit = git rev-parse HEAD
$remoteCommit = git rev-parse origin/main

if ($localCommit -eq $remoteCommit) {
    Write-Host "  Already up to date!" -ForegroundColor Green
    Pop-Location
    exit 0
}

# Get script hash before update
$scriptPath = $PSCommandPath
$hashBefore = (Get-FileHash $scriptPath -Algorithm MD5).Hash

# Reset any local changes (safe for installed copy)
git reset --hard origin/main
Write-Host "  Changes pulled." -ForegroundColor Green

# Check if the update script itself was updated
$hashAfter = (Get-FileHash $scriptPath -Algorithm MD5).Hash
if ($hashBefore -ne $hashAfter) {
    Write-Host ""
    Write-Host "  Update script was updated. Restarting with new version..." -ForegroundColor Cyan
    Write-Host ""
    # Re-invoke with same parameters
    $restartArgs = @("-File", $scriptPath)
    if ($Force) { $restartArgs += "-Force" }
    Start-Process -FilePath "powershell.exe" -ArgumentList $restartArgs -NoNewWindow -Wait
    Pop-Location
    exit 0
}

# Update dependencies
Write-Host ""
Write-Host "[2/3] Updating dependencies..." -ForegroundColor Yellow

# Determine exe path based on environment
$ExePath = switch ($EnvManager) {
    "uv" { "$InstallPath\.venv\Scripts\mcp-creator-growth.exe" }
    "conda" {
        $condaInfo = conda env list | Select-String "mcp-creator-growth"
        if ($condaInfo) {
            $CondaEnvPath = ($condaInfo -split '\s+')[-1]
            "$CondaEnvPath\Scripts\mcp-creator-growth.exe"
        } else { $null }
    }
    "venv" { "$InstallPath\venv\Scripts\mcp-creator-growth.exe" }
}

# Check if exe is locked (in use by an AI coding assistant or IDE)
if ($ExePath -and (Test-FileLocked $ExePath)) {
    Write-Host ""
    Write-Host "  WARNING: mcp-creator-growth.exe is currently in use!" -ForegroundColor Yellow
    Write-Host "  An AI coding assistant or IDE is likely using this MCP server." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  To update successfully, please:" -ForegroundColor Cyan
    Write-Host "    1. Close any AI coding assistant using this MCP server" -ForegroundColor White
    Write-Host "       (e.g., Claude Code, Cursor, Windsurf, VS Code, etc.)" -ForegroundColor Gray
    Write-Host "    2. Run this update script again" -ForegroundColor White
    Write-Host ""

    if (-not $Force) {
        Write-Host "  Or use -Force to skip dependency update (code changes only):" -ForegroundColor Gray
        Write-Host "    .\scripts\update.ps1 -Force" -ForegroundColor Gray
        Write-Host ""
        Pop-Location
        exit 1
    } else {
        Write-Host "  -Force flag detected, skipping dependency update..." -ForegroundColor Yellow
    }
} else {
    # Safe to update
    switch ($EnvManager) {
        "uv" {
            uv pip install -e '.[dev]' --quiet --upgrade
        }
        "conda" {
            conda activate mcp-creator-growth
            pip install -e '.[dev]' --quiet --upgrade
            conda deactivate
        }
        "venv" {
            & ".\venv\Scripts\pip.exe" install -e '.[dev]' --quiet --upgrade
        }
    }
    Write-Host "  Dependencies updated." -ForegroundColor Green
}

# Get new version
$newVersion = "unknown"
try {
    $initFile = Get-Content "src\mcp_creator_growth\__init__.py" -Raw
    if ($initFile -match '__version__\s*=\s*"([^"]+)"') {
        $newVersion = $Matches[1]
    }
} catch {}

Write-Host ""
Write-Host "[3/3] Checking version..." -ForegroundColor Yellow
Write-Host "  Updated: $currentVersion -> $newVersion" -ForegroundColor Green

Pop-Location

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "  Update Complete!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Please restart your AI coding assistant to apply changes." -ForegroundColor Yellow
Write-Host "(e.g., Claude Code, Cursor, Windsurf, VS Code, etc.)" -ForegroundColor Gray
Write-Host ""
