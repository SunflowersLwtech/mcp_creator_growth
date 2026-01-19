
import unittest
import tempfile
import shutil
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from mcp_creator_growth.storage.debug_index import DebugIndexManager

class TestDebugIndex(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.manager = DebugIndexManager(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_search_by_error_type_compact_key(self):
        """Test that search_by_error_type finds records with compact 'et' key."""
        # Create a record
        rid = self.manager.record(
            context={
                "error_type": "MyCustomError",
                "error_message": "Something happened",
                "file": "test.py",
                "line": 1
            },
            cause="cause",
            solution="solution",
            tags=["test"]
        )

        # Reload manager to ensure it reads from index (simulating persistence)
        # This forces it to rely on the index structure which uses compact keys
        manager2 = DebugIndexManager(self.test_dir)

        # Search
        results = manager2.search_by_error_type("MyCustomError")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], rid)
        self.assertEqual(results[0]["context"]["error_type"], "MyCustomError")

    def test_search_by_error_type_performance(self):
        """Test that search doesn't crash and returns valid records."""
        # Create a record
        rid = self.manager.record(
            context={
                "error_type": "PerfError",
                "error_message": "msg",
            },
            cause="cause",
            solution="solution"
        )

        results = self.manager.search_by_error_type("PerfError")
        self.assertEqual(len(results), 1)

if __name__ == '__main__':
    unittest.main()
