#!/bin/bash
# MCP Creator Growth - Unix Installation Script
# Usage: curl -fsSL https://raw.githubusercontent.com/SunflowersLwtech/mcp_creator_growth/main/scripts/install.sh | bash

set -e

INSTALL_PATH="${MCP_INSTALL_PATH:-$HOME/mcp-creator-growth}"

echo "================================================"
echo "  MCP Creator Growth - Installation Script"
echo "================================================"
echo ""

# Check Python version
echo "[1/5] Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | sed -n 's/Python \([0-9]*\.[0-9]*\).*/\1/p')
    MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

    if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 11 ]); then
        echo "Error: Python 3.11+ is required. Found: Python $PYTHON_VERSION"
        exit 1
    fi
    echo "  Found: Python $PYTHON_VERSION"
else
    echo "Error: Python not found. Please install Python 3.11+"
    exit 1
fi

# Clone or update repository
echo ""
echo "[2/5] Setting up repository..."
if [ -d "$INSTALL_PATH" ]; then
    echo "  Directory exists. Updating..."
    cd "$INSTALL_PATH"
    git pull origin main
else
    echo "  Cloning repository..."
    git clone https://github.com/SunflowersLwtech/mcp_creator_growth.git "$INSTALL_PATH"
    cd "$INSTALL_PATH"
fi

# Create virtual environment
echo ""
echo "[3/5] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "  Virtual environment created."
else
    echo "  Virtual environment already exists."
fi

# Install dependencies
echo ""
echo "[4/5] Installing dependencies..."
./venv/bin/pip install -e ".[dev]" --quiet
echo "  Dependencies installed."

# Configure Claude Code
echo ""
echo "[5/5] Configuring Claude Code..."

PYTHON_PATH="$INSTALL_PATH/venv/bin/python"

cat << EOF

  Add the following to your Claude Code MCP settings:
  (Settings > MCP Servers > Edit Config)

{
  "mcpServers": {
    "mcp-creator-growth": {
      "command": "$PYTHON_PATH",
      "args": ["-m", "mcp_creator_growth"],
      "env": {
        "MCP_DEBUG": "false"
      }
    }
  }
}

EOF

# Save config to file
cat > "$INSTALL_PATH/claude-mcp-config.json" << EOF
{
  "mcpServers": {
    "mcp-creator-growth": {
      "command": "$PYTHON_PATH",
      "args": ["-m", "mcp_creator_growth"],
      "env": {
        "MCP_DEBUG": "false"
      }
    }
  }
}
EOF

echo "  Config saved to: $INSTALL_PATH/claude-mcp-config.json"

echo ""
echo "================================================"
echo "  Installation Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "  1. Open Claude Code"
echo "  2. Go to Settings > MCP Servers"
echo "  3. Add the configuration shown above"
echo "  4. Restart Claude Code"
echo ""
echo "To update later, run:"
echo "  $INSTALL_PATH/scripts/update.sh"
echo ""
