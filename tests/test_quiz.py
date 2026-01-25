"""
Tests for quiz generation and validation logic.
"""

import pytest
from mcp_creator_growth.skills.quiz import (
    detect_change_type,
    generate_default_quizzes,
    validate_quizzes,
    validate_reasoning,
)


def test_detect_change_type_bugfix():
    assert detect_change_type("Fix a bug in the code") == "bugfix"
    assert detect_change_type("Resolve issue #123") == "bugfix"
    assert detect_change_type("Prevent crash on startup") == "bugfix"


def test_detect_change_type_performance():
    assert detect_change_type("Optimize database queries") == "performance"
    assert detect_change_type("Improve speed of rendering") == "performance"


def test_detect_change_type_refactor():
    assert detect_change_type("Refactor user module") == "refactor"
    assert detect_change_type("Clean up code structure") == "refactor"


def test_detect_change_type_security():
    assert detect_change_type("Fix security vulnerability") == "security"
    assert detect_change_type("Sanitize user input") == "security"


def test_detect_change_type_docs():
    assert detect_change_type("Update documentation") == "docs"
    assert detect_change_type("Add docstrings") == "docs"


def test_detect_change_type_test():
    assert detect_change_type("Add unit tests") == "test"
    assert detect_change_type("Improve test coverage") == "test"


def test_detect_change_type_feature():
    assert detect_change_type("Add new login screen") == "feature"
    assert detect_change_type("Implement dark mode") == "feature"


def test_generate_default_quizzes():
    summary = "Fix a bug in the code"
    quizzes = generate_default_quizzes(summary)
    assert len(quizzes) == 3
    assert "bug" in quizzes[0]["question"].lower() or "bug" in quizzes[0]["options"][1].lower()


def test_validate_reasoning_valid():
    reasoning = {
        "goal": "Fix bug",
        "trigger": "User report",
        "mechanism": "Patch",
        "alternatives": "None",
        "risks": "None",
    }
    validate_reasoning(reasoning)
    # Should not raise exception


def test_validate_reasoning_missing_keys():
    reasoning = {"goal": "Fix bug"}
    validate_reasoning(reasoning)
    assert "Not specified: trigger" in reasoning["trigger"]


def test_validate_quizzes_valid():
    quizzes = [
        {
            "question": "Q1",
            "options": ["A", "B"],
            "answer": "A",
            "explanation": "Exp",
        }
    ]
    validate_quizzes(quizzes)
    # Should not raise exception


def test_validate_quizzes_missing_keys():
    quizzes = [{"question": "Q1"}]
    with pytest.raises(ValueError, match="missing required key"):
        validate_quizzes(quizzes)
