from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "radar_collector_state.py"


spec = importlib.util.spec_from_file_location("radar_collector_state", MODULE_PATH)
assert spec is not None
radar_collector_state = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(radar_collector_state)


class RadarCollectorStateTest(unittest.TestCase):
    def test_disables_collector_after_repeated_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            name = "reddit-rss:LocalLLaMA"
            for _ in range(3):
                radar_collector_state.record_result(root, name, False, "403")
            self.assertTrue(radar_collector_state.is_disabled(root, name))

    def test_active_collectors_filters_disabled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            names = ["hn:agent", "reddit-rss:test", "pypi-updates:mcp"]
            radar_collector_state.record_result(root, "reddit-rss:test", False, "403")
            radar_collector_state.record_result(root, "reddit-rss:test", False, "403")
            radar_collector_state.record_result(root, "reddit-rss:test", False, "403")
            active = radar_collector_state.active_collectors(root, names)
            self.assertIn("hn:agent", active)
            self.assertNotIn("reddit-rss:test", active)
            self.assertIn("pypi-updates:mcp", active)

    def test_successful_collector_stays_active(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            name = "bluesky:AI agent"
            radar_collector_state.record_result(root, name, True)
            radar_collector_state.record_result(root, name, False, "timeout")
            self.assertFalse(radar_collector_state.is_disabled(root, name))


if __name__ == "__main__":
    unittest.main()
