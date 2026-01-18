# MCP Creator Growth

A context-aware learning assistant for AI coding that helps developers **learn from AI-generated code changes** through interactive quizzes and debug experience tracking.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

## Why This Tool?

When AI writes code for you, **do you actually learn?** This MCP server creates a **blocking learning session** that:
- Waits until you complete an interactive quiz about the changes
- Tracks your debugging experiences for future reference (RAG-based)
- Helps you build real understanding, not just copy-paste habits

## Features

- **Blocking Learning Sessions** - Agent pauses until you complete the learning card
- **Interactive Quizzes** - Verify your understanding with targeted questions
- **5-Why Reasoning** - Understand the "why" behind code decisions
- **Debug Experience RAG** - Search and record debugging solutions for reuse
- **Token-Efficient** - Designed to minimize unnecessary AI output

## Quick Start

### One-Line Installation

**macOS / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/SunflowersLwtech/mcp_creator_growth/main/scripts/install.sh | bash
```

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/SunflowersLwtech/mcp_creator_growth/main/scripts/install.ps1 | iex
```

The installer will:
1. Auto-detect your environment (uv / conda / system Python)
2. Install Python 3.11+ via uv if needed
3. Create a virtual environment
4. Install all dependencies
5. Display the configuration command for your IDE

### Manual Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SunflowersLwtech/mcp_creator_growth.git
   cd mcp_creator_growth
   ```

2. **Create virtual environment:**
   ```bash
   # Using uv (recommended)
   uv venv --python 3.11 .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   uv pip install -e ".[dev]"

   # Or using standard venv
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -e ".[dev]"
   ```

## IDE Configuration

After installation, configure your AI coding IDE to use this MCP server.

### Claude Code

**Option 1: CLI (Recommended)**
```bash
# macOS / Linux
claude mcp add mcp-creator-growth -- ~/mcp-creator-growth/.venv/bin/mcp-creator-growth

# Windows
claude mcp add mcp-creator-growth -- %USERPROFILE%\mcp-creator-growth\.venv\Scripts\mcp-creator-growth.exe
```

**Option 2: Config File**

Add to `~/.claude.json`:
```json
{
  "mcpServers": {
    "mcp-creator-growth": {
      "command": "~/mcp-creator-growth/.venv/bin/mcp-creator-growth"
    }
  }
}
```

For Windows:
```json
{
  "mcpServers": {
    "mcp-creator-growth": {
      "command": "C:\\Users\\YourName\\mcp-creator-growth\\.venv\\Scripts\\mcp-creator-growth.exe"
    }
  }
}
```

### Cursor

Add to Cursor MCP settings (Settings → MCP → Add Server):

```json
{
  "mcp-creator-growth": {
    "command": "~/mcp-creator-growth/.venv/bin/mcp-creator-growth"
  }
}
```

For Windows:
```json
{
  "mcp-creator-growth": {
    "command": "C:\\Users\\YourName\\mcp-creator-growth\\.venv\\Scripts\\mcp-creator-growth.exe"
  }
}
```

### Windsurf

Add to `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "mcp-creator-growth": {
      "command": "~/mcp-creator-growth/.venv/bin/mcp-creator-growth"
    }
  }
}
```

### Other IDEs

For any MCP-compatible IDE, use these settings:
- **Command:** `<install-path>/.venv/bin/mcp-creator-growth` (or `.venv\Scripts\mcp-creator-growth.exe` on Windows)
- **Transport:** stdio

**After configuration, restart your IDE.**

## Usage

### Available Tools

| Tool | Trigger | Description |
|------|---------|-------------|
| `learning_session` | User explicit request | Creates a blocking learning session with quiz |
| `debug_search` | Automatic | Search historical debug experiences |
| `debug_record` | Automatic | Record new debug solutions |
| `get_system_info` | Automatic | Get system environment info |

### Trigger Learning Session

Say to your AI assistant:
- "Quiz me on this change"
- "Test my understanding"
- "Help me learn about what you did"

The agent will create an interactive learning card and **wait** until you complete it.

### Debug Tools

The debug tools work silently in the background:
- When the AI encounters an error, it searches your past solutions
- When the AI fixes an error, it records the solution for future use

## Updating

**macOS / Linux:**
```bash
~/mcp-creator-growth/scripts/update.sh
```

**Windows:**
```powershell
~\mcp-creator-growth\scripts\update.ps1
```

Then restart your IDE.

## Configuration

Create `~/.config/mcp-sidecar/config.toml` (Unix) or `%APPDATA%/mcp-sidecar/config.toml` (Windows):

```toml
[server]
host = "127.0.0.1"
port = 0  # Auto-select

[storage]
use_global = false  # true = share across projects

[ui]
theme = "auto"  # auto, dark, light
language = "en"  # en, zh-CN

[session]
default_timeout = 600  # 10 minutes
```

## Data Storage

All data is stored locally:

- **Project-level:** `{project}/.mcp-sidecar/` (tracked with git if you want)
- **Global:** `~/.config/mcp-sidecar/` (personal, never tracked)

## Development

```bash
# Run tests
pytest dev/tests/ -v

# Run specific phase
pytest dev/tests/phase1/ -v

# Run with coverage
pytest --cov=src/mcp_creator_growth dev/tests/
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp)
- Inspired by the need for meaningful AI-assisted learning
