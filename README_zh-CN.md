# <img src="assets/icon.png" width="48" height="48" align="top" style="margin-right: 10px;"> MCP Creator Growth [访问官网](https://github.com/SunflowersLwtech/mcp_creator_growth)

[English](README.md) | [简体中文](README_zh-CN.md) | [繁體中文](README_zh-TW.md)

一个具备上下文感知能力的 **Model Context Protocol (MCP)** 服务器，作为 AI 编程助手的“学习侧边栏”。它通过互动测验帮助开发者**从 AI 生成的代码变更中学习**，并为智能体提供持久化的**项目级调试记忆**。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MCP Standard](https://img.shields.io/badge/MCP-Standard-green.svg)](https://modelcontextprotocol.io/)

## 🚀 为什么使用它？

1.  **对于开发者（学习）**：不要只接受 AI 的代码——要理解它。当你问“针对这个变更考考我”时，本服务器会创建一个互动学习卡片，验证你对逻辑、安全性或性能影响的理解。
2.  **对于智能体（记忆）**：不再重复解决同一个 Bug。服务器会在后台静默记录调试解决方案，并在未来遇到类似错误时自动检索它们。

## ✨ 功能特性

### 🧠 互动学习会话
- **工具**: `learning_session`
- **行为**: 暂停 Agent 并打开本地 Web UI，根据最近的代码变更生成测验。
- **触发**: 用户显式请求（例如：“教我这个修复”，“考考我”）。
- **收益**: 确保你在继续之前理解*为什么*要做这个变更。

![WebUI 预览](assets/webui-CN.png)

### 🐞 调试记忆 (RAG)
- **工具**: `debug_search`, `debug_record`
- **行为**:
    - **搜索**: 当错误发生时，Agent 静默搜索你项目中的过往解决方案。
    - **记录**: 修复 Bug 后，Agent 记录原因和解决方案。
- **隐私**: 所有数据均存储在本地 `.mcp-sidecar/` 中。
- **收益**: 为你的项目构建“群体记忆”，让它随着时间推移变得更聪明。

### 📚 术语字典
- **工具**: `term_get`
- **行为**: 获取与你当前工作上下文相关的编程术语和概念。
- **收益**: 帮助你在不离开 IDE 的情况下填补知识空白。

---

## 🛠️ 快速开始

### 一键安装

**macOS / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/SunflowersLwtech/mcp_creator_growth/main/scripts/install.sh | bash
```

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/SunflowersLwtech/mcp_creator_growth/main/scripts/install.ps1 | iex
```

### 手动安装

先决条件：`uv` (推荐) 或 Python 3.11+。

1.  **克隆仓库：**
    ```bash
    git clone https://github.com/SunflowersLwtech/mcp_creator_growth.git
    cd mcp_creator_growth
    ```

2.  **安装依赖：**
    ```bash
    # 使用 uv
    uv venv --python 3.11 .venv
    source .venv/bin/activate  # Windows: .venv\Scripts\activate
    uv pip install -e ".[dev]"
    ```

---

## ⚙️ IDE 配置

将你的 AI 编程助手连接到 MCP 服务器。

### Claude Desktop / CLI

添加到你的 `claude_desktop_config.json` (或 `~/.claude.json`)：

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
*注意：在 Windows 上，使用 `.venv\Scripts\` 内 `mcp-creator-growth.exe` 的完整路径。*

### Cursor

1.  进入 **Settings** > **MCP**。
2.  点击 **Add New MCP Server**。
3.  **Name**: `mcp-creator-growth`
4.  **Type**: `command`
5.  **Command**: `/absolute/path/to/mcp_creator_growth/.venv/bin/mcp-creator-growth`

### Windsurf

添加到 `~/.codeium/windsurf/mcp_config.json`：

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

## 🔒 安全与数据

- **本地优先**: 所有学习历史和调试记录都牢固地存储在你磁盘上的 `.mcp-sidecar/` 目录中（位于项目或用户主目录下）。
- **无遥测**: 本服务器不会将你的代码或测验表现发送到任何云服务器。
- **掌控权**: 你可以随时删除 `.mcp-sidecar` 文件夹来重置你的数据。

## 🤝 贡献

我们欢迎贡献！请遵循以下步骤：

1.  Fork 本仓库。
2.  创建特性分支：`git checkout -b feature/amazing-feature`。
3.  安装开发依赖：`uv pip install -e ".[dev]"`。
4.  进行更改并运行测试：`pytest dev/tests/`。
5.  提交 Pull Request。

## 📄 许可证

本项目基于 [MIT License](LICENSE) 授权。

---

<p align="center">
  基于 <a href="https://github.com/jlowin/fastmcp">FastMCP</a> 构建 • 
  <a href="https://modelcontextprotocol.io">MCP 标准</a>
</p>
