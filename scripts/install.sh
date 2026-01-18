#!/bin/bash
# MCP Creator Growth - Unix Installation Script
# Usage: curl -fsSL https://raw.githubusercontent.com/SunflowersLwtech/mcp_creator_growth/main/scripts/install.sh | bash
#
# Environment variables:
#   MCP_INSTALL_PATH - Custom installation path (default: ~/mcp-creator-growth)
#   MCP_USE_UV       - Force use uv (set to "1" to enable)
#   MCP_USE_CONDA    - Force use conda (set to "1" to enable)

set -e

INSTALL_PATH="${MCP_INSTALL_PATH:-$HOME/mcp-creator-growth}"
PYTHON_VERSION_REQUIRED="3.11"
ENV_MANAGER=""
PYTHON_PATH=""

echo "================================================"
echo "  MCP Creator Growth - Installation Script"
echo "================================================"
echo ""

# Function to check Python version
check_python_version() {
    local python_cmd="$1"
    local version=$($python_cmd --version 2>&1 | sed -n 's/Python \([0-9]*\.[0-9]*\).*/\1/p')
    local major=$(echo $version | cut -d. -f1)
    local minor=$(echo $version | cut -d. -f2)

    if [ "$major" -ge 3 ] && [ "$minor" -ge 11 ]; then
        echo "$version"
        return 0
    fi
    return 1
}

# Function to install uv if not present
install_uv() {
    echo "  Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
}

# Step 1: Detect or install environment manager
echo "[1/5] Setting up Python environment..."

# Check user preference
if [ "$MCP_USE_UV" = "1" ]; then
    ENV_MANAGER="uv"
    if ! command -v uv &> /dev/null; then
        install_uv
    fi
elif [ "$MCP_USE_CONDA" = "1" ]; then
    ENV_MANAGER="conda"
    if ! command -v conda &> /dev/null; then
        echo "Error: MCP_USE_CONDA=1 but conda is not installed."
        echo "Please install Miniconda: https://docs.conda.io/en/latest/miniconda.html"
        exit 1
    fi
else
    # Auto-detect: prefer uv > conda > system python
    if command -v uv &> /dev/null; then
        ENV_MANAGER="uv"
        echo "  Detected: uv"
    elif command -v conda &> /dev/null; then
        ENV_MANAGER="conda"
        echo "  Detected: conda"
    elif command -v python3 &> /dev/null; then
        if version=$(check_python_version python3); then
            ENV_MANAGER="venv"
            echo "  Detected: Python $version (using venv)"
        else
            # System Python is too old, try to install uv
            echo "  System Python is too old. Installing uv..."
            install_uv
            ENV_MANAGER="uv"
        fi
    else
        # No Python found, install uv
        echo "  No Python found. Installing uv..."
        install_uv
        ENV_MANAGER="uv"
    fi
fi

echo "  Using: $ENV_MANAGER"

# Step 2: Clone or update repository
echo ""
echo "[2/5] Setting up repository..."
if [ -d "$INSTALL_PATH" ]; then
    echo "  Directory exists. Updating..."
    cd "$INSTALL_PATH"
    git pull origin main 2>/dev/null || true
else
    echo "  Cloning repository..."
    git clone https://github.com/SunflowersLwtech/mcp_creator_growth.git "$INSTALL_PATH"
    cd "$INSTALL_PATH"
fi

# Step 3: Create virtual environment
echo ""
echo "[3/5] Creating virtual environment..."

case "$ENV_MANAGER" in
    "uv")
        if [ ! -d ".venv" ]; then
            uv venv --python $PYTHON_VERSION_REQUIRED .venv
            echo "  Virtual environment created with Python $PYTHON_VERSION_REQUIRED"
        else
            echo "  Virtual environment already exists."
        fi
        PYTHON_PATH="$INSTALL_PATH/.venv/bin/python"
        ;;
    "conda")
        if ! conda env list | grep -q "mcp-creator-growth"; then
            conda create -n mcp-creator-growth python=$PYTHON_VERSION_REQUIRED -y
            echo "  Conda environment created."
        else
            echo "  Conda environment already exists."
        fi
        # Get conda env path
        CONDA_ENV_PATH=$(conda env list | grep "mcp-creator-growth" | awk '{print $NF}')
        PYTHON_PATH="$CONDA_ENV_PATH/bin/python"
        ;;
    "venv")
        if [ ! -d "venv" ]; then
            python3 -m venv venv
            echo "  Virtual environment created."
        else
            echo "  Virtual environment already exists."
        fi
        PYTHON_PATH="$INSTALL_PATH/venv/bin/python"
        ;;
esac

# Step 4: Install dependencies
echo ""
echo "[4/5] Installing dependencies..."

case "$ENV_MANAGER" in
    "uv")
        uv pip install -e ".[dev]" --quiet
        ;;
    "conda")
        eval "$(conda shell.bash hook)"
        conda activate mcp-creator-growth
        pip install -e ".[dev]" --quiet
        conda deactivate
        ;;
    "venv")
        ./venv/bin/pip install -e ".[dev]" --quiet
        ;;
esac

echo "  Dependencies installed."

# Step 5: Configure Claude Code
echo ""
echo "[5/5] Configuring Claude Code..."

# Save environment manager info for update script
echo "$ENV_MANAGER" > "$INSTALL_PATH/.env_manager"

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
echo "Environment: $ENV_MANAGER"
echo "Python path: $PYTHON_PATH"
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
