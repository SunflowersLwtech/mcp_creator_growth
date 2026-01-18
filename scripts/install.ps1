# MCP Creator Growth - Windows Installation Script
# Usage: .\scripts\install.ps1

param(
    [string]$InstallPath = "$env:USERPROFILE\mcp-creator-growth",
    [switch]$SkipClaudeConfig
)

$ErrorActionPreference = "Stop"

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  MCP Creator Growth - Installation Script" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "[1/5] Checking Python version..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python (\d+)\.(\d+)") {
        $major = [int]$Matches[1]
        $minor = [int]$Matches[2]
        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 11)) {
            Write-Host "Error: Python 3.11+ is required. Found: $pythonVersion" -ForegroundColor Red
            exit 1
        }
        Write-Host "  Found: $pythonVersion" -ForegroundColor Green
    }
} catch {
    Write-Host "Error: Python not found. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Clone or update repository
Write-Host ""
Write-Host "[2/5] Setting up repository..." -ForegroundColor Yellow
if (Test-Path $InstallPath) {
    Write-Host "  Directory exists. Updating..." -ForegroundColor Gray
    Push-Location $InstallPath
    git pull origin main
    Pop-Location
} else {
    Write-Host "  Cloning repository..." -ForegroundColor Gray
    git clone https://github.com/SunflowersLwtech/mcp_creator_growth.git $InstallPath
}

# Create virtual environment
Write-Host ""
Write-Host "[3/5] Creating virtual environment..." -ForegroundColor Yellow
Push-Location $InstallPath
if (-not (Test-Path "venv")) {
    python -m venv venv
    Write-Host "  Virtual environment created." -ForegroundColor Green
} else {
    Write-Host "  Virtual environment already exists." -ForegroundColor Gray
}

# Install dependencies
Write-Host ""
Write-Host "[4/5] Installing dependencies..." -ForegroundColor Yellow
& ".\venv\Scripts\pip.exe" install -e ".[dev]" --quiet
Write-Host "  Dependencies installed." -ForegroundColor Green

# Configure Claude Code
Write-Host ""
Write-Host "[5/5] Configuring Claude Code..." -ForegroundColor Yellow

if (-not $SkipClaudeConfig) {
    $mcpConfig = @{
        mcpServers = @{
            "mcp-creator-growth" = @{
                command = "$InstallPath\venv\Scripts\python.exe"
                args = @("-m", "mcp_creator_growth")
                env = @{
                    MCP_DEBUG = "false"
                }
            }
        }
    }

    $configJson = $mcpConfig | ConvertTo-Json -Depth 4

    Write-Host ""
    Write-Host "  Add the following to your Claude Code MCP settings:" -ForegroundColor Cyan
    Write-Host "  (Settings > MCP Servers > Edit Config)" -ForegroundColor Gray
    Write-Host ""
    Write-Host $configJson -ForegroundColor White
    Write-Host ""

    # Also save to a file for reference
    $configJson | Out-File -FilePath "$InstallPath\claude-mcp-config.json" -Encoding UTF8
    Write-Host "  Config saved to: $InstallPath\claude-mcp-config.json" -ForegroundColor Gray
}

Pop-Location

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "  Installation Complete!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Open Claude Code" -ForegroundColor White
Write-Host "  2. Go to Settings > MCP Servers" -ForegroundColor White
Write-Host "  3. Add the configuration shown above" -ForegroundColor White
Write-Host "  4. Restart Claude Code" -ForegroundColor White
Write-Host ""
Write-Host "To update later, run:" -ForegroundColor Yellow
Write-Host "  .\scripts\update.ps1" -ForegroundColor White
Write-Host ""
