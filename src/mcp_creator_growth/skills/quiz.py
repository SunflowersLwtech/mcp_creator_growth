"""
Quiz Skill Module
=================

Generates quiz questions based on change summaries.
Extracted from server.py for modularity.
"""

from typing import Any


def detect_change_type(summary: str) -> str:
    """Detect the type of change based on summary keywords."""
    summary_lower = summary.lower()

    # Check for bug fix indicators
    if any(kw in summary_lower for kw in ["fix", "bug", "issue", "error", "crash", "repair", "patch", "resolve"]):
        return "bugfix"

    # Check for performance indicators
    if any(kw in summary_lower for kw in ["performance", "optimize", "speed", "faster", "cache", "efficient", "memory"]):
        return "performance"

    # Check for refactoring indicators
    if any(kw in summary_lower for kw in ["refactor", "restructure", "reorganize", "clean", "simplify", "rename"]):
        return "refactor"

    # Check for security indicators
    if any(kw in summary_lower for kw in ["security", "vulnerab", "auth", "permission", "sanitize", "escape", "inject"]):
        return "security"

    # Check for documentation indicators
    if any(kw in summary_lower for kw in ["document", "readme", "comment", "docstring", "doc"]):
        return "docs"

    # Check for test indicators
    if any(kw in summary_lower for kw in ["test", "spec", "coverage", "assert", "mock"]):
        return "test"

    # Default to new feature
    return "feature"


def generate_default_quizzes(summary: str) -> list[dict[str, Any]]:
    """Generate default quiz questions based on summary content analysis."""
    change_type = detect_change_type(summary)

    # Quiz templates based on change type
    quiz_templates = {
        "bugfix": [
            {
                "question": "What is the main purpose of this change?",
                "options": ["A) Performance improvement", "B) Bug fix", "C) New feature", "D) Refactoring"],
                "answer": "B",
                "explanation": "Based on the summary, this is a bug fix to resolve an existing issue.",
            },
            {
                "question": "What is most important when verifying a bug fix?",
                "options": ["A) The bug no longer occurs", "B) No regression in related features", "C) Root cause is addressed, not just symptoms", "D) All of the above"],
                "answer": "D",
                "explanation": "A complete bug fix verification includes all these aspects.",
            },
            {
                "question": "What documentation should accompany a bug fix?",
                "options": ["A) Steps to reproduce the original issue", "B) Root cause analysis", "C) Prevention measures for similar issues", "D) All of the above"],
                "answer": "D",
                "explanation": "Good bug fix documentation helps prevent similar issues in the future.",
            },
        ],
        "performance": [
            {
                "question": "What is the main purpose of this change?",
                "options": ["A) Performance improvement", "B) Bug fix", "C) New feature", "D) Refactoring"],
                "answer": "A",
                "explanation": "Based on the summary, this is a performance optimization.",
            },
            {
                "question": "How should performance improvements be validated?",
                "options": ["A) Before/after benchmarks", "B) Memory profiling", "C) Load testing", "D) All of the above"],
                "answer": "D",
                "explanation": "Comprehensive performance validation uses multiple measurement methods.",
            },
            {
                "question": "What is a common risk with performance optimizations?",
                "options": ["A) Reduced code readability", "B) Increased complexity", "C) Potential correctness issues", "D) All of the above"],
                "answer": "D",
                "explanation": "Performance optimizations often introduce trade-offs that need careful consideration.",
            },
        ],
        "refactor": [
            {
                "question": "What is the main purpose of this change?",
                "options": ["A) Performance improvement", "B) Bug fix", "C) New feature", "D) Refactoring"],
                "answer": "D",
                "explanation": "Based on the summary, this is a code refactoring for better structure or maintainability.",
            },
            {
                "question": "What is the key principle of refactoring?",
                "options": ["A) Change behavior and structure together", "B) Change structure without changing behavior", "C) Always add new features while refactoring", "D) Refactor without tests"],
                "answer": "B",
                "explanation": "Refactoring should improve code structure while preserving existing behavior.",
            },
            {
                "question": "What should you ensure before refactoring?",
                "options": ["A) Adequate test coverage exists", "B) Changes are incremental and reversible", "C) Each step can be verified", "D) All of the above"],
                "answer": "D",
                "explanation": "Safe refactoring requires tests, incremental changes, and verification at each step.",
            },
        ],
        "security": [
            {
                "question": "What is the main purpose of this change?",
                "options": ["A) Performance improvement", "B) Security enhancement", "C) New feature", "D) Refactoring"],
                "answer": "B",
                "explanation": "Based on the summary, this change addresses security concerns.",
            },
            {
                "question": "What should security changes always include?",
                "options": ["A) Threat model documentation", "B) Security testing", "C) Review by security-aware team members", "D) All of the above"],
                "answer": "D",
                "explanation": "Security changes require comprehensive documentation, testing, and review.",
            },
            {
                "question": "What is critical after deploying security fixes?",
                "options": ["A) Monitor for exploitation attempts", "B) Verify the fix in production", "C) Update security documentation", "D) All of the above"],
                "answer": "D",
                "explanation": "Post-deployment security verification is crucial for ensuring the fix is effective.",
            },
        ],
        "docs": [
            {
                "question": "What is the main purpose of this change?",
                "options": ["A) Performance improvement", "B) Bug fix", "C) Documentation update", "D) Refactoring"],
                "answer": "C",
                "explanation": "Based on the summary, this is a documentation improvement.",
            },
            {
                "question": "What makes documentation effective?",
                "options": ["A) Clear examples", "B) Up-to-date with code", "C) Easy to navigate", "D) All of the above"],
                "answer": "D",
                "explanation": "Effective documentation combines clarity, accuracy, and usability.",
            },
            {
                "question": "When should documentation be updated?",
                "options": ["A) After major releases only", "B) Whenever code behavior changes", "C) Only when users complain", "D) Once a year"],
                "answer": "B",
                "explanation": "Documentation should stay synchronized with code changes.",
            },
        ],
        "test": [
            {
                "question": "What is the main purpose of this change?",
                "options": ["A) Performance improvement", "B) Bug fix", "C) Test improvement", "D) Refactoring"],
                "answer": "C",
                "explanation": "Based on the summary, this change improves test coverage or quality.",
            },
            {
                "question": "What makes a good test?",
                "options": ["A) Tests one specific behavior", "B) Fast and deterministic", "C) Clear failure messages", "D) All of the above"],
                "answer": "D",
                "explanation": "Good tests are focused, reliable, and provide clear feedback on failures.",
            },
            {
                "question": "What should tests NOT do?",
                "options": ["A) Test implementation details", "B) Depend on external services", "C) Have flaky/random failures", "D) All of the above"],
                "answer": "D",
                "explanation": "Tests should be stable, isolated, and test behavior rather than implementation.",
            },
        ],
        "feature": [
            {
                "question": "What is the main purpose of this change?",
                "options": ["A) Performance improvement", "B) Bug fix", "C) New feature", "D) Refactoring"],
                "answer": "C",
                "explanation": "Based on the summary, this appears to be a new feature or enhancement.",
            },
            {
                "question": "What should you verify after adding a new feature?",
                "options": ["A) Feature works as specified", "B) No regression in existing features", "C) Edge cases are handled", "D) All of the above"],
                "answer": "D",
                "explanation": "New feature verification should cover functionality, regression, and edge cases.",
            },
            {
                "question": "What is the potential risk of adding new features?",
                "options": ["A) Breaking existing functionality", "B) Increased maintenance burden", "C) Scope creep", "D) All of the above"],
                "answer": "D",
                "explanation": "New features introduce various risks that need careful management.",
            },
        ],
    }

    return quiz_templates.get(change_type, quiz_templates["feature"])
