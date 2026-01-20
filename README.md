# <img src="assets/icon.png" width="48" height="48" align="top" style="margin-right: 10px;"> MCP Creator Growth

[English](README.md) | [简体中文](README_zh-CN.md) | [繁體中文](README_zh-TW.md)

A context-aware **Model Context Protocol (MCP)** server that acts as a learning sidecar for AI coding assistants. It helps developers **learn from AI-generated code changes** through interactive quizzes and provides agents with a persistent **project-specific debugging memory**.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MCP Standard](https://img.shields.io/badge/MCP-Standard-green.svg)](https://modelcontextprotocol.io/)
[![Glama MCP](https://img.shields.io/badge/Glama-MCP%20Server-blue)](https://glama.ai/mcp/servers/@SunflowersLwtech/mcp_creator_growth)
[![DeepWiki](https://img.shields.io/badge/DeepWiki-Documentation-purple)](https://deepwiki.com/SunflowersLwtech/mcp_creator_growth)

---

## 🌐 Resources

| Resource | Description |
|----------|-------------|
| [**Glama MCP Marketplace**](https://glama.ai/mcp/servers/@SunflowersLwtech/mcp_creator_growth) | Official MCP server listing with installation guides |
| [**DeepWiki Documentation**](https://deepwiki.com/SunflowersLwtech/mcp_creator_growth) | AI-generated deep analysis of the codebase |
| [**GitHub Repository**](https://github.com/SunflowersLwtech/mcp_creator_growth) | Source code, issues, and contributions |

---

## 🚀 Why Use This?

| For | Benefit |
|-----|---------|
| **Developers** | Don't just accept AI code—understand it. Request a quiz to verify your grasp of the logic, security, or performance implications. |
| **AI Agents** | Stop solving the same bug twice. The server quietly records debugging solutions and retrieves them automatically when similar errors occur. |

---

## 📦 Available Tools

| Tool | Type | Description |
|------|------|-------------|
| `learning_session` | 🎓 Interactive | Opens a WebUI quiz based on recent code changes. **Blocks** until user completes learning. |
| `debug_search` | 🔍 Silent RAG | Searches project debug history for relevant past solutions. Auto-triggered on errors. |
| `debug_record` | 📝 Silent | Records debugging experiences to project knowledge base. Auto-triggered after fixes. |
| `term_get` | 📚 Reference | Fetches programming terms/concepts. Tracks shown terms to avoid repetition. |
| `get_system_info` | ℹ️ Utility | Returns system environment information (platform, Python version, etc.). |

### Tool Details

<details>
<summary><b>🎓 learning_session</b> - Interactive Learning Card</summary>

**Trigger**: User explicitly requests (e.g., "Quiz me", "Test my understanding")

**Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `project_directory` | string | `"."` | Project directory path |
| `summary` | string | — | Structured summary of Agent's actions |
| `reasoning` | object | null | 5-Why reasoning (goal, trigger, mechanism, alternatives, risks) |
| `quizzes` | array | auto-generated | 3 quiz questions with options, answer, explanation |
| `focus_areas` | array | `["logic"]` | Focus areas: logic, security, performance, architecture, syntax |
| `timeout` | int | 600 | Timeout in seconds (60-7200) |

**Returns**: `{"status": "completed", "action": "HALT_GENERATION"}`

</details>

<details>
<summary><b>🔍 debug_search</b> - Search Debug History</summary>

**Trigger**: Auto-called when encountering errors (silent, no UI)

**Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | string | — | Error message or description to search |
| `project_directory` | string | `"."` | Project directory path |
| `error_type` | string | null | Filter by error type (e.g., ImportError) |
| `tags` | array | null | Filter by tags |
| `limit` | int | 5 | Maximum results (1-20) |

**Returns**: `{"results": [...], "count": N}`

</details>

<details>
<summary><b>📝 debug_record</b> - Record Debug Experience</summary>

**Trigger**: Auto-called after fixing bugs (silent, background)

**Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `context` | object | — | Error context: `{error_type, error_message, file, line}` |
| `cause` | string | — | Root cause analysis |
| `solution` | string | — | Solution that worked |
| `project_directory` | string | `"."` | Project directory path |
| `tags` | array | null | Tags for categorization |

**Returns**: `{"ok": true, "id": "..."}`

</details>

<details>
<summary><b>📚 term_get</b> - Get Programming Terms</summary>

**Available Domains**: programming_basics, data_structures, algorithms, software_design, web_development, version_control, testing, security, databases, devops

**Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `project_directory` | string | `"."` | Project directory path |
| `count` | int | 3 | Number of terms (1-5) |
| `domain` | string | null | Filter by domain |

**Returns**: `{"terms": [...], "count": N, "remaining": N}`

</details>

---

## 🛠️ Installation

### One-Line Install (Recommended)

<table>
<tr>
<th>Platform</th>
<th>Command</th>
</tr>
<tr>
<td><b>macOS / Linux</b></td>
<td>

```bash
curl -fsSL https://raw.githubusercontent.com/SunflowersLwtech/mcp_creator_growth/main/scripts/install.sh | bash
```

</td>
</tr>
<tr>
<td><b>Windows (PowerShell)</b></td>
<td>

```powershell
irm https://raw.githubusercontent.com/SunflowersLwtech/mcp_creator_growth/main/scripts/install.ps1 | iex
```

</td>
</tr>
</table>

The installer will:
1. Auto-detect your Python environment (uv → conda → venv)
2. Clone the repository to `~/mcp-creator-growth`
3. Create virtual environment and install dependencies
4. Print the exact command to configure your IDE

### Manual Installation

<details>
<summary>Click to expand manual installation steps</summary>

**Prerequisites**: Python 3.11+ or [uv](https://docs.astral.sh/uv/)

```bash
# 1. Clone the repository
git clone https://github.com/SunflowersLwtech/mcp_creator_growth.git
cd mcp_creator_growth

# 2. Create virtual environment and install
# Using uv (recommended)
uv venv --python 3.11 .venv
source .venv/bin/activate          # macOS/Linux
# .venv\Scripts\activate           # Windows
uv pip install -e '.[dev]'

# Or using standard venv
python -m venv venv
source venv/bin/activate           # macOS/Linux
# venv\Scripts\activate            # Windows
pip install -e '.[dev]'
```

</details>

---

## ⚙️ IDE Configuration

### Claude Code (CLI) — One Command Setup

After installation, configure Claude Code with a single command:

<table>
<tr>
<th>Platform</th>
<th>Command</th>
</tr>
<tr>
<td><b>macOS / Linux</b></td>
<td>

```bash
# User scope (available across all projects)
claude mcp add --scope user mcp-creator-growth -- ~/mcp-creator-growth/.venv/bin/mcp-creator-growth

# Or project scope (shared with team via .mcp.json)
claude mcp add --scope project mcp-creator-growth -- ~/mcp-creator-growth/.venv/bin/mcp-creator-growth
```

</td>
</tr>
<tr>
<td><b>Windows (PowerShell)</b></td>
<td>

```powershell
# User scope
claude mcp add --scope user mcp-creator-growth -- "$env:USERPROFILE\mcp-creator-growth\.venv\Scripts\mcp-creator-growth.exe"

# Or project scope
claude mcp add --scope project mcp-creator-growth -- "$env:USERPROFILE\mcp-creator-growth\.venv\Scripts\mcp-creator-growth.exe"
```

</td>
</tr>
</table>

**Verify installation:**
```bash
claude mcp list                    # List all MCP servers
claude mcp get mcp-creator-growth  # Check this server's status
```

### Manual JSON Configuration

For Claude Desktop, Cursor, Windsurf, or other MCP-compatible IDEs:

<table>
<tr>
<th>IDE</th>
<th>Config File Location</th>
</tr>
<tr>
<td>Claude Desktop</td>
<td>

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

</td>
</tr>
<tr>
<td>Claude Code (User)</td>
<td><code>~/.claude.json</code></td>
</tr>
<tr>
<td>Claude Code (Project)</td>
<td><code>.mcp.json</code> in project root</td>
</tr>
<tr>
<td>Cursor</td>
<td>Settings → MCP → Add New MCP Server</td>
</tr>
<tr>
<td>Windsurf</td>
<td><code>~/.codeium/windsurf/mcp_config.json</code></td>
</tr>
</table>

**JSON Configuration:**

<details>
<summary><b>macOS / Linux</b></summary>

```json
{
  "mcpServers": {
    "mcp-creator-growth": {
      "command": "/Users/YOUR_USERNAME/mcp-creator-growth/.venv/bin/mcp-creator-growth",
      "args": []
    }
  }
}
```

</details>

<details>
<summary><b>Windows</b></summary>

```json
{
  "mcpServers": {
    "mcp-creator-growth": {
      "command": "C:\\Users\\YOUR_USERNAME\\mcp-creator-growth\\.venv\\Scripts\\mcp-creator-growth.exe",
      "args": []
    }
  }
}
```

</details>

> **Note**: Replace `YOUR_USERNAME` with your actual username, or use the full path printed by the installer.

---

## 🔄 Updating

### One-Line Update (Recommended)

If you installed using the one-line installer, update is just as easy:

<table>
<tr>
<th>Platform</th>
<th>Command</th>
</tr>
<tr>
<td><b>macOS / Linux</b></td>
<td>

```bash
~/mcp-creator-growth/scripts/update.sh
```

</td>
</tr>
<tr>
<td><b>Windows (PowerShell)</b></td>
<td>

```powershell
~\mcp-creator-growth\scripts\update.ps1
```

</td>
</tr>
</table>

The update script will:
1. Pull the latest changes from the repository
2. Upgrade all dependencies to their latest versions
3. Restart any affected MCP server instances

### Manual Update

<details>
<summary>Click to expand manual update steps</summary>

```bash
# Navigate to installation directory
cd ~/mcp-creator-growth  # or your custom installation path

# Pull latest changes
git pull origin main

# Update dependencies
# Using uv
source .venv/bin/activate          # macOS/Linux
# .venv\Scripts\activate           # Windows
uv pip install -e '.[dev]' --upgrade

# Or using standard venv
source venv/bin/activate           # macOS/Linux
# venv\Scripts\activate            # Windows
pip install -e '.[dev]' --upgrade
```

</details>

---

## 🔧 Troubleshooting

Having issues with installation or configuration? Check out our comprehensive troubleshooting guide:

📖 **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**

Common issues covered:
- Git pull "errors" during installation (not actually errors!)
- "MCP server already exists" message
- PowerShell environment variable syntax (`$env:USERPROFILE` vs `%USERPROFILE%`)
- MCP server not starting
- Python version issues
- Configuration file locations

---

## 🖼️ Screenshots

### Learning Session WebUI

![WebUI Preview](assets/webui.png)

---

## 🔒 Security & Privacy

| Aspect | Details |
|--------|---------|
| **Local First** | All data stored in `.mcp-sidecar/` directory within your project |
| **No Telemetry** | Zero data sent to external servers |
| **Full Control** | Delete `.mcp-sidecar/` anytime to reset all data |

---

## 🔧 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_DEBUG` | `false` | Enable debug logging (`true`, `1`, `yes`, `on`) |
| `MCP_TIMEOUT` | `120000` | MCP server startup timeout in ms |
| `MAX_MCP_OUTPUT_TOKENS` | `25000` | Maximum tokens for MCP output |

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Install dev dependencies: `uv pip install -e '.[dev]'`
4. Make changes and run tests: `pytest`
5. Submit a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📬 Contact

| Channel | Address |
|---------|---------|
| **Email** | sunflowers0607@outlook.com |
| **Email** | weiliu0607@gmail.com |
| **GitHub Issues** | [Open an Issue](https://github.com/SunflowersLwtech/mcp_creator_growth/issues) |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">
  Built with <a href="https://github.com/jlowin/fastmcp">FastMCP</a> •
  <a href="https://modelcontextprotocol.io">MCP Standard</a> •
  <a href="https://glama.ai/mcp/servers/@SunflowersLwtech/mcp_creator_growth">Glama MCP</a>
</p>
