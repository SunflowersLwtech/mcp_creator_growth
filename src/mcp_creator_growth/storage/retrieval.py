"""
Debug Retrieval Engine
======================

Provides keyword matching and similarity-based search for debug records.
Used by the debug_search tool to find relevant historical experiences.
"""

import re
from typing import Any

from ..debug import server_debug_log as debug_log
from .debug_index import DebugIndexManager


class DebugRetrieval:
    """
    Retrieval engine for debug records.

    Implements keyword matching and basic similarity scoring
    to find relevant debug experiences.
    """

    def __init__(
        self,
        index_manager: DebugIndexManager | None = None,
        project_directory: str | None = None,
    ):
        """
        Initialize the retrieval engine.

        Supports two calling conventions:
        1. With index_manager: DebugRetrieval(index_manager=manager)
        2. With project_directory: DebugRetrieval(project_directory="/path")

        Args:
            index_manager: The debug index manager to search (optional)
            project_directory: Project directory to create index manager (optional)
        """
        if index_manager is not None:
            self.index_manager = index_manager
        elif project_directory is not None:
            self.index_manager = DebugIndexManager(project_directory)
        else:
            raise ValueError("Either index_manager or project_directory must be provided")

    def search(
        self,
        query: str,
        limit: int = 5,
        error_type: str | None = None,
        tags: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Search for relevant debug records.

        Args:
            query: Search query (error message or description)
            limit: Maximum number of results
            error_type: Optional filter by error type
            tags: Optional filter by tags

        Returns:
            List of matching records with relevance scores
        """
        debug_log(f"Searching debug records: query='{query[:50]}...', limit={limit}")

        # Get all records
        all_records = self._get_all_records()

        if not all_records:
            debug_log("No records found in index")
            return []

        # Score each record
        scored_records = []
        for record in all_records:
            score = self._calculate_relevance(record, query, error_type, tags)
            if score > 0:
                scored_records.append({
                    "record": record,
                    "score": score,
                })

        # Sort by score (descending)
        scored_records.sort(key=lambda x: x["score"], reverse=True)

        # Return top results
        results = []
        for item in scored_records[:limit]:
            record = item["record"]
            record["relevance_score"] = item["score"]
            results.append(record)

        debug_log(f"Found {len(results)} relevant records")
        return results

    def _get_all_records(self) -> list[dict[str, Any]]:
        """Get all records with full data."""
        records = []
        for entry in self.index_manager.list_records(limit=1000):
            full_record = self.index_manager.get_record(entry["id"])
            if full_record:
                records.append(full_record)
        return records

    def _calculate_relevance(
        self,
        record: dict[str, Any],
        query: str,
        error_type: str | None = None,
        tags: list[str] | None = None,
    ) -> float:
        """
        Calculate relevance score for a record.

        Scoring factors:
        - Keyword matches in error message, cause, solution
        - Error type match
        - Tag matches
        - Recency bonus

        Args:
            record: The debug record
            query: Search query
            error_type: Optional error type filter
            tags: Optional tag filters

        Returns:
            Relevance score (0.0 to 1.0+)
        """
        score = 0.0
        query_lower = query.lower()
        query_terms = self._tokenize(query_lower)

        # Error type filter (if specified, must match)
        if error_type:
            record_error_type = record.get("context", {}).get("error_type", "")
            if error_type.lower() not in record_error_type.lower():
                return 0.0  # Doesn't match filter
            score += 0.3  # Bonus for error type match

        # Tag filter (if specified, must have at least one match)
        if tags:
            record_tags = set(t.lower() for t in record.get("tags", []))
            filter_tags = set(t.lower() for t in tags)
            if not record_tags.intersection(filter_tags):
                return 0.0  # No tag match
            # Bonus for each matching tag
            score += 0.1 * len(record_tags.intersection(filter_tags))

        # Search in error message
        error_message = record.get("context", {}).get("error_message", "").lower()
        message_matches = self._count_term_matches(query_terms, error_message)
        score += message_matches * 0.2

        # Search in cause
        cause = record.get("cause", "").lower()
        cause_matches = self._count_term_matches(query_terms, cause)
        score += cause_matches * 0.15

        # Search in solution
        solution = record.get("solution", "").lower()
        solution_matches = self._count_term_matches(query_terms, solution)
        score += solution_matches * 0.15

        # Search in tags
        record_tags = " ".join(record.get("tags", [])).lower()
        tag_matches = self._count_term_matches(query_terms, record_tags)
        score += tag_matches * 0.1

        # Exact phrase match bonus
        if query_lower in error_message or query_lower in cause or query_lower in solution:
            score += 0.3

        return score

    def _tokenize(self, text: str) -> list[str]:
        """
        Tokenize text into search terms.

        Removes common words and normalizes terms.

        Args:
            text: Text to tokenize

        Returns:
            List of terms
        """
        # Split on non-alphanumeric characters
        terms = re.split(r'[^a-zA-Z0-9_]+', text)

        # Filter out short terms and common words
        stop_words = {
            "a", "an", "the", "is", "are", "was", "were", "be", "been",
            "to", "of", "in", "for", "on", "with", "at", "by", "from",
            "and", "or", "not", "no", "as", "it", "this", "that",
        }

        return [t for t in terms if len(t) > 2 and t not in stop_words]

    def _count_term_matches(self, terms: list[str], text: str) -> int:
        """Count how many query terms appear in the text."""
        count = 0
        for term in terms:
            if term in text:
                count += 1
        return count

    def search_similar_errors(
        self,
        error_type: str,
        error_message: str,
        limit: int = 3,
    ) -> list[dict[str, Any]]:
        """
        Search for similar errors based on type and message.

        This is a convenience method for finding related debug experiences
        when encountering an error.

        Args:
            error_type: The type of error (e.g., "ImportError")
            error_message: The error message
            limit: Maximum number of results

        Returns:
            List of similar debug records
        """
        # Combine error type and message for search
        query = f"{error_type} {error_message}"
        return self.search(query, limit=limit, error_type=error_type)

    def get_recent_records(self, limit: int = 10) -> list[dict[str, Any]]:
        """
        Get most recent debug records.

        Args:
            limit: Maximum number of records

        Returns:
            List of recent records
        """
        records = []
        for entry in self.index_manager.list_records(limit=limit):
            full_record = self.index_manager.get_record(entry["id"])
            if full_record:
                records.append(full_record)
        return records


# Alias for test compatibility
DebugSearchEngine = DebugRetrieval
