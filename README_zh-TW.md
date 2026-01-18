# <img src="assets/icon.png" width="48" height="48" align="top" style="margin-right: 10px;"> MCP Creator Growth [訪問官網](https://github.com/SunflowersLwtech/mcp_creator_growth)

[English](README.md) | [简体中文](README_zh-CN.md) | [繁體中文](README_zh-TW.md)

一個具備上下文感知能力的 **Model Context Protocol (MCP)** 伺服器，作為 AI 編程助手的「學習側邊欄」。它通過互動測驗幫助開發者**從 AI 生成的代碼變更中學習**，並為智能體提供持久化的**項目級調試記憶**。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MCP Standard](https://img.shields.io/badge/MCP-Standard-green.svg)](https://modelcontextprotocol.io/)

## 🚀 為什麼使用它？

1.  **對於開發者（學習）**：不要只接受 AI 的代碼——要理解它。當你問「針對這個變更考考我」時，本伺服器會創建一個互動學習卡片，驗證你對邏輯、安全性或性能影響的理解。
2.  **對於智能體（記憶）**：不再重複解決同一個 Bug。伺服器會在後台靜默記錄調試解決方案，並在未來遇到類似錯誤時自動檢索它們。

## ✨ 功能特性

### 🧠 互動學習會話
- **工具**: `learning_session`
- **行為**: 暫停 Agent 並打開本地 Web UI，根據最近的代碼變更生成測驗。
- **觸發**: 用戶顯式請求（例如：「教我這個修復」，「考考我」）。
- **收益**: 確保你在繼續之前理解*為什麼*要做這個變更。

![WebUI 預覽](assets/webui-TW.png)

### 🐞 調試記憶 (RAG)
- **工具**: `debug_search`, `debug_record`
- **行為**:
    - **搜索**: 當錯誤發生時，Agent 靜默搜索你項目中的過往解決方案。
    - **記錄**: 修復 Bug 後，Agent 記錄原因和解決方案。
- **隱私**: 所有數據均存儲在本地 `.mcp-sidecar/` 中。
- **收益**: 為你的項目構建「群體記憶」，讓它隨著時間推移變得更聰明。

### 📚 術語字典
- **工具**: `term_get`
- **行為**: 獲取與你當前工作上下文相關的編程術語和概念。
- **收益**: 幫助你在不離開 IDE 的情況下填補知識空白。

---

## 🛠️ 快速開始

### 一鍵安裝

**macOS / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/SunflowersLwtech/mcp_creator_growth/main/scripts/install.sh | bash
```

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/SunflowersLwtech/mcp_creator_growth/main/scripts/install.ps1 | iex
```

### 手動安裝

先決條件：`uv` (推薦) 或 Python 3.11+。

1.  **克隆倉庫：**
    ```bash
    git clone https://github.com/SunflowersLwtech/mcp_creator_growth.git
    cd mcp_creator_growth
    ```

2.  **安裝依賴：**
    ```bash
    # 使用 uv
    uv venv --python 3.11 .venv
    source .venv/bin/activate  # Windows: .venv\Scripts\activate
    uv pip install -e ".[dev]"
    ```

---

## ⚙️ IDE 配置

將你的 AI 編程助手連接到 MCP 伺服器。

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
*注意：在 Windows 上，使用 `.venv\Scripts\` 內 `mcp-creator-growth.exe` 的完整路徑。*

### Cursor

1.  進入 **Settings** > **MCP**。
2.  點擊 **Add New MCP Server**。
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

## 🔒 安全與數據

- **本地優先**: 所有學習歷史和調試記錄都牢固地存儲在你磁盤上的 `.mcp-sidecar/` 目錄中（位於項目或用戶主目錄下）。
- **無遙測**: 本伺服器不會將你的代碼或測驗表現發送到任何雲伺服器。
- **掌控權**: 你可以隨時刪除 `.mcp-sidecar` 文件夾來重置你的數據。

## 🤝 貢獻

我們歡迎貢獻！請遵循以下步驟：

1.  Fork 本倉庫。
2.  創建特性分支：`git checkout -b feature/amazing-feature`。
3.  安裝開發依賴：`uv pip install -e ".[dev]"`。
4.  進行更改並運行測試：`pytest dev/tests/`。
5.  提交 Pull Request。

## 📄 許可證

本項目基於 [MIT License](LICENSE) 授權。

---

<p align="center">
  基於 <a href="https://github.com/jlowin/fastmcp">FastMCP</a> 構建 • 
  <a href="https://modelcontextprotocol.io">MCP 標準</a>
</p>
