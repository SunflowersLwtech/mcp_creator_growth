# <img src="assets/icon.png" width="48" height="48" align="top" style="margin-right: 10px;"> MCP Creator Growth [访问官网](https://github.com/SunflowersLwtech/mcp_creator_growth)

一个具备上下文感知能力的 AI 编程助手学习侧边栏，通过互动测验和调试经验追踪，帮助开发者**从 AI 生成的代码变更中学习**。

[English](README.md) | [简体中文](README_zh-CN.md) | [繁體中文](README_zh-TW.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

## 设计理念

> **学习是为了用户。调试是为了智能体 (Agent)。**

本项目遵循两个核心原则：

| 组件 | 用途 | 受益方 |
|-----------|---------|-------------|
| `learning_session` | 帮助用户理解 AI 生成的变更 | **用户** |
| `debug_search/record` | 构建项目特定的知识库 | **智能体** |

### 低干扰，高价值

- **极小的上下文污染**：返回值刻意保持紧凑，以减少 Token 使用
- **渐进式披露**：调试搜索首先返回摘要，而不是完整记录
- **倒排索引**：基于关键字的快速查找，无需加载所有记录
- **本地优先**：所有数据存储在 `.mcp-sidecar/` 中 - 你的数据属于你自己

## 功能特性

- **阻塞式学习会话** - Agent 会暂停，直到你完成学习卡片
- **互动测验** - 通过针对性问题验证你的理解
- **5-Why 溯源** - 理解代码决策背后的“为什么”
- **调试经验 RAG** - 搜索并记录调试解决方案以供复用
- **Token 高效** - 返回最少的数据以减少上下文污染
- **优化的索引** - 用于快速关键字搜索的倒排索引

## 快速开始

### 一键安装

**macOS / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/SunflowersLwtech/mcp_creator_growth/main/scripts/install.sh | bash
```

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/SunflowersLwtech/mcp_creator_growth/main/scripts/install.ps1 | iex
```

安装程序将：
1. 自动检测你的环境 (uv / conda / 系统 Python)
2. 如果需要，通过 uv 安装 Python 3.11+
3. 创建虚拟环境
4. 安装所有依赖项
5. 显示你的 IDE 配置命令

### 手动安装

1. **克隆仓库：**
   ```bash
   git clone https://github.com/SunflowersLwtech/mcp_creator_growth.git
   cd mcp_creator_growth
   ```

2. **创建虚拟环境：**
   ```bash
   # 使用 uv (推荐)
   uv venv --python 3.11 .venv
   source .venv/bin/activate  # 或在 Windows 上使用 .venv\Scripts\activate
   uv pip install -e ".[dev]"

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

**Windows:**
```powershell
~\mcp-creator-growth\scripts\update.ps1
```

然后重启你的 IDE。

## 配置

创建 `~/.config/mcp-sidecar/config.toml` (Unix) 或 `%APPDATA%/mcp-sidecar/config.toml` (Windows)：

```toml
[server]
host = "127.0.0.1"
port = 0  # 自动选择

[storage]
use_global = false  # true = 跨项目共享

[ui]
theme = "auto"  # auto, dark, light
language = "en"  # en, zh-CN

[session]
default_timeout = 600  # 10 分钟
```

## 数据存储

所有数据都存储在本地的 `.mcp-sidecar/` 目录中：

```
.mcp-sidecar/
├── meta.json              # 项目元数据
├── debug/
│   ├── index.json         # 带倒排查找的优化索引
│   └── *.json             # 单个调试记录
├── sessions/
│   └── *.json             # 学习会话历史
└── terms/
    └── shown.json         # 已展示术语追踪
```

**存储位置：**
- **项目级：** `{project}/.mcp-sidecar/` (如果需要可以用 git 追踪)
- **全局级：** `~/.config/mcp-sidecar/` (个人数据，永不追踪)

**索引优化：**
- 针对关键字、标签和错误类型的倒排索引
- 紧凑的记录条目以减小文件大小
- 懒加载 - 仅在需要时获取完整记录

## 开发

```bash
# 运行测试
pytest dev/tests/ -v

# 运行特定阶段
pytest dev/tests/phase1/ -v

# 运行带覆盖率的测试
pytest --cov=src/mcp_creator_growth dev/tests/
```

## 贡献

欢迎贡献！请：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交你的变更 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

## 许可证

MIT License - 详情见 [LICENSE](LICENSE)。

## 致谢

- 基于 [FastMCP](https://github.com/jlowin/fastmcp) 构建
- 灵感来自于对有意义的 AI 辅助学习的需求
