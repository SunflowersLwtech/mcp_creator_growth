"""
Terms Index Manager
====================

Manages the terms glossary storage at `.mcp-sidecar/terms/`.
Provides operations for tracking shown terms and retrieving new ones.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any
from collections import OrderedDict

from ..debug import server_debug_log as debug_log
from .terms_data import TERMS_GLOSSARY


class TermsIndexManager:
    """
    Manages terms tracking to ensure no term is shown twice.

    Storage structure:
    {project_root}/.mcp-sidecar/terms/
    └── shown.json         # Record of shown term IDs
    """

    def __init__(self, project_directory: str):
        """
        Initialize the terms index manager.

        Args:
            project_directory: The project root directory
        """
        self.project_directory = Path(project_directory).resolve()
        self.storage_dir = self.project_directory / ".mcp-sidecar" / "terms"
        self.shown_file = self.storage_dir / "shown.json"

        # Ensure storage directory exists
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # Load shown terms
        self._shown = self._load_shown()

        # Build a flat list of all terms with unique IDs
        self._all_terms = self._build_terms_index()

    def _load_shown(self) -> dict[str, Any]:
        """Load the shown terms record."""
        if self.shown_file.exists():
            try:
                with open(self.shown_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                debug_log(f"Error loading shown terms: {e}, creating new record")

        return {
            "version": 1,
            "created_at": datetime.now().isoformat(),
            "shown_ids": [],
        }

    def _save_shown(self) -> None:
        """Save the shown terms record."""
        self._shown["updated_at"] = datetime.now().isoformat()
        with open(self.shown_file, "w", encoding="utf-8") as f:
            json.dump(self._shown, f, ensure_ascii=False, indent=2)

    def _build_terms_index(self) -> OrderedDict[str, dict[str, Any]]:
        """Build a flat index of all terms with unique IDs."""
        terms = OrderedDict()
        for domain, domain_terms in TERMS_GLOSSARY.items():
            for term_data in domain_terms:
                # Create unique ID from domain + term
                term_id = f"{domain}:{term_data['term'].lower().replace(' ', '_')}"
                terms[term_id] = {
                    "id": term_id,
                    "domain": domain,
                    **term_data
                }
        return terms

    def get_unshown_terms(self, count: int = 3, domain: str | None = None) -> list[dict[str, Any]]:
        """
        Get terms that haven't been shown yet.

        Args:
            count: Number of terms to return (1-5)
            domain: Optional domain filter

        Returns:
            List of term dictionaries
        """
        count = max(1, min(5, count))  # Clamp between 1-5
        shown_ids = set(self._shown.get("shown_ids", []))

        result = []
        for term_id, term_data in self._all_terms.items():
            if term_id in shown_ids:
                continue
            if domain and term_data["domain"] != domain:
                continue
            result.append(term_data)
            if len(result) >= count:
                break

        return result

    def mark_as_shown(self, term_ids: list[str]) -> None:
        """
        Mark terms as shown so they won't appear again.

        Args:
            term_ids: List of term IDs to mark as shown
        """
        current_shown = set(self._shown.get("shown_ids", []))
        current_shown.update(term_ids)
        self._shown["shown_ids"] = list(current_shown)
        self._save_shown()
        debug_log(f"Marked {len(term_ids)} terms as shown")

    def get_shown_count(self) -> int:
        """Get the number of terms that have been shown."""
        return len(self._shown.get("shown_ids", []))

    def get_total_count(self) -> int:
        """Get the total number of available terms."""
        return len(self._all_terms)

    def get_remaining_count(self) -> int:
        """Get the number of unshown terms."""
        return self.get_total_count() - self.get_shown_count()

    def reset_shown(self) -> None:
        """Reset shown terms (use with caution)."""
        self._shown = {
            "version": 1,
            "created_at": datetime.now().isoformat(),
            "shown_ids": [],
        }
        self._save_shown()
        debug_log("Terms shown history reset")

    def get_domains(self) -> list[str]:
        """Get all available domains."""
        return list(TERMS_GLOSSARY.keys())

    def get_term_by_id(self, term_id: str) -> dict[str, Any] | None:
        """Get a specific term by its ID."""
        return self._all_terms.get(term_id)

    def search_terms(self, query: str, limit: int = 5) -> list[dict[str, Any]]:
        """
        Search terms by keyword.

        Args:
            query: Search query
            limit: Maximum results to return

        Returns:
            List of matching terms
        """
        query_lower = query.lower()
        results = []

        for term_id, term_data in self._all_terms.items():
            # Search in term name and definition
            if (query_lower in term_data["term"].lower() or
                query_lower in term_data["term_cn"] or
                query_lower in term_data["definition_en"].lower() or
                query_lower in term_data["definition_cn"]):
                results.append(term_data)
                if len(results) >= limit:
                    break

        return results


def get_session_terms(
    project_directory: str,
    count: int = 3,
    domain: str | None = None,
    auto_mark: bool = True,
    lang: str = "en",
) -> list[dict[str, Any]]:
    """
    Get terms for a learning session in a single language.

    This is a convenience function that gets unshown terms,
    optionally marks them as shown, and returns them in the
    specified language format to minimize token usage.

    Args:
        project_directory: Project directory path
        count: Number of terms to get (1-5)
        domain: Optional domain filter
        auto_mark: Whether to automatically mark terms as shown
        lang: Language code ("zh" for Chinese, "en" for English)

    Returns:
        List of term dictionaries with only the requested language
    """
    manager = TermsIndexManager(project_directory)
    terms = manager.get_unshown_terms(count=count, domain=domain)

    if auto_mark and terms:
        manager.mark_as_shown([t["id"] for t in terms])

    # Convert to single-language format to save tokens
    is_chinese = lang.startswith("zh")
    result = []
    for t in terms:
        result.append({
            "id": t["id"],
            "domain": t["domain"],
            "term": t["term_cn"] if is_chinese else t["term"],
            "definition": t["definition_cn"] if is_chinese else t["definition_en"],
        })

    return result
