# MCP Creator Growth - Windows Installation Script
# Usage: irm https://raw.githubusercontent.com/SunflowersLwtech/mcp_creator_growth/main/scripts/install.ps1 | iex
# Or: .\scripts\install.ps1
#
# Parameters:
#   -InstallPath - Custom installation path (default: ~/mcp-creator-growth)
#   -UseUV       - Force use uv
#   -UseConda    - Force use conda

param(
    [string]$InstallPath = "$env:USERPROFILE\mcp-creator-growth",
    [switch]$UseUV,
    [switch]$UseConda
)

$ErrorActionPreference = "Stop"
$PythonVersionRequired = "3.11"
$EnvManager = ""
$PythonPath = ""

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  MCP Creator Growth - Installation Script" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Function to check Python version
function Test-PythonVersion {
    param([string]$PythonCmd)
    try {
        $version = & $PythonCmd --version 2>&1
        if ($version -match "Python (\d+)\.(\d+)") {
            $major = [int]$Matches[1]
            $minor = [int]$Matches[2]
            if ($major -ge 3 -and $minor -ge 11) {
                return "$major.$minor"
            }
        }
    } catch {}
    return $null
}

# Function to install uv
function Install-UV {
    Write-Host "  Installing uv..." -ForegroundColor Yellow
    irm https://astral.sh/uv/install.ps1 | iex
    $env:Path = "$env:USERPROFILE\.local\bin;$env:Path"
}

# Step 1: Detect or install environment manager
Write-Host "[1/4] Setting up Python environment..." -ForegroundColor Yellow

if ($UseUV) {
    $EnvManager = "uv"
    if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
        Install-UV
    }
} elseif ($UseConda) {
    $EnvManager = "conda"
    if (-not (Get-Command conda -ErrorAction SilentlyContinue)) {
        Write-Host "Error: -UseConda specified but conda is not installed." -ForegroundColor Red
        Write-Host "Please install Miniconda: https://docs.conda.io/en/latest/miniconda.html" -ForegroundColor Yellow
        exit 1
    }
} else {
    # Auto-detect: prefer uv > conda > system python
    if (Get-Command uv -ErrorAction SilentlyContinue) {
        $EnvManager = "uv"
        Write-Host "  Detected: uv" -ForegroundColor Green
    } elseif (Get-Command conda -ErrorAction SilentlyContinue) {
        $EnvManager = "conda"
        Write-Host "  Detected: conda" -ForegroundColor Green
    } elseif (Get-Command python -ErrorAction SilentlyContinue) {
        $version = Test-PythonVersion "python"
        if ($version) {
            $EnvManager = "venv"
            Write-Host "  Detected: Python $version (using venv)" -ForegroundColor Green
        } else {
            Write-Host "  System Python is too old. Installing uv..." -ForegroundColor Yellow
            Install-UV
            $EnvManager = "uv"
        }
    } else {
        Write-Host "  No Python found. Installing uv..." -ForegroundColor Yellow
        Install-UV
        $EnvManager = "uv"
    }
}

Write-Host "  Using: $EnvManager" -ForegroundColor Cyan

# Step 2: Clone or update repository
Write-Host ""
Write-Host "[2/4] Setting up repository..." -ForegroundColor Yellow
if (Test-Path $InstallPath) {
    Write-Host "  Directory exists. Updating..." -ForegroundColor Gray
    Push-Location $InstallPath
    git pull origin main 2>$null
    Pop-Location
} else {
    Write-Host "  Cloning repository..." -ForegroundColor Gray
    git clone https://github.com/SunflowersLwtech/mcp_creator_growth.git $InstallPath
}

Push-Location $InstallPath

# Step 3: Create virtual environment
Write-Host ""
Write-Host "[3/4] Creating virtual environment..." -ForegroundColor Yellow

switch ($EnvManager) {
    "uv" {
        if (-not (Test-Path ".venv")) {
            uv venv --python $PythonVersionRequired .venv
            Write-Host "  Virtual environment created with Python $PythonVersionRequired" -ForegroundColor Green
        } else {
            Write-Host "  Virtual environment already exists." -ForegroundColor Gray
        }
        $PythonPath = "$InstallPath\.venv\Scripts\python.exe"
    }
    "conda" {
        $envExists = conda env list | Select-String "mcp-creator-growth"
        if (-not $envExists) {
            conda create -n mcp-creator-growth python=$PythonVersionRequired -y
            Write-Host "  Conda environment created." -ForegroundColor Green
        } else {
            Write-Host "  Conda environment already exists." -ForegroundColor Gray
        }
        # Get conda env path
        $condaInfo = conda env list | Select-String "mcp-creator-growth"
        $CondaEnvPath = ($condaInfo -split '\s+')[-1]
        $PythonPath = "$CondaEnvPath\python.exe"
    }
    "venv" {
        if (-not (Test-Path "venv")) {
            python -m venv venv
            Write-Host "  Virtual environment created." -ForegroundColor Green
        } else {
            Write-Host "  Virtual environment already exists." -ForegroundColor Gray
        }
        $PythonPath = "$InstallPath\venv\Scripts\python.exe"
    }
}

# Step 4: Install dependencies
Write-Host ""
Write-Host "[4/4] Installing dependencies..." -ForegroundColor Yellow

switch ($EnvManager) {
    "uv" {
        uv pip install -e ".[dev]" --quiet
    }
    "conda" {
        conda activate mcp-creator-growth
        pip install -e ".[dev]" --quiet
        conda deactivate
    }
    "venv" {
        & ".\venv\Scripts\pip.exe" install -e ".[dev]" --quiet
    }
}

Write-Host "  Dependencies installed." -ForegroundColor Green

# Save environment manager info for update script
$EnvManager | Out-File -FilePath "$InstallPath\.env_manager" -Encoding UTF8 -NoNewline

Pop-Location

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "  Installation Complete!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Environment: $EnvManager" -ForegroundColor Cyan
Write-Host "Python path: $PythonPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Configure Your IDE" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Add this MCP server configuration to your IDE:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Python command: $PythonPath" -ForegroundColor White
Write-Host "  Arguments:      -m mcp_creator_growth" -ForegroundColor White
Write-Host ""
Write-Host "For Claude Code:" -ForegroundColor Yellow
Write-Host "  claude mcp add mcp-creator-growth -- `"$PythonPath`" -m mcp_creator_growth" -ForegroundColor White
Write-Host ""
Write-Host "For other IDEs (Cursor, Windsurf, etc.):" -ForegroundColor Yellow
Write-Host "  See README.md for detailed configuration instructions." -ForegroundColor White
Write-Host ""
Write-Host "To update later, run:" -ForegroundColor Yellow
Write-Host "  $InstallPath\scripts\update.ps1" -ForegroundColor White
Write-Host ""
