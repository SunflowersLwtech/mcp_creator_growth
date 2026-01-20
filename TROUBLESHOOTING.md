# Troubleshooting Guide

This guide helps you resolve common issues with MCP Creator Growth installation and configuration.

## Installation Issues

### 1. Git Pull "Error" Message (PowerShell)

**Symptom:**
```
git : From https://github.com/SunflowersLwtech/mcp_creator_growth
...
+ CategoryInfo          : NotSpecified: (From https://gi...
```

**Explanation:**
- This is **NOT actually an error** - it's just Git's normal output
- The repository was updated successfully (you'll see "Fast-forward" in the output)
- PowerShell misinterprets Git's stderr output as an error

**Solution:**
- ✅ **Ignore this message** - your installation completed successfully
- ✅ Look for "Repository updated successfully" message in newer install scripts
- This issue has been fixed in the latest version of `install.ps1`

---

### 2. "MCP server already exists" Message

**Symptom:**
```
MCP server mcp-creator-growth already exists in local config
```

**Explanation:**
- The MCP server is already configured in Claude Code
- Running `claude mcp add` again attempts to add it twice

**Solution:**
- ✅ **No action needed** - your server is already configured
- To verify configuration: `claude mcp list`
- To remove and re-add: `claude mcp remove mcp-creator-growth` then add again

---

### 3. PowerShell Environment Variable Syntax

**Symptom:**
```powershell
# This doesn't work in PowerShell:
claude mcp add mcp-creator-growth -- %USERPROFILE%\mcp-creator-growth\.venv\Scripts\mcp-creator-growth.exe
```

**Explanation:**
- `%USERPROFILE%` is CMD/batch syntax
- PowerShell doesn't expand `%VARIABLE%` syntax

**Solution:**
Use PowerShell syntax instead:
```powershell
# Correct PowerShell syntax:
claude mcp add mcp-creator-growth -- "$env:USERPROFILE\mcp-creator-growth\.venv\Scripts\mcp-creator-growth.exe"

# Or use shorthand:
claude mcp add mcp-creator-growth -- "~\mcp-creator-growth\.venv\Scripts\mcp-creator-growth.exe"
```

---

## Configuration Issues

### 4. Finding Your Configuration File

**Claude Code CLI:**
- **Windows:** `%USERPROFILE%\.config\claude-cli\config.json`
- **macOS/Linux:** `~/.config/claude-cli/config.json`

**Claude Desktop:**
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

**Cursor/Windsurf:**
- Check their respective documentation for MCP configuration locations

---

### 5. MCP Server Not Starting

**Symptom:**
- Server doesn't appear in Claude Code
- Timeout errors
- No response from server

**Diagnosis Steps:**

1. **Verify installation:**
   ```bash
   # Check if executable exists (Windows)
   dir %USERPROFILE%\mcp-creator-growth\.venv\Scripts\mcp-creator-growth.exe

   # Check if executable exists (Unix)
   ls ~/mcp-creator-growth/.venv/bin/mcp-creator-growth
   ```

2. **Test server manually:**
   ```bash
   # Windows
   %USERPROFILE%\mcp-creator-growth\.venv\Scripts\mcp-creator-growth.exe

   # Unix
   ~/mcp-creator-growth/.venv/bin/mcp-creator-growth
   ```

   Expected output: Server should start and wait for input (press Ctrl+C to exit)

3. **Check configuration:**
   ```bash
   claude mcp list
   ```

   Should show `mcp-creator-growth` in the list

4. **View logs:**
   - Enable debug mode: `export MCP_DEBUG=true` (Unix) or `$env:MCP_DEBUG="true"` (PowerShell)
   - Restart Claude Code
   - Check logs in `~/.config/mcp-sidecar/logs/` (Unix) or `%APPDATA%\mcp-sidecar\logs\` (Windows)

---

### 6. Python Version Issues

**Symptom:**
```
Python 3.11 or higher is required
```

**Solution:**

1. **Check your Python version:**
   ```bash
   python --version
   ```

2. **Install Python 3.11+ or use uv:**
   ```bash
   # Option 1: Install uv (handles Python automatically)
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Option 2: Download Python 3.11+ from python.org
   ```

3. **Re-run installation script**

---

### 7. Virtual Environment Issues

**Symptom:**
- Installation fails during venv creation
- Dependencies fail to install

**Solution:**

1. **Remove old environment:**
   ```bash
   # Windows
   rmdir /s %USERPROFILE%\mcp-creator-growth\.venv

   # Unix
   rm -rf ~/mcp-creator-growth/.venv
   ```

2. **Clear .env_manager file:**
   ```bash
   # Windows
   del %USERPROFILE%\mcp-creator-growth\.env_manager

   # Unix
   rm ~/mcp-creator-growth/.env_manager
   ```

3. **Re-run installation script**

---

### 8. Permission Denied (Unix/Linux)

**Symptom:**
```
Permission denied: ./mcp-creator-growth
```

**Solution:**

1. **Make scripts executable:**
   ```bash
   chmod +x ~/mcp-creator-growth/.venv/bin/mcp-creator-growth
   chmod +x ~/mcp-creator-growth/scripts/*.sh
   ```

2. **Verify permissions:**
   ```bash
   ls -l ~/mcp-creator-growth/.venv/bin/mcp-creator-growth
   ```
   Should show: `-rwxr-xr-x`

---

## Common Questions

### How do I verify my installation?

Run these commands:

```bash
# 1. Check if server is configured
claude mcp list

# 2. Test server manually
# Windows:
%USERPROFILE%\mcp-creator-growth\.venv\Scripts\mcp-creator-growth.exe

# Unix:
~/mcp-creator-growth/.venv/bin/mcp-creator-growth

# 3. Check Claude Code can see it
# Start a new Claude Code session and type:
# /mcp
```

### How do I update?

```bash
# Windows
%USERPROFILE%\mcp-creator-growth\scripts\update.ps1

# Unix
~/mcp-creator-growth/scripts/update.sh
```

### How do I uninstall?

1. **Remove from Claude Code:**
   ```bash
   claude mcp remove mcp-creator-growth
   ```

2. **Delete installation directory:**
   ```bash
   # Windows
   rmdir /s %USERPROFILE%\mcp-creator-growth

   # Unix
   rm -rf ~/mcp-creator-growth
   ```

### How do I move the installation to a different location?

The installation uses absolute paths, so moving it requires reconfiguration:

1. **Move the directory:**
   ```bash
   # Windows
   move %USERPROFILE%\mcp-creator-growth C:\new\location

   # Unix
   mv ~/mcp-creator-growth /new/location
   ```

2. **Remove old configuration:**
   ```bash
   claude mcp remove mcp-creator-growth
   ```

3. **Add with new path:**
   ```bash
   claude mcp add mcp-creator-growth -- /new/location/.venv/bin/mcp-creator-growth
   ```

---

## Getting Help

If you continue to experience issues:

1. **Check the logs:**
   - MCP sidecar logs: `~/.config/mcp-sidecar/logs/`
   - Look for error messages

2. **Enable debug mode:**
   ```bash
   # Unix
   export MCP_DEBUG=true

   # PowerShell
   $env:MCP_DEBUG="true"
   ```

3. **Report an issue:**
   - GitHub: https://github.com/SunflowersLwtech/mcp_creator_growth/issues
   - Include:
     - Operating system and version
     - Python version
     - Error messages
     - Steps to reproduce

---

## Quick Reference

### Useful Commands

```bash
# List MCP servers
claude mcp list

# Add MCP server
claude mcp add mcp-creator-growth -- <path-to-executable>

# Remove MCP server
claude mcp remove mcp-creator-growth

# Update installation
# Windows: %USERPROFILE%\mcp-creator-growth\scripts\update.ps1
# Unix: ~/mcp-creator-growth/scripts/update.sh

# Test server manually
# Windows: %USERPROFILE%\mcp-creator-growth\.venv\Scripts\mcp-creator-growth.exe
# Unix: ~/mcp-creator-growth/.venv/bin/mcp-creator-growth
```

### Environment Variables

```bash
# Enable debug logging
MCP_DEBUG=true

# Set timeout (milliseconds)
MCP_TIMEOUT=30000

# Max output tokens
MAX_MCP_OUTPUT_TOKENS=2000
```

### Configuration Locations

| Platform | Claude Code | Claude Desktop |
|----------|-------------|----------------|
| Windows  | `%USERPROFILE%\.config\claude-cli\config.json` | `%APPDATA%\Claude\claude_desktop_config.json` |
| macOS    | `~/.config/claude-cli/config.json` | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Linux    | `~/.config/claude-cli/config.json` | `~/.config/Claude/claude_desktop_config.json` |
