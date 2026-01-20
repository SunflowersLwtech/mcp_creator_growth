"""
Debug Index Manager
===================

Manages the debug experience index at `.mcp-sidecar/debug/`.
Provides CRUD operations for debug records.
"""

import json
import os
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Any

from ..debug import server_debug_log as debug_log


class DebugIndexManager:
    """
    Manages debug records storage and indexing.

    Storage structure:
    {project_root}/.mcp-sidecar/debug/
    ├── index.json            # Index of all records
    ├── 20260118_001.json     # Individual record files
    └── 20260118_002.json
    """

    def __init__(self, project_directory: str):
        """
        Initialize the debug index manager.

        Args:
            project_directory: The project root directory
        """
        self.project_directory = Path(project_directory).resolve()
        self.storage_dir = self.project_directory / ".mcp-sidecar" / "debug"
        self.index_file = self.storage_dir / "index.json"

        # Ensure storage directory exists
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # Load or create index
        self._index = self._load_index()

    def _load_index(self) -> dict[str, Any]:
        """Load the index from file or create a new one.

        Index structure (Progressive Disclosure):
        - records: Minimal metadata only (id, ts, et, tags)
        - tags: Inverted index for tag-based lookup
        - error_types: Inverted index for error type lookup
        - keywords: Lazy-built, can be rebuilt from records via rebuild_keywords()

        Note: Detailed content (cause, solution) stays in record files.
        """
        if self.index_file.exists():
            try:
                with open(self.index_file, "r", encoding="utf-8") as f:
                    index = json.load(f)
                    # Migrate old index if needed
                    if "keywords" not in index:
                        index["keywords"] = {}
                    if "error_types" not in index:
                        index["error_types"] = {}
                    return index
            except (json.JSONDecodeError, IOError) as e:
                debug_log(f"Error loading index: {e}, creating new index")

        return {
            "version": 3,  # Bumped for progressive disclosure
            "created_at": datetime.now().isoformat(),
            "records": [],
            "tags": {},
            "keywords": {},      # Lazy: rebuilt on demand
            "error_types": {},
        }

    def _save_index(self) -> None:
        """Save the index to file (compact mode for token savings)."""
        self._index["updated_at"] = datetime.now().isoformat()
        with open(self.index_file, "w", encoding="utf-8") as f:
            json.dump(self._index, f, ensure_ascii=False)

    def _extract_keywords(self, text: str) -> list[str]:
        """Extract searchable keywords from text.

        Only extracts meaningful keywords (length > 3) for the inverted index.
        This enables fast keyword-based lookups without full-text search.
        """
        import re
        # Split on non-alphanumeric, filter short/common words
        words = re.split(r'[^a-zA-Z0-9_]+', text.lower())
        stop_words = {
            "a", "an", "the", "is", "are", "was", "were", "be", "been",
            "to", "of", "in", "for", "on", "with", "at", "by", "from",
            "and", "or", "not", "no", "as", "it", "this", "that", "none",
            "true", "false", "null", "undefined", "error", "exception",
        }
        return list(set(w for w in words if len(w) > 3 and w not in stop_words))[:20]

    def _generate_id(self) -> str:
        """Generate a unique ID for a new record."""
        now = datetime.now()
        date_str = now.strftime("%Y%m%d")

        # Create a unique suffix using project hash + timestamp
        project_hash = hashlib.md5(
            str(self.project_directory).encode()
        ).hexdigest()[:4]

        existing = [r["id"] for r in self._index["records"] if r["id"].startswith(date_str)]

        # Find the next available number
        counter = 1
        while f"{date_str}_{project_hash}_{counter:03d}" in existing:
            counter += 1

        return f"{date_str}_{project_hash}_{counter:03d}"

    def record(
        self,
        context: dict[str, Any] | None = None,
        cause: str | None = None,
        solution: str | None = None,
        tags: list[str] | None = None,
        *,
        data: dict[str, Any] | None = None,  # Legacy parameter name for backward compatibility
    ) -> str:
        """
        Record a new debug experience.

        Supports multiple calling conventions:
        1. Single dict: record(context={"context": {...}, "cause": "...", "solution": "...", "tags": [...]})
        2. Separate args: record(context={...}, cause="...", solution="...", tags=[...])
        3. Legacy 'data' parameter: record(data={...}, cause="...", solution="...")

        Args:
            context: Error context dict with error_type, error_message, file, line
            cause: Root cause analysis (when using separate args)
            solution: Solution that worked (when using separate args)
            tags: Optional tags for categorization
            data: Legacy parameter alias for 'context' (backward compatibility)

        Returns:
            str: The ID of the new record
        """
        record_id = self._generate_id()
        timestamp = datetime.now().isoformat()

        # Handle 'data' as legacy alias for 'context'
        if context is None and data is not None:
            context = data
        
        if context is None:
            context = {}

        # Handle both calling conventions
        if "context" in context and "cause" in context and "solution" in context:
            # Full record dict passed
            actual_context = context["context"]
            cause = context["cause"]
            solution = context["solution"]
            tags = context.get("tags", [])
        else:
            # Context dict passed with separate args
            actual_context = context
            cause = cause or ""
            solution = solution or ""
            tags = tags or []

        # Create record
        record = {
            "id": record_id,
            "timestamp": timestamp,
            "context": actual_context,
            "cause": cause,
            "solution": solution,
            "tags": tags,
        }

        # Save record file (compact mode for token savings)
        record_file = self.storage_dir / f"{record_id}.json"
        with open(record_file, "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False)

        # Update index with compact entry
        error_type = actual_context.get("error_type", "Unknown")
        index_entry = {
            "id": record_id,
            "ts": timestamp,  # Shortened key for compactness
            "et": error_type,  # error_type shortened
            "tags": tags[:5],  # Limit stored tags
        }
        self._index["records"].append(index_entry)

        # Update tag inverted index
        for tag in tags:
            tag_lower = tag.lower()
            if tag_lower not in self._index["tags"]:
                self._index["tags"][tag_lower] = []
            self._index["tags"][tag_lower].append(record_id)

        # Update error type inverted index
        et_lower = error_type.lower()
        if et_lower not in self._index["error_types"]:
            self._index["error_types"][et_lower] = []
        self._index["error_types"][et_lower].append(record_id)

        # Update keyword inverted index (from cause and solution)
        keywords = self._extract_keywords(f"{cause} {solution}")
        for kw in keywords:
            if kw not in self._index["keywords"]:
                self._index["keywords"][kw] = []
            if record_id not in self._index["keywords"][kw]:
                self._index["keywords"][kw].append(record_id)

        self._save_index()
        
        # Update project metadata
        try:
            from .project_meta import ProjectMetaManager
            meta = ProjectMetaManager(str(self.project_directory))
            meta.record_debug_entry(record_id)
        except Exception as e:
            debug_log(f"Warning: Could not update project metadata: {e}")

        debug_log(f"Debug record created: {record_id}")
        return record_id

    def get_record(self, record_id: str) -> dict[str, Any] | None:
        """
        Get a specific record by ID.

        Args:
            record_id: The record ID

        Returns:
            The record data or None if not found
        """
        record_file = self.storage_dir / f"{record_id}.json"
        if not record_file.exists():
            return None

        try:
            with open(record_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            debug_log(f"Error reading record {record_id}: {e}")
            return None

    def list_records(self, limit: int = 100) -> list[dict[str, Any]]:
        """
        List all records from the index.

        Args:
            limit: Maximum number of records to return

        Returns:
            List of index entries (with normalized keys)
        """
        records = self._index["records"][-limit:]
        # Normalize compact keys for backward compatibility
        normalized = []
        for r in records:
            normalized.append({
                "id": r.get("id"),
                "timestamp": r.get("ts") or r.get("timestamp"),
                "error_type": r.get("et") or r.get("error_type", "Unknown"),
                "tags": r.get("tags", []),
            })
        return normalized

    def search_by_keywords(self, keywords: list[str], limit: int = 10) -> list[str]:
        """
        Fast keyword search using inverted index.

        Args:
            keywords: List of keywords to search for
            limit: Maximum number of record IDs to return

        Returns:
            List of matching record IDs, sorted by match count
        """
        # Count matches per record
        match_counts: dict[str, int] = {}
        for kw in keywords:
            kw_lower = kw.lower()
            if kw_lower in self._index.get("keywords", {}):
                for record_id in self._index["keywords"][kw_lower]:
                    match_counts[record_id] = match_counts.get(record_id, 0) + 1

        # Sort by match count (descending)
        sorted_ids = sorted(match_counts.keys(), key=lambda x: match_counts[x], reverse=True)
        return sorted_ids[:limit]

    def search_by_tag(self, tag: str) -> list[dict[str, Any]]:
        """
        Search records by tag.

        Args:
            tag: The tag to search for

        Returns:
            List of matching records
        """
        record_ids = self._index["tags"].get(tag.lower(), [])
        return [self.get_record(rid) for rid in record_ids if self.get_record(rid)]

    def search_by_error_type(self, error_type: str) -> list[dict[str, Any]]:
        """
        Search records by error type.

        Args:
            error_type: The error type to search for

        Returns:
            List of matching records
        """
        error_type_lower = error_type.lower()
        matching_ids = self._index.get("error_types", {}).get(error_type_lower)
        if matching_ids is None:
            matching_ids = [
                r["id"] for r in self._index["records"]
                if error_type_lower in (r.get("et") or r.get("error_type", "")).lower()
            ]
        return [self.get_record(rid) for rid in matching_ids if self.get_record(rid)]

    def get_all_tags(self) -> list[str]:
        """Get all unique tags."""
        return list(self._index["tags"].keys())

    def get_record_count(self) -> int:
        """Get total number of records."""
        return len(self._index["records"])

    def clear_all(self) -> None:
        """Clear all records (use with caution)."""
        # Remove all record files
        for record_file in self.storage_dir.glob("*.json"):
            if record_file.name != "index.json":
                record_file.unlink()

        # Reset index
        self._index = {
            "version": 2,
            "created_at": datetime.now().isoformat(),
            "records": [],
            "tags": {},
            "keywords": {},
            "error_types": {},
        }
        self._save_index()

        debug_log("All debug records cleared")

    def rebuild_index(self) -> dict[str, int]:
        """
        Rebuild the entire index from record files (Progressive Disclosure).

        This is useful when:
        - Index is corrupted or lost
        - Migrating to a new index format
        - Cleaning up stale entries

        Returns:
            dict with rebuild statistics
        """
        debug_log("Rebuilding debug index from record files...")

        # Find all record files
        record_files = list(self.storage_dir.glob("*.json"))
        record_files = [f for f in record_files if f.name != "index.json"]

        # Reset index
        new_index = {
            "version": 3,
            "created_at": self._index.get("created_at", datetime.now().isoformat()),
            "rebuilt_at": datetime.now().isoformat(),
            "records": [],
            "tags": {},
            "keywords": {},
            "error_types": {},
        }

        stats = {"records": 0, "errors": 0, "tags": 0, "keywords": 0}

        for record_file in sorted(record_files):
            try:
                with open(record_file, "r", encoding="utf-8") as f:
                    record = json.load(f)

                record_id = record.get("id", record_file.stem)
                error_type = record.get("context", {}).get("error_type", "Unknown")
                tags = record.get("tags", [])

                # Add compact index entry
                new_index["records"].append({
                    "id": record_id,
                    "ts": record.get("timestamp", ""),
                    "et": error_type,
                    "tags": tags[:5],
                })
                stats["records"] += 1

                # Rebuild tag inverted index
                for tag in tags:
                    tag_lower = tag.lower()
                    if tag_lower not in new_index["tags"]:
                        new_index["tags"][tag_lower] = []
                    new_index["tags"][tag_lower].append(record_id)
                    stats["tags"] += 1

                # Rebuild error_types inverted index
                et_lower = error_type.lower()
                if et_lower not in new_index["error_types"]:
                    new_index["error_types"][et_lower] = []
                new_index["error_types"][et_lower].append(record_id)

                # Rebuild keywords inverted index
                cause = record.get("cause", "")
                solution = record.get("solution", "")
                keywords = self._extract_keywords(f"{cause} {solution}")
                for kw in keywords:
                    if kw not in new_index["keywords"]:
                        new_index["keywords"][kw] = []
                    if record_id not in new_index["keywords"][kw]:
                        new_index["keywords"][kw].append(record_id)
                        stats["keywords"] += 1

            except (json.JSONDecodeError, IOError) as e:
                debug_log(f"Error reading record file {record_file}: {e}")
                stats["errors"] += 1

        self._index = new_index
        self._save_index()

        debug_log(f"Index rebuilt: {stats}")
        return stats

    def rebuild_keywords(self) -> int:
        """
        Rebuild only the keywords inverted index (lazy rebuild).

        Useful when keywords index is empty but you need keyword search.
        More efficient than full rebuild if records index is intact.

        Returns:
            Number of keywords indexed
        """
        debug_log("Rebuilding keywords index...")

        self._index["keywords"] = {}
        keyword_count = 0

        for entry in self._index["records"]:
            record_id = entry.get("id")
            record = self.get_record(record_id)
            if not record:
                continue

            cause = record.get("cause", "")
            solution = record.get("solution", "")
            keywords = self._extract_keywords(f"{cause} {solution}")

            for kw in keywords:
                if kw not in self._index["keywords"]:
                    self._index["keywords"][kw] = []
                if record_id not in self._index["keywords"][kw]:
                    self._index["keywords"][kw].append(record_id)
                    keyword_count += 1

        self._save_index()
        debug_log(f"Keywords index rebuilt: {keyword_count} keywords")
        return keyword_count

    def compact_index(self) -> dict[str, int]:
        """
        Remove keywords index to save space (Progressive Disclosure).

        Keywords can be rebuilt on demand via rebuild_keywords().
        This reduces index file size significantly for large projects.

        Returns:
            dict with compaction statistics
        """
        keywords_before = len(self._index.get("keywords", {}))

        # Clear keywords (can be rebuilt on demand)
        self._index["keywords"] = {}

        self._save_index()

        stats = {
            "keywords_removed": keywords_before,
            "records_kept": len(self._index["records"]),
        }
        debug_log(f"Index compacted: {stats}")
        return stats


# Alias for test compatibility
DebugRecordManager = DebugIndexManager
