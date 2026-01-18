#!/bin/bash
# MCP Creator Growth - Unix Update Script
# Usage: ./scripts/update.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_PATH="$(dirname "$SCRIPT_DIR")"

echo "================================================"
echo "  MCP Creator Growth - Update Script"
echo "================================================"
echo ""

cd "$INSTALL_PATH"

# Read environment manager from saved file
if [ -f ".env_manager" ]; then
    ENV_MANAGER=$(cat .env_manager)
else
    # Fallback: detect from existing environment
    if [ -d ".venv" ]; then
        ENV_MANAGER="uv"
    elif conda env list 2>/dev/null | grep -q "mcp-creator-growth"; then
        ENV_MANAGER="conda"
    elif [ -d "venv" ]; then
        ENV_MANAGER="venv"
    else
        echo "Error: Cannot detect environment manager."
        echo "Please run install.sh again."
        exit 1
    fi
fi

echo "Environment: $ENV_MANAGER"

# Get current version
CURRENT_VERSION=$(sed -n 's/^__version__[[:space:]]*=[[:space:]]*"\([^"]*\)".*/\1/p' src/mcp_creator_growth/__init__.py 2>/dev/null || echo "unknown")
echo "Current version: $CURRENT_VERSION"
echo ""

# Pull latest changes
echo "[1/3] Pulling latest changes..."
git fetch origin main
LOCAL_COMMIT=$(git rev-parse HEAD)
REMOTE_COMMIT=$(git rev-parse origin/main)

if [ "$LOCAL_COMMIT" = "$REMOTE_COMMIT" ]; then
    echo "  Already up to date!"
    exit 0
fi

git pull origin main
echo "  Changes pulled."

# Update dependencies
echo ""
echo "[2/3] Updating dependencies..."

case "$ENV_MANAGER" in
    "uv")
        uv pip install -e ".[dev]" --quiet --upgrade
        ;;
    "conda")
        eval "$(conda shell.bash hook)"
        conda activate mcp-creator-growth
        pip install -e ".[dev]" --quiet --upgrade
        conda deactivate
        ;;
    "venv")
        ./venv/bin/pip install -e ".[dev]" --quiet --upgrade
        ;;
esac

echo "  Dependencies updated."

# Get new version
NEW_VERSION=$(sed -n 's/^__version__[[:space:]]*=[[:space:]]*"\([^"]*\)".*/\1/p' src/mcp_creator_growth/__init__.py 2>/dev/null || echo "unknown")

echo ""
echo "[3/3] Checking version..."
echo "  Updated: $CURRENT_VERSION -> $NEW_VERSION"

echo ""
echo "================================================"
echo "  Update Complete!"
echo "================================================"
echo ""
echo "Please restart Claude Code to apply changes."
echo ""
