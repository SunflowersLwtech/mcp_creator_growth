# <img src="assets/icon.png" width="48" height="48" align="top" style="margin-right: 10px;"> MCP Creator Growth [訪問官網](https://github.com/SunflowersLwtech/mcp_creator_growth)

一個具備上下文感知能力的 AI 編程助手學習側邊欄，通過互動測驗和調試經驗追蹤，幫助開發者**從 AI 生成的代碼變更中學習**。

[English](README.md) | [简体中文](README_zh-CN.md) | [繁體中文](README_zh-TW.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

## 設計理念

> **學習是為了用戶。調試是為了智能體 (Agent)。**

本項目遵循兩個核心原則：

| 組件 | 用途 | 受益方 |
|-----------|---------|-------------|
| `learning_session` | 幫助用戶理解 AI 生成的變更 | **用戶** |
| `debug_search/record` | 構建項目特定的知識庫 | **智能體** |

### 低干擾，高價值

- **極小的上下文污染**：返回值刻意保持緊湊，以減少 Token 使用
- **漸進式披露**：調試搜索首先返回摘要，而不是完整記錄
- **倒排索引**：基於關鍵字的快速查找，無需加載所有記錄
- **本地優先**：所有數據存儲在 `.mcp-sidecar/` 中 - 你的數據屬於你自己

## 功能特性

- **阻塞式學習會話** - Agent 會暫停，直到你完成學習卡片
- **互動測驗** - 通過針對性問題驗證你的理解
- **5-Why 溯源** - 理解代碼決策背後的「為什麼」
- **調試經驗 RAG** - 搜索並記錄調試解決方案以供複用
- **Token 高效** - 返回最少的數據以減少上下文污染
- **優化的索引** - 用於快速關鍵字搜索的倒排索引

## 快速開始

### 一鍵安裝

**macOS / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/SunflowersLwtech/mcp_creator_growth/main/scripts/install.sh | bash
```

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/SunflowersLwtech/mcp_creator_growth/main/scripts/install.ps1 | iex
```

安裝程序將：
1. 自動檢測你的環境 (uv / conda / 系統 Python)
2. 如果需要，通過 uv 安裝 Python 3.11+
3. 創建虛擬環境
4. 安裝所有依賴項
5. 顯示你的 IDE 配置命令

### 手動安裝

1. **克隆倉庫：**
   ```bash
   git clone https://github.com/SunflowersLwtech/mcp_creator_growth.git
   cd mcp_creator_growth
   ```

2. **創建虛擬環境：**
   ```bash
   # 使用 uv (推薦)
   uv venv --python 3.11 .venv
   source .venv/bin/activate  # 或在 Windows 上使用 .venv\Scripts\activate
   uv pip install -e ".[dev]"

   # 或者使用標準 venv
   python -m venv venv
   source venv/bin/activate  # 或在 Windows 上使用 venv\Scripts\activate
   pip install -e ".[dev]"
   ```

## IDE 配置

安裝後，配置你的 AI 編程 IDE 以使用此 MCP 服務器。

### Claude Code

**選項 1：CLI (推薦)**
```bash
# macOS / Linux
claude mcp add mcp-creator-growth -- ~/mcp-creator-growth/.venv/bin/mcp-creator-growth

# Windows
claude mcp add mcp-creator-growth -- %USERPROFILE%\mcp-creator-growth\.venv\Scripts\mcp-creator-growth.exe
```

**選項 2：配置文件**

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

Windows 用戶：
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

添加到 Cursor MCP 設置 (Settings → MCP → Add Server)：

```json
{
  "mcp-creator-growth": {
    "command": "~/mcp-creator-growth/.venv/bin/mcp-creator-growth"
  }
}
```

Windows 用戶：
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

對於任何兼容 MCP 的 IDE，使用這些設置：
- **Command:** `<install-path>/.venv/bin/mcp-creator-growth` (或 Windows 上的 `.venv\Scripts\mcp-creator-growth.exe`)
- **Transport:** stdio

**配置完成後，重啟你的 IDE。**

## 使用方法

### 可用工具

| 工具 | 觸發方式 | 面向對象 | 返回 |
|------|---------|-----|---------|
| `learning_session` | 用戶顯式請求 | **用戶** | `{status, action}` - 極簡 |
| `debug_search` | 自動 (出錯時) | **智能體** | 緊湊摘要 |
| `debug_record` | 自動 (修復後) | **智能體** | `{ok, id}` - 極簡 |

### 對於用戶：學習會話

對你的 AI 助手說：
- "Quiz me on this change" (針對這個變更考考我)
- "Test my understanding" (測試我的理解)
- "Help me learn about what you did" (幫我學習你做了什麼)

Agent 將創建一個互動學習卡片並**等待**直到你完成它。

> **注意**：測驗分數保存在本地供你自我追蹤，**不會**返回給 Agent - 以保持上下文乾淨。

### 對於 Agent：調試工具

調試工具在後台靜默工作：
- **先搜索**：遇到錯誤時，Agent 搜索過去的解決方案
- **後記錄**：修復錯誤時，Agent 記錄解決方案
- **漸進式披露**：返回緊湊的摘要，而不是完整記錄
- **快速查找**：使用倒排索引進行基於關鍵字的搜索

## 更新

**macOS / Linux:**
```bash
~/mcp-creator-growth/scripts/update.sh
```

**Windows:**
```powershell
~\mcp-creator-growth\scripts\update.ps1
```

然後重啟你的 IDE。

## 配置

創建 `~/.config/mcp-sidecar/config.toml` (Unix) 或 `%APPDATA%/mcp-sidecar/config.toml` (Windows)：

```toml
[server]
host = "127.0.0.1"
port = 0  # 自動選擇

[storage]
use_global = false  # true = 跨項目共享

[ui]
theme = "auto"  # auto, dark, light
language = "en"  # en, zh-CN

[session]
default_timeout = 600  # 10 分鐘
```

## 數據存儲

所有數據都存儲在本地的 `.mcp-sidecar/` 目錄中：

```
.mcp-sidecar/
├── meta.json              # 項目元數據
├── debug/
│   ├── index.json         # 帶倒排查找的優化索引
│   └── *.json             # 單個調試記錄
├── sessions/
│   └── *.json             # 學習會話歷史
└── terms/
    └── shown.json         # 已展示術語追蹤
```

**存儲位置：**
- **項目級：** `{project}/.mcp-sidecar/` (如果需要可以用 git 追蹤)
- **全局級：** `~/.config/mcp-sidecar/` (個人數據，永不追蹤)

**索引優化：**
- 針對關鍵字、標籤和錯誤類型的倒排索引
- 緊湊的記錄條目以減小文件大小
- 懶加載 - 僅在需要時獲取完整記錄

## 開發

```bash
# 運行測試
pytest dev/tests/ -v

# 運行特定階段
pytest dev/tests/phase1/ -v

# 運行帶覆蓋率的測試
pytest --cov=src/mcp_creator_growth dev/tests/
```

## 貢獻

歡迎貢獻！請：

1. Fork 本倉庫
2. 創建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交你的變更 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 開啟 Pull Request

## 許可證

MIT License - 詳情見 [LICENSE](LICENSE)。

## 致謝

- 基於 [FastMCP](https://github.com/jlowin/fastmcp) 構建
- 靈感來自於對有意義的 AI 輔助學習的需求
