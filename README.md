# <img src="assets/icon.png" width="48" height="48" align="top" style="margin-right: 10px;"> MCP Creator Growth [Visit Website](https://github.com/SunflowersLwtech/mcp_creator_growth)

[English](README.md) | [简体中文](README_zh-CN.md) | [繁體中文](README_zh-TW.md)

A context-aware learning assistant for AI coding that helps developers **learn from AI-generated code changes** through interactive quizzes and debug experience tracking.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

## Design Philosophy

> **Learning is for the User. Debug is for the Agent.**

This project follows two core principles:

| Component | Purpose | Beneficiary |
|-----------|---------|-------------|
| `learning_session` | Help users understand AI-generated changes | **User** |
| `debug_search/record` | Build project-specific knowledge base | **Agent** |

### Low Intrusion, High Value

- **Minimal context pollution**: Return values are deliberately compact to reduce token usage
- **Progressive disclosure**: Debug search returns summaries first, not full records
- **Inverted index**: Fast keyword-based lookups without loading all records
- **Local-first**: All data stored in `.mcp-sidecar/` - your data stays yours

## Features

- **Blocking Learning Sessions** - Agent pauses until you complete the learning card
- **Interactive Quizzes** - Verify your understanding with targeted questions
- **5-Why Reasoning** - Understand the "why" behind code decisions
- **Debug Experience RAG** - Search and record debugging solutions for reuse
- **Token-Efficient** - Returns minimal data to reduce context pollution
- **Optimized Indexing** - Inverted index for fast keyword searches

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

**Option 1: Use the command from install script (Recommended)**

The install script outputs the exact command for your environment. Copy and run it directly:

```
For Claude Code (one command):
  claude mcp add mcp-creator-growth -- "<your-actual-path>"
```

**Option 2: Find the path manually**

If you didn't save the install output, find your executable path:

| Install Method | Executable Path |
|---------------|-----------------|
| uv (default) | `~/mcp-creator-growth/.venv/bin/mcp-creator-growth` (Unix) or `.venv\Scripts\mcp-creator-growth.exe` (Windows) |
| conda | `<conda-path>/envs/mcp-creator-growth/bin/mcp-creator-growth` (Unix) or `Scripts\mcp-creator-growth.exe` (Windows) |
| venv | `~/mcp-creator-growth/venv/bin/mcp-creator-growth` (Unix) or `venv\Scripts\mcp-creator-growth.exe` (Windows) |

Then run:
```bash
claude mcp add mcp-creator-growth -- "<your-executable-path>"
```

**Option 3: Config File**

Add to `~/.claude.json` (replace `<path>` with your actual executable path):
```json
{
  "mcpServers": {
    "mcp-creator-growth": {
      "command": "<path-to-mcp-creator-growth-executable>"
    }
  }
}
```

Example paths:
- Unix (uv): `~/mcp-creator-growth/.venv/bin/mcp-creator-growth`
- Windows (uv): `C:\\Users\\YourName\\mcp-creator-growth\\.venv\\Scripts\\mcp-creator-growth.exe`
- Windows (conda): `C:\\Users\\YourName\\anaconda3\\envs\\mcp-creator-growth\\Scripts\\mcp-creator-growth.exe`

### Cursor

Add to Cursor MCP settings (Settings → MCP → Add Server):

```json
{
  "mcp-creator-growth": {
    "command": "<path-to-mcp-creator-growth-executable>"
  }
}
```

### Windsurf

Add to `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "mcp-creator-growth": {
      "command": "<path-to-mcp-creator-growth-executable>"
    }
  }
}
```

### Other IDEs

For any MCP-compatible IDE, use these settings:
- **Command:** Use the executable path from the install script output (see table above)
- **Transport:** stdio

**After configuration, restart your IDE.**

## Usage

### Available Tools

| Tool | Trigger | For | Returns |
|------|---------|-----|---------|
| `learning_session` | User explicit request | **User** | `{status, action}` - minimal |
| `debug_search` | Automatic (on error) | **Agent** | Compact summaries |
| `debug_record` | Automatic (after fix) | **Agent** | `{ok, id}` - minimal |

### For Users: Learning Session

Say to your AI assistant:
- "Quiz me on this change"
- "Test my understanding"
- "Help me learn about what you did"

The agent will create an interactive learning card and **wait** until you complete it.

> **Note**: Quiz scores are saved locally for your self-tracking but are NOT returned to the agent - this keeps the context clean.

### For Agents: Debug Tools

The debug tools work silently in the background:
- **Search first**: When encountering errors, agent searches past solutions
- **Record after**: When fixing errors, agent records the solution
- **Progressive disclosure**: Returns compact summaries, not full records
- **Fast lookups**: Uses inverted index for keyword-based searches

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

All data is stored locally in `.mcp-sidecar/`:

```
.mcp-sidecar/
├── meta.json              # Project metadata
├── debug/
│   ├── index.json         # Optimized index with inverted lookups
│   └── *.json             # Individual debug records
├── sessions/
│   └── *.json             # Learning session history
└── terms/
    └── shown.json         # Shown terms tracking
```

**Storage locations:**
- **Project-level:** `{project}/.mcp-sidecar/` (tracked with git if you want)
- **Global:** `~/.config/mcp-sidecar/` (personal, never tracked)

**Index optimization:**
- Inverted index for keywords, tags, and error types
- Compact record entries to reduce file size
- Lazy loading - only fetches full records when needed

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
