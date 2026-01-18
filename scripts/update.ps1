# MCP Creator Growth - Windows Update Script
# Usage: .\scripts\update.ps1

param(
    [string]$InstallPath = $PSScriptRoot.Replace("\scripts", "")
)

$ErrorActionPreference = "Stop"

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  MCP Creator Growth - Update Script" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

Push-Location $InstallPath

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

# Reset any local changes (safe for installed copy)
git reset --hard origin/main
Write-Host "  Changes pulled." -ForegroundColor Green

# Update dependencies
Write-Host ""
Write-Host "[2/3] Updating dependencies..." -ForegroundColor Yellow

switch ($EnvManager) {
    "uv" {
        uv pip install -e ".[dev]" --quiet --upgrade
    }
    "conda" {
        conda activate mcp-creator-growth
        pip install -e ".[dev]" --quiet --upgrade
        conda deactivate
    }
    "venv" {
        & ".\venv\Scripts\pip.exe" install -e ".[dev]" --quiet --upgrade
    }
}

Write-Host "  Dependencies updated." -ForegroundColor Green

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
Write-Host "Please restart Claude Code to apply changes." -ForegroundColor Yellow
Write-Host ""
