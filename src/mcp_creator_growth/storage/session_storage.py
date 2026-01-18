"""
Session Storage Manager
=======================

Manages persistence of learning sessions to disk.
Sessions are stored in {project}/.mcp-sidecar/sessions/
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from ..debug import server_debug_log as debug_log
from .path_resolver import get_storage_path
from .serializers import save_json_file, load_json_file
from .project_meta import ProjectMetaManager


class SessionStorageManager:
    """
    Manages learning session persistence.
    
    Storage structure:
    {project}/.mcp-sidecar/sessions/
    ├── index.json              # Session index for quick lookup
    ├── 20260118_abc123.json    # Individual session files
    └── 20260118_def456.json
    """
    
    def __init__(self, project_directory: str):
        """
        Initialize the session storage manager.
        
        Args:
            project_directory: The project root directory
        """
        self.project_directory = Path(project_directory).resolve()
        self.storage_dir = get_storage_path(
            project_directory=str(self.project_directory),
            storage_type="sessions",
            use_global=False,
        )
        self.index_file = self.storage_dir / "index.json"
        
        # Ensure storage directory exists
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Load or create index
        self._index = self._load_index()
        
        debug_log(f"Session storage initialized at: {self.storage_dir}")
    
    def _load_index(self) -> dict[str, Any]:
        """Load the session index or create a new one."""
        data = load_json_file(self.index_file)
        if data:
            return data
        
        return {
            "version": 1,
            "created_at": datetime.now().isoformat(),
            "sessions": [],
            "statistics": {
                "total_sessions": 0,
                "total_quiz_score": 0,
                "total_time_spent": 0,
            },
        }
    
    def _save_index(self) -> None:
        """Save the session index."""
        self._index["updated_at"] = datetime.now().isoformat()
        save_json_file(self.index_file, self._index)
    
    def save_session(
        self,
        session_id: str,
        session_data: dict[str, Any],
        quiz_score: int = 0,
        time_spent: float = 0,
        answers: list[Any] | None = None,
    ) -> str:
        """
        Save a completed learning session.
        
        Args:
            session_id: Unique session identifier
            session_data: Session data from LearningSession.get_session_data()
            quiz_score: Quiz score achieved
            time_spent: Time spent in seconds
            answers: Optional quiz answers
            
        Returns:
            Path to saved session file
        """
        timestamp = datetime.now()
        
        # Build session record
        record = {
            "session_id": session_id,
            "saved_at": timestamp.isoformat(),
            "project_directory": str(self.project_directory),
            "summary": session_data.get("summary", ""),
            "reasoning": session_data.get("reasoning", {}),
            "quizzes": session_data.get("quizzes", []),
            "focus_areas": session_data.get("focus_areas", []),
            "results": {
                "quiz_score": quiz_score,
                "time_spent": time_spent,
                "answers": answers or [],
            },
            "metadata": {
                "created_at": session_data.get("created_at", timestamp.isoformat()),
                "completed_at": timestamp.isoformat(),
            },
        }
        
        # Generate filename
        date_str = timestamp.strftime("%Y%m%d")
        short_id = session_id.split("_")[-1] if "_" in session_id else session_id[:8]
        filename = f"{date_str}_{short_id}.json"
        session_file = self.storage_dir / filename
        
        # Save session file
        save_json_file(session_file, record)
        
        # Update index
        index_entry = {
            "session_id": session_id,
            "filename": filename,
            "saved_at": timestamp.isoformat(),
            "quiz_score": quiz_score,
            "time_spent": time_spent,
            "summary_preview": session_data.get("summary", "")[:100],
        }
        self._index["sessions"].append(index_entry)
        
        # Update statistics
        stats = self._index["statistics"]
        stats["total_sessions"] += 1
        stats["total_quiz_score"] += quiz_score
        stats["total_time_spent"] += time_spent
        
        self._save_index()
        
        # Update project metadata
        try:
            meta_manager = ProjectMetaManager(str(self.project_directory))
            meta_manager.record_learning_session(session_id, quiz_score, time_spent)
        except Exception as e:
            debug_log(f"Failed to update project meta: {e}")
        
        debug_log(f"Session saved: {filename}")
        return str(session_file)
    
    def load_session(self, session_id: str) -> dict[str, Any] | None:
        """
        Load a session by ID.
        
        Args:
            session_id: The session ID to load
            
        Returns:
            Session data or None if not found
        """
        # Find in index
        for entry in self._index["sessions"]:
            if entry["session_id"] == session_id:
                session_file = self.storage_dir / entry["filename"]
                return load_json_file(session_file)
        
        return None
    
    def list_sessions(self, limit: int = 50) -> list[dict[str, Any]]:
        """
        List recent sessions.
        
        Args:
            limit: Maximum number of sessions to return
            
        Returns:
            List of session index entries (most recent first)
        """
        sessions = self._index["sessions"][-limit:]
        sessions.reverse()  # Most recent first
        return sessions
    
    def get_session_by_date(self, date: str) -> list[dict[str, Any]]:
        """
        Get all sessions for a specific date.
        
        Args:
            date: Date string in YYYYMMDD format
            
        Returns:
            List of sessions for that date
        """
        return [
            entry for entry in self._index["sessions"]
            if entry["filename"].startswith(date)
        ]
    
    def get_statistics(self) -> dict[str, Any]:
        """Get session statistics."""
        stats = self._index["statistics"].copy()
        
        # Calculate averages
        total = stats["total_sessions"]
        if total > 0:
            stats["average_score"] = stats["total_quiz_score"] / total
            stats["average_time"] = stats["total_time_spent"] / total
        else:
            stats["average_score"] = 0
            stats["average_time"] = 0
        
        return stats
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session.
        
        Args:
            session_id: The session ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        for i, entry in enumerate(self._index["sessions"]):
            if entry["session_id"] == session_id:
                # Remove file
                session_file = self.storage_dir / entry["filename"]
                if session_file.exists():
                    session_file.unlink()
                
                # Update statistics
                stats = self._index["statistics"]
                stats["total_sessions"] -= 1
                stats["total_quiz_score"] -= entry.get("quiz_score", 0)
                stats["total_time_spent"] -= entry.get("time_spent", 0)
                
                # Remove from index
                self._index["sessions"].pop(i)
                self._save_index()
                
                debug_log(f"Session deleted: {session_id}")
                return True
        
        return False
    
    def cleanup_old_sessions(self, max_sessions: int = 100) -> int:
        """
        Remove old sessions if exceeding max limit.
        
        Args:
            max_sessions: Maximum number of sessions to keep
            
        Returns:
            Number of sessions deleted
        """
        sessions = self._index["sessions"]
        if len(sessions) <= max_sessions:
            return 0
        
        # Remove oldest sessions
        to_delete = sessions[:-max_sessions]
        deleted = 0
        
        for entry in to_delete:
            session_file = self.storage_dir / entry["filename"]
            if session_file.exists():
                session_file.unlink()
            deleted += 1
        
        # Update index
        self._index["sessions"] = sessions[-max_sessions:]
        self._save_index()
        
        debug_log(f"Cleaned up {deleted} old sessions")
        return deleted
    
    def export_sessions(self, output_path: Path | str) -> int:
        """
        Export all sessions to a single JSON file.
        
        Args:
            output_path: Path to output file
            
        Returns:
            Number of sessions exported
        """
        output_path = Path(output_path)
        
        all_sessions = []
        for entry in self._index["sessions"]:
            session_file = self.storage_dir / entry["filename"]
            data = load_json_file(session_file)
            if data:
                all_sessions.append(data)
        
        export_data = {
            "version": 1,
            "exported_at": datetime.now().isoformat(),
            "project_directory": str(self.project_directory),
            "statistics": self.get_statistics(),
            "sessions": all_sessions,
        }
        
        save_json_file(output_path, export_data)
        debug_log(f"Exported {len(all_sessions)} sessions to: {output_path}")
        
        return len(all_sessions)
