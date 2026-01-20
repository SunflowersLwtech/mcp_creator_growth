# <img src="assets/icon.png" width="48" height="48" align="top" style="margin-right: 10px;"> MCP Creator Growth

[English](README.md) | [简体中文](README_zh-CN.md) | [繁體中文](README_zh-TW.md)

一个具备上下文感知能力的 **Model Context Protocol (MCP)** 服务器，作为 AI 编程助手的「学习侧边栏」。它通过互动测验帮助开发者**从 AI 生成的代码变更中学习**，并为智能体提供持久化的**项目级调试记忆**。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MCP Standard](https://img.shields.io/badge/MCP-Standard-green.svg)](https://modelcontextprotocol.io/)
[![Glama MCP](https://img.shields.io/badge/Glama-MCP%20Server-blue)](https://glama.ai/mcp/servers/@SunflowersLwtech/mcp_creator_growth)
[![DeepWiki](https://img.shields.io/badge/DeepWiki-文档-purple)](https://deepwiki.com/SunflowersLwtech/mcp_creator_growth)

---

## 🌐 资源链接

| 资源 | 描述 |
|------|------|
| [**Glama MCP 市场**](https://glama.ai/mcp/servers/@SunflowersLwtech/mcp_creator_growth) | 官方 MCP 服务器列表，含安装指南 |
| [**DeepWiki 文档**](https://deepwiki.com/SunflowersLwtech/mcp_creator_growth) | AI 生成的代码库深度解析 |
| [**GitHub 仓库**](https://github.com/SunflowersLwtech/mcp_creator_growth) | 源代码、Issue 和贡献 |

---

## 🚀 为什么使用它？

| 角色 | 收益 |
|------|------|
| **开发者** | 不要只接受 AI 的代码——要理解它。请求测验来验证你对逻辑、安全性或性能影响的理解。 |
| **AI 智能体** | 不再重复解决同一个 Bug。服务器会静默记录调试方案，并在遇到类似错误时自动检索。 |

---

## 📦 可用工具

| 工具 | 类型 | 描述 |
|------|------|------|
| `learning_session` | 🎓 互动式 | 打开 WebUI 测验界面，基于最近的代码变更生成题目。**阻塞**直到用户完成学习。 |
| `debug_search` | 🔍 静默 RAG | 搜索项目调试历史，查找相关的历史解决方案。遇到错误时自动触发。 |
| `debug_record` | 📝 静默 | 将调试经验记录到项目知识库。修复 Bug 后自动触发。 |
| `term_get` | 📚 参考 | 获取编程术语和概念。跟踪已展示的术语以避免重复。 |
| `get_system_info` | ℹ️ 工具 | 返回系统环境信息（平台、Python 版本等）。 |

### 工具详情

<details>
<summary><b>🎓 learning_session</b> - 互动学习卡片</summary>

**触发条件**: 用户显式请求（例如：「考考我」、「测试我的理解」）

**参数**:
| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `project_directory` | string | `"."` | 项目目录路径 |
| `summary` | string | — | Agent 操作的结构化摘要 |
| `reasoning` | object | null | 5-Why 推理（目标、触发、机制、替代方案、风险） |
| `quizzes` | array | 自动生成 | 3 道测验题，包含选项、答案、解释 |
| `focus_areas` | array | `["logic"]` | 重点领域：logic、security、performance、architecture、syntax |
| `timeout` | int | 600 | 超时时间（秒，60-7200） |

**返回**: `{"status": "completed", "action": "HALT_GENERATION"}`

</details>

<details>
<summary><b>🔍 debug_search</b> - 搜索调试历史</summary>

**触发条件**: 遇到错误时自动调用（静默，无 UI）

**参数**:
| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `query` | string | — | 要搜索的错误消息或描述 |
| `project_directory` | string | `"."` | 项目目录路径 |
| `error_type` | string | null | 按错误类型过滤（如 ImportError） |
| `tags` | array | null | 按标签过滤 |
| `limit` | int | 5 | 最大结果数（1-20） |

**返回**: `{"results": [...], "count": N}`

</details>

<details>
<summary><b>📝 debug_record</b> - 记录调试经验</summary>

**触发条件**: 修复 Bug 后自动调用（静默，后台运行）

**参数**:
| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `context` | object | — | 错误上下文：`{error_type, error_message, file, line}` |
| `cause` | string | — | 根因分析 |
| `solution` | string | — | 有效的解决方案 |
| `project_directory` | string | `"."` | 项目目录路径 |
| `tags` | array | null | 分类标签 |

**返回**: `{"ok": true, "id": "..."}`

</details>

<details>
<summary><b>📚 term_get</b> - 获取编程术语</summary>

**可用领域**: programming_basics、data_structures、algorithms、software_design、web_development、version_control、testing、security、databases、devops

**参数**:
| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `project_directory` | string | `"."` | 项目目录路径 |
| `count` | int | 3 | 术语数量（1-5） |
| `domain` | string | null | 按领域过滤 |

**返回**: `{"terms": [...], "count": N, "remaining": N}`

</details>

---

## 🛠️ 安装

### 一键安装（推荐）

<table>
<tr>
<th>平台</th>
<th>命令</th>
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

安装脚本会：
1. 自动检测 Python 环境（uv → conda → venv）
2. 克隆仓库到 `~/mcp-creator-growth`
3. 创建虚拟环境并安装依赖
4. 输出配置 IDE 所需的确切命令

### 手动安装

<details>
<summary>点击展开手动安装步骤</summary>

**前置条件**: Python 3.11+ 或 [uv](https://docs.astral.sh/uv/)

```bash
# 1. 克隆仓库
git clone https://github.com/SunflowersLwtech/mcp_creator_growth.git
cd mcp_creator_growth

# 2. 创建虚拟环境并安装
# 使用 uv（推荐）
uv venv --python 3.11 .venv
source .venv/bin/activate          # macOS/Linux
# .venv\Scripts\activate           # Windows
uv pip install -e '.[dev]'

   # 或者使用标准 venv
   python -m venv venv
   source venv/bin/activate  # 或在 Windows 上使用 venv\Scripts\activate
   pip install -e ".[dev]"
   ```

## IDE 配置

安装后，配置你的 AI 编程 IDE 以使用此 MCP 服务器。

### Claude Code

**选项 1：CLI (推荐)**
```bash
# macOS / Linux
claude mcp add mcp-creator-growth -- ~/mcp-creator-growth/.venv/bin/mcp-creator-growth

# Windows
claude mcp add mcp-creator-growth -- %USERPROFILE%\mcp-creator-growth\.venv\Scripts\mcp-creator-growth.exe
```

**选项 2：配置文件**

添加到 `~/.claude.json`：
```json
{
  "mcpServers": {
    "mcp-creator-growth": {
      "command": "~/mcp-creator-growth/.venv/bin/mcp-creator-growth"
    }
  }
}
```

Windows 用户：
```json
{
  "mcpServers": {
    "mcp-creator-growth": {
      "command": "C:\\Users\\YourName\\mcp-creator-growth\\.venv\\Scripts\\mcp-creator-growth.exe"
    }
  }
}
```

示例路径：
- Unix (uv): `~/mcp-creator-growth/.venv/bin/mcp-creator-growth`
- Windows (uv): `C:\\Users\\YourName\\mcp-creator-growth\\.venv\\Scripts\\mcp-creator-growth.exe`
- Windows (conda): `C:\\Users\\YourName\\anaconda3\\envs\\mcp-creator-growth\\Scripts\\mcp-creator-growth.exe`

### Cursor

添加到 Cursor MCP 设置 (Settings → MCP → Add Server)：

```json
{
  "mcp-creator-growth": {
    "command": "~/mcp-creator-growth/.venv/bin/mcp-creator-growth"
  }
}
```

Windows 用户：
```json
{
  "mcp-creator-growth": {
    "command": "C:\\Users\\YourName\\mcp-creator-growth\\.venv\\Scripts\\mcp-creator-growth.exe"
  }
}
```

### Windsurf

添加到 `~/.codeium/windsurf/mcp_config.json`：

```json
{
  "mcpServers": {
    "mcp-creator-growth": {
      "command": "~/mcp-creator-growth/.venv/bin/mcp-creator-growth"
    }
  }
}
```

### 其他 IDE

对于任何兼容 MCP 的 IDE，使用这些设置：
- **Command:** `<install-path>/.venv/bin/mcp-creator-growth` (或 Windows 上的 `.venv\Scripts\mcp-creator-growth.exe`)
- **Transport:** stdio

**配置完成后，重启你的 IDE。**

## 使用方法

### 可用工具

| 工具 | 触发方式 | 面向对象 | 返回 |
|------|---------|-----|---------|
| `learning_session` | 用户显式请求 | **用户** | `{status, action}` - 极简 |
| `debug_search` | 自动 (出错时) | **智能体** | 紧凑摘要 |
| `debug_record` | 自动 (修复后) | **智能体** | `{ok, id}` - 极简 |

### 对于用户：学习会话

对你的 AI 助手说：
- "Quiz me on this change" (针对这个变更考考我)
- "Test my understanding" (测试我的理解)
- "Help me learn about what you did" (帮我学习你做了什么)

Agent 将创建一个互动学习卡片并**等待**直到你完成它。

> **注意**：测验分数保存在本地供你自我追踪，**不会**返回给 Agent - 以保持上下文干净。

### 对于 Agent：调试工具

调试工具在后台静默工作：
- **先搜索**：遇到错误时，Agent 搜索过去的解决方案
- **后记录**：修复错误时，Agent 记录解决方案
- **渐进式披露**：返回紧凑的摘要，而不是完整记录
- **快速查找**：使用倒排索引进行基于关键字的搜索

## 更新

**macOS / Linux:**
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

更新脚本会：
1. 从仓库拉取最新代码
2. 升级所有依赖到最新版本
3. 重启受影响的 MCP 服务器实例

### 手动更新

<details>
<summary>点击展开手动更新步骤</summary>

```bash
# 进入安装目录
cd ~/mcp-creator-growth  # 或你的自定义安装路径

# 拉取最新代码
git pull origin main

# 更新依赖
# 使用 uv
source .venv/bin/activate          # macOS/Linux
# .venv\Scripts\activate           # Windows
uv pip install -e '.[dev]' --upgrade

# 或使用标准 venv
source venv/bin/activate           # macOS/Linux
# venv\Scripts\activate            # Windows
pip install -e '.[dev]' --upgrade
```

</details>

---

## 🔧 故障排除

安装或配置遇到问题？请查看我们的详细故障排除指南：

📖 **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**（英文）

涵盖的常见问题：
- 安装时 Git pull "错误"信息（实际上不是错误！）
- "MCP server already exists"（服务器已存在）提示
- PowerShell 环境变量语法（`$env:USERPROFILE` vs `%USERPROFILE%`）
- MCP 服务器无法启动
- Python 版本问题
- 配置文件位置

---

## 🖼️ 截图

### 学习会话 WebUI

![WebUI 预览](assets/webui-CN.png)

---

## 🔒 安全与隐私

| 方面 | 详情 |
|------|------|
| **本地优先** | 所有数据存储在项目内的 `.mcp-sidecar/` 目录 |
| **无遥测** | 不向外部服务器发送任何数据 |
| **完全掌控** | 随时删除 `.mcp-sidecar/` 即可重置所有数据 |

---

## 🔧 环境变量

| 变量 | 默认值 | 描述 |
|------|--------|------|
| `MCP_DEBUG` | `false` | 启用调试日志（`true`、`1`、`yes`、`on`） |
| `MCP_TIMEOUT` | `120000` | MCP 服务器启动超时时间（毫秒） |
| `MAX_MCP_OUTPUT_TOKENS` | `25000` | MCP 输出的最大 token 数 |

---

## 🤝 贡献

我们欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/amazing-feature`
3. 安装开发依赖：`uv pip install -e '.[dev]'`
4. 进行更改并运行测试：`pytest`
5. 提交 Pull Request

详细指南请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 📬 联系方式

| 渠道 | 地址 |
|------|------|
| **邮箱** | sunflowers0607@outlook.com |
| **邮箱** | weiliu0607@gmail.com |
| **GitHub Issues** | [提交 Issue](https://github.com/SunflowersLwtech/mcp_creator_growth/issues) |

---

## 📄 许可证

本项目基于 [MIT License](LICENSE) 授权。

---

<p align="center">
  基于 <a href="https://github.com/jlowin/fastmcp">FastMCP</a> 构建 •
  <a href="https://modelcontextprotocol.io">MCP 标准</a> •
  <a href="https://glama.ai/mcp/servers/@SunflowersLwtech/mcp_creator_growth">Glama MCP</a>
</p>
