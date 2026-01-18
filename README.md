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

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/SunflowersLwtech/mcp_creator_growth/main/scripts/install.ps1 | iex
```

**macOS / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/SunflowersLwtech/mcp_creator_growth/main/scripts/install.sh | bash
```

### Manual Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SunflowersLwtech/mcp_creator_growth.git
   cd mcp_creator_growth
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv

   # Windows
   .\venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

## Configure Claude Code

Add the following to your Claude Code MCP settings:

**Windows:**
```json
{
  "mcpServers": {
    "mcp-creator-growth": {
      "command": "C:\\path\\to\\mcp_creator_growth\\venv\\Scripts\\python.exe",
      "args": ["-m", "mcp_creator_growth"],
      "env": {
        "MCP_DEBUG": "false"
      }
    }
  }
}
```

**macOS / Linux:**
```json
{
  "mcpServers": {
    "mcp-creator-growth": {
      "command": "/path/to/mcp_creator_growth/venv/bin/python",
      "args": ["-m", "mcp_creator_growth"],
      "env": {
        "MCP_DEBUG": "false"
      }
    }
  }
}
```

Then restart Claude Code.

## Usage

### Available Tools

| Tool | Trigger | Description |
|------|---------|-------------|
| `learning_session` | User explicit request | Creates a blocking learning session with quiz |
| `debug_search` | Automatic | Search historical debug experiences |
| `debug_record` | Automatic | Record new debug solutions |
| `get_system_info` | Automatic | Get system environment info |

### Trigger Learning Session

Say to Claude:
- "Quiz me on this change"
- "Test my understanding"
- "Help me learn about what you did"

The agent will create an interactive learning card and **wait** until you complete it.

### Debug Tools

The debug tools work silently in the background:
- When Claude encounters an error, it searches your past solutions
- When Claude fixes an error, it records the solution for future use

## Updating

**Windows:**
```powershell
.\scripts\update.ps1
```

**macOS / Linux:**
```bash
./scripts/update.sh
```

Then restart Claude Code.

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
