# <img src="assets/icon.png" width="48" height="48" align="top" style="margin-right: 10px;"> MCP Creator Growth [Visit Website](https://github.com/SunflowersLwtech/mcp_creator_growth)

[English](README.md) | [简体中文](README_zh-CN.md) | [繁體中文](README_zh-TW.md)

A context-aware **Model Context Protocol (MCP)** server that acts as a learning sidecar for AI coding assistants. It helps developers **learn from AI-generated code changes** through interactive quizzes and provides agents with a persistent **project-specific debugging memory**.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MCP Standard](https://img.shields.io/badge/MCP-Standard-green.svg)](https://modelcontextprotocol.io/)

## 🚀 Why Use This?

1.  **For Developers (Learning)**: Don't just accept AI code—understand it. When you ask "Quiz me on this change," this server creates an interactive learning card to verify your grasp of the logic, security, or performance implications.
2.  **For Agents (Memory)**: Stop solving the same bug twice. The server quietly records debugging solutions in the background and retrieves them automatically when similar errors occur in the future.

## ✨ Features

### 🧠 Interactive Learning Session
- **Tool**: `learning_session`
- **Behavior**: Pauses the agent and opens a local Web UI with a quiz based on recent code changes.
- **Trigger**: Explicit user request (e.g., "Teach me about this fix", "Quiz me").
- **Benefit**: Ensures you understand *why* a change was made before moving on.

![WebUI Preview](assets/webui.png)

### 🐞 Debugging Memory (RAG)
- **Tools**: `debug_search`, `debug_record`
- **Behavior**:
    - **Search**: When an error occurs, the agent silently searches past solutions in your project.
    - **Record**: After fixing a bug, the agent records the cause and solution.
- **Privacy**: All data is stored locally in `.mcp-sidecar/`.
- **Benefit**: Builds a "group memory" for your project that gets smarter over time.

### 📚 Terminology Dictionary
- **Tool**: `term_get`
- **Behavior**: Fetches programming terms and concepts relevant to your current work context.
- **Benefit**: Helps fill knowledge gaps without leaving your IDE.

---

## 🛠️ Quick Start

### One-Line Installation

**macOS / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/SunflowersLwtech/mcp_creator_growth/main/scripts/install.sh | bash
```

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/SunflowersLwtech/mcp_creator_growth/main/scripts/install.ps1 | iex
```

### Manual Installation

Prerequisites: `uv` (recommended) or Python 3.11+.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/SunflowersLwtech/mcp_creator_growth.git
    cd mcp_creator_growth
    ```

2.  **Install dependencies:**
    ```bash
    # Using uv
    uv venv --python 3.11 .venv
    source .venv/bin/activate  # Windows: .venv\Scripts\activate
    uv pip install -e ".[dev]"
    ```

---

## ⚙️ IDE Configuration

Connect your AI coding assistant to the MCP server.

### Claude Desktop / CLI

Add to your `claude_desktop_config.json` (or `~/.claude.json`):

```json
{
  "mcpServers": {
    "mcp-creator-growth": {
      "command": "/absolute/path/to/mcp_creator_growth/.venv/bin/mcp-creator-growth",
      "args": []
    }
  }
}
```
*Note: On Windows, use the full path to `mcp-creator-growth.exe` inside `.venv\Scripts\`.*

### Cursor

1.  Go to **Settings** > **MCP**.
2.  Click **Add New MCP Server**.
3.  **Name**: `mcp-creator-growth`
4.  **Type**: `command`
5.  **Command**: `/absolute/path/to/mcp_creator_growth/.venv/bin/mcp-creator-growth`

### Windsurf

Add to `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "mcp-creator-growth": {
      "command": "/absolute/path/to/mcp_creator_growth/.venv/bin/mcp-creator-growth",
      "args": []
    }
  }
}
```

---

## 🔒 Security & Data

- **Local First**: All learning history and debugging records are stored firmly on your disk in the `.mcp-sidecar/` directory within your project or user home.
- **No Telemetry**: This server does not send your code or quiz performance to any cloud server.
- **Control**: You can delete the `.mcp-sidecar` folder at any time to reset your data.

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1.  Fork the repository.
2.  Create a feature branch: `git checkout -b feature/amazing-feature`.
3.  Install dev dependencies: `uv pip install -e ".[dev]"`.
4.  Make your changes and run tests: `pytest dev/tests/`.
5.  Submit a Pull Request.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">
  Built with <a href="https://github.com/jlowin/fastmcp">FastMCP</a> • 
  <a href="https://modelcontextprotocol.io">MCP Standard</a>
</p>
