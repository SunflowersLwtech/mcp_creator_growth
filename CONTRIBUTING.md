# Contributing to MCP Creator Growth

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Code Style](#code-style)
- [Testing](#testing)
- [Project Structure](#project-structure)

## Code of Conduct

Please be respectful and constructive in all interactions. We welcome contributors of all experience levels.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/mcp_creator_growth.git
   cd mcp_creator_growth
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/SunflowersLwtech/mcp_creator_growth.git
   ```

## Development Setup

### Prerequisites
- Python 3.11 or higher
- Git

### Setup Steps

1. **Create a virtual environment**:
   ```bash
   python -m venv venv

   # Windows
   .\venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

2. **Install in development mode**:
   ```bash
   pip install -e ".[dev]"
   ```

3. **Configure Claude Code** (for testing):
   ```json
   {
     "mcpServers": {
       "mcp-creator-growth": {
         "command": "/path/to/venv/bin/python",
         "args": ["-m", "mcp_creator_growth"],
         "env": {
           "MCP_DEBUG": "true"
         }
       }
     }
   }
   ```

## Making Changes

### Branch Naming
- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

### Workflow

1. **Create a branch**:
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make your changes** and commit:
   ```bash
   git add .
   git commit -m "Add: description of changes"
   ```

3. **Keep your branch updated**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

### Commit Message Format

Use clear, descriptive commit messages:
- `Add: new feature description`
- `Fix: bug description`
- `Update: what was changed`
- `Refactor: what was refactored`
- `Docs: documentation changes`

## Submitting a Pull Request

1. **Push your branch**:
   ```bash
   git push origin feature/my-feature
   ```

2. **Create a Pull Request** on GitHub

3. **Fill out the PR template** completely

4. **Wait for review** - maintainers will review and provide feedback

5. **Address feedback** - make requested changes and push updates

## Code Style

### Python Style
- Follow PEP 8 guidelines
- Use type hints for function parameters and return values
- Keep functions focused and under 50 lines when possible
- Write docstrings for public functions

### Example
```python
async def process_quiz_result(
    session_id: str,
    answers: list[str],
    score: int
) -> dict[str, Any]:
    """
    Process quiz results and update session.

    Args:
        session_id: Unique session identifier
        answers: List of user answers
        score: Quiz score (0-100)

    Returns:
        dict with status and updated session data
    """
    # Implementation
    pass
```

### Formatting Tools
```bash
# Check style with ruff
pip install ruff
ruff check src/

# Auto-fix issues
ruff check src/ --fix
```

## Testing

### Running Tests
```bash
# Run all tests
pytest dev/tests/ -v

# Run specific phase
pytest dev/tests/phase1/ -v

# Run with coverage
pytest --cov=src/mcp_creator_growth dev/tests/

# Run single test file
pytest dev/tests/phase1/test_learning_session_class.py -v
```

### Writing Tests
- Place tests in `dev/tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use pytest fixtures for common setup

### Test Example
```python
import pytest
from mcp_creator_growth.web.models.learning_session import LearningSession

@pytest.mark.asyncio
async def test_session_creation():
    session = LearningSession(
        session_id="test-123",
        summary="Test summary"
    )
    assert session.session_id == "test-123"
    assert session.status == "pending"
```

## Project Structure

```
mcp_creator_growth/
├── src/mcp_creator_growth/    # Main source code
│   ├── server.py              # MCP server and tools
│   ├── config.py              # Configuration management
│   ├── storage/               # Data persistence
│   └── web/                   # Web UI components
├── dev/
│   ├── docs/                  # Documentation
│   └── tests/                 # Test suites
├── scripts/                   # Installation/update scripts
└── pyproject.toml            # Project configuration
```

### Key Files
- `server.py` - MCP tool definitions (learning_session, debug_search, etc.)
- `web/models/learning_session.py` - Core blocking mechanism
- `storage/path_resolver.py` - Data storage path logic
- `config.py` - TOML configuration handling

## Questions?

- Open an [Issue](https://github.com/SunflowersLwtech/mcp_creator_growth/issues) for questions
- Check existing issues before creating new ones
- Provide as much context as possible

Thank you for contributing!
